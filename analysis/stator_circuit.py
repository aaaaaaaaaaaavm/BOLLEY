"""Bolley A3e: explicit serpentine stator, winding and pulse-circuit screen.

This is a lumped magnetic/circuit model. It defines the iron path and copper behind A3d's field
assumption, then integrates source power over both frozen shots and every CG point. The bands in
validation/A3e_serpentine_stator.md precede the first output.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from induction_screen import channel_state
from interface_fit_screen import cardinal_forces


INPUT = ROOT / "cad" / "serpentine_stator_parameters.json"
FLUXFOIL_INPUT = ROOT / "cad" / "fluxfoil_a3d_parameters.json"
BASELINE = RESULTS / "baseline.json"
OUTPUT = RESULTS / "stator_circuit.json"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def winding_state(field_t: float, p: dict) -> dict:
    magnetic = p["magnetic_circuit"]
    winding = p["winding"]
    architecture = p["architecture"]
    if field_t <= 0.0:
        return {
            "field_rms_t": 0.0,
            "core_field_rms_t": 0.0,
            "mmf_a_turn": 0.0,
            "phase_current_rms_a": 0.0,
            "phase_flux_linkage_wb_turn": 0.0,
            "phase_inductance_h": 0.0,
        }
    rated_field = magnetic["rated_gap_field_rms_t"]
    core_field = magnetic["rated_outer_leg_and_yoke_field_rms_t"] * field_t / rated_field
    gap_mmf = field_t * magnetic["total_low_permeability_length_m"] / MU_0_H_PER_M
    core_h = magnetic["conservative_core_h_at_rated_a_m"] * core_field / magnetic[
        "rated_outer_leg_and_yoke_field_rms_t"
    ]
    core_mmf = core_h * magnetic["mean_core_path_length_m"]
    mmf = gap_mmf + core_mmf
    turns = winding["turns_per_cell"]
    current = mmf / turns
    pole_area = (
        magnetic["gap_face_height_m"] * architecture["phase_cell_axial_length_m"]
    )
    flux_per_cell = field_t * pole_area
    linkage = (
        architecture["cells_in_series_per_phase"] * turns * flux_per_cell
    )
    inductance = linkage / current
    return {
        "field_rms_t": field_t,
        "core_field_rms_t": core_field,
        "gap_mmf_a_turn": gap_mmf,
        "core_mmf_a_turn": core_mmf,
        "mmf_a_turn": mmf,
        "phase_current_rms_a": current,
        "phase_flux_linkage_wb_turn": linkage,
        "phase_inductance_h": inductance,
    }


def calculate() -> dict:
    p = load(INPUT)
    fluxfoil = load(FLUXFOIL_INPUT)
    baseline = load(BASELINE)
    architecture = p["architecture"]
    magnetic = p["magnetic_circuit"]
    winding = p["winding"]
    drive = p["drive"]
    limits = p["bands"]
    foil = fluxfoil["fluxfoil"]

    turns = winding["turns_per_cell"]
    cells_per_phase = architecture["cells_in_series_per_phase"]
    phase_count = architecture["phase_count"]
    channel_count = architecture["channel_count"]
    cell_conductor_length = turns * winding["mean_turn_length_m"]
    cell_resistance = (
        winding["copper_resistivity_ohm_m"]
        * cell_conductor_length
        / winding["copper_area_m2"]
    )
    phase_resistance = cells_per_phase * cell_resistance
    copper_volume = (
        channel_count
        * architecture["total_phase_cells_per_channel"]
        * cell_conductor_length
        * winding["copper_area_m2"]
    )
    copper_mass = copper_volume * winding["copper_density_kg_m3"]
    core_volume = (
        channel_count
        * architecture["total_phase_cells_per_channel"]
        * magnetic["equivalent_core_cross_section_m2"]
        * magnetic["mean_core_path_length_m"]
    )
    core_mass = core_volume * magnetic["steel_density_kg_m3"]
    active_mass = copper_mass + core_mass

    rated = winding_state(magnetic["rated_gap_field_rms_t"], p)
    rated_current_density = (
        rated["phase_current_rms_a"] / winding["copper_area_m2"]
    )
    active_sheet_area = (
        foil["fins_per_channel"]
        * foil["active_fin_height_m"]
        * fluxfoil["interface"]["active_length_m"]
    )

    def core_loss_w(field_t: float, frequency_hz: float) -> float:
        if field_t <= 0.0 or frequency_hz <= 0.0:
            return 0.0
        specific = magnetic["specific_core_loss_at_rated_w_kg"] * (
            field_t / magnetic["rated_gap_field_rms_t"]
        ) ** magnetic["core_loss_flux_exponent"] * (
            frequency_hz / magnetic["core_loss_reference_frequency_hz"]
        ) ** magnetic["core_loss_frequency_exponent"]
        return specific * core_mass / channel_count

    def point_shot(total_force: float, moving_mass: float, y_cg: float, z_cg: float) -> dict:
        acceleration = total_force / moving_mass
        exit_velocity = math.sqrt(
            2.0 * acceleration * fluxfoil["duty"]["powered_length_m"]
        )
        stroke_time = exit_velocity / acceleration
        forces = cardinal_forces(
            total_force,
            y_cg,
            z_cg,
            fluxfoil["interface"]["force_line_radius_m"],
        )
        channel_data = {}
        for name, force in forces.items():
            if force <= 1e-12:
                field = 0.0
            else:
                field = magnetic["rated_gap_field_rms_t"] * math.sqrt(
                    force / drive["field_command_normalization_force_n"]
                )
                field = min(field, magnetic["rated_gap_field_rms_t"])
            foil_copy = json.loads(json.dumps(fluxfoil))
            foil_copy["fluxfoil"]["external_field_rms_t"] = field
            secondary = channel_state(force, active_sheet_area, foil_copy)
            electrical = winding_state(field, p)
            channel_data[name] = {
                "force_n": force,
                "field_rms_t": field,
                "slip_speed_m_s": secondary["slip_speed_m_s"],
                "secondary_loss_w": secondary["secondary_loss_w"],
                "phase_current_rms_a": electrical["phase_current_rms_a"],
                "phase_inductance_h": electrical["phase_inductance_h"],
            }

        steps = drive["integration_steps"]
        dt = stroke_time / (steps - 1)
        source_energy = 0.0
        copper_energy = 0.0
        core_energy = 0.0
        secondary_energy = 0.0
        peak_dc_power = 0.0
        peak_phase_voltage = 0.0
        peak_required_dc_link = 0.0
        peak_frequency = 0.0
        for index in range(steps):
            velocity = acceleration * index * dt
            mechanical_power = total_force * velocity
            secondary_power = 0.0
            copper_power = 0.0
            total_core_power = 0.0
            for channel in channel_data.values():
                force = channel["force_n"]
                field = channel["field_rms_t"]
                current = channel["phase_current_rms_a"]
                if field <= 0.0:
                    continue
                slip = channel["slip_speed_m_s"]
                frequency = (velocity + slip) / architecture["electrical_wavelength_m"]
                peak_frequency = max(peak_frequency, frequency)
                airgap_power = force * (velocity + slip)
                channel_core_loss = core_loss_w(field, frequency)
                channel_copper_loss = phase_count * current**2 * phase_resistance
                secondary_power += channel["secondary_loss_w"]
                copper_power += channel_copper_loss
                total_core_power += channel_core_loss
                real_load_resistance = (
                    (airgap_power + channel_core_loss)
                    / (phase_count * current**2)
                    if current > 0.0
                    else 0.0
                )
                phase_voltage = current * math.hypot(
                    phase_resistance + real_load_resistance,
                    2.0 * math.pi * frequency * channel["phase_inductance_h"],
                )
                required_dc_link = (
                    math.sqrt(6.0)
                    * phase_voltage
                    / drive["space_vector_modulation_utilisation"]
                )
                peak_phase_voltage = max(peak_phase_voltage, phase_voltage)
                peak_required_dc_link = max(peak_required_dc_link, required_dc_link)
            dc_power = (
                mechanical_power + secondary_power + copper_power + total_core_power
            ) / drive["inverter_efficiency"]
            peak_dc_power = max(peak_dc_power, dc_power)
            weight = 0.5 if index in (0, steps - 1) else 1.0
            source_energy += weight * dc_power * dt
            copper_energy += weight * copper_power * dt
            core_energy += weight * total_core_power * dt
            secondary_energy += weight * secondary_power * dt

        copper_temperature_rise = copper_energy / (
            copper_mass * winding["copper_specific_heat_j_kg_k"]
        )
        mechanical_energy = total_force * fluxfoil["duty"]["powered_length_m"]
        return {
            "y_cg_m": y_cg,
            "z_cg_m": z_cg,
            "forces_n": forces,
            "channel_commands": channel_data,
            "acceleration_m_s2": acceleration,
            "exit_velocity_m_s": exit_velocity,
            "stroke_time_s": stroke_time,
            "mechanical_energy_j": mechanical_energy,
            "secondary_energy_j": secondary_energy,
            "copper_energy_j": copper_energy,
            "core_energy_j": core_energy,
            "source_energy_j": source_energy,
            "source_to_payload_efficiency": mechanical_energy / source_energy,
            "peak_dc_power_w": peak_dc_power,
            "peak_phase_voltage_rms_v": peak_phase_voltage,
            "required_dc_link_v": peak_required_dc_link,
            "peak_electrical_frequency_hz": peak_frequency,
            "copper_adiabatic_temperature_rise_k": copper_temperature_rise,
        }

    def grid_case(case: dict) -> dict:
        cg_limit = fluxfoil["interface"]["transverse_cg_limit_m"]
        points = fluxfoil["interface"]["cg_grid_points_per_axis"]
        grid = [(-cg_limit + 2.0 * cg_limit * i / (points - 1)) for i in range(points)]
        records = []
        worst_energy = None
        worst_power = None
        worst_voltage = None
        for y_cg in grid:
            for z_cg in grid:
                record = point_shot(
                    case["total_force_n"], case["moving_mass_kg"], y_cg, z_cg
                )
                records.append(
                    [
                        y_cg,
                        z_cg,
                        record["source_energy_j"],
                        record["peak_dc_power_w"],
                        record["required_dc_link_v"],
                        record["source_to_payload_efficiency"],
                    ]
                )
                if worst_energy is None or record["source_energy_j"] > worst_energy[
                    "source_energy_j"
                ]:
                    worst_energy = record
                if worst_power is None or record["peak_dc_power_w"] > worst_power[
                    "peak_dc_power_w"
                ]:
                    worst_power = record
                if worst_voltage is None or record["required_dc_link_v"] > worst_voltage[
                    "required_dc_link_v"
                ]:
                    worst_voltage = record
        return {
            "grid_point_count": len(records),
            "record_columns": [
                "y_cg_m",
                "z_cg_m",
                "source_energy_j",
                "peak_dc_power_w",
                "required_dc_link_v",
                "source_to_payload_efficiency",
            ],
            "records": records,
            "worst_source_energy_point": worst_energy,
            "worst_peak_power_point": worst_power,
            "worst_voltage_point": worst_voltage,
        }

    reference_case = {
        "total_force_n": baseline["reference_case"]["total_force_n"],
        "moving_mass_kg": baseline["reference_case"]["moving_mass_kg"],
    }
    qualification_case = {
        "total_force_n": baseline["qualification_case"]["total_force_n"],
        "moving_mass_kg": baseline["qualification_case"]["moving_mass_kg"],
    }
    reference = grid_case(reference_case)
    qualification = grid_case(qualification_case)
    maximum_voltage = max(
        reference["worst_voltage_point"]["required_dc_link_v"],
        qualification["worst_voltage_point"]["required_dc_link_v"],
    )
    voltage_margin = drive["nominal_dc_link_v"] / maximum_voltage - 1.0
    max_temperature = max(
        reference["worst_source_energy_point"]["copper_adiabatic_temperature_rise_k"],
        qualification["worst_source_energy_point"]["copper_adiabatic_temperature_rise_k"],
    )
    maximum_frequency = max(
        reference["worst_voltage_point"]["peak_electrical_frequency_hz"],
        qualification["worst_voltage_point"]["peak_electrical_frequency_hz"],
    )

    bands = {
        "slot_array_width": magnetic["slot_array_width_m"] <= limits["maximum_slot_array_width_m"],
        "rated_outer_leg_field": rated["core_field_rms_t"] <= limits["maximum_rated_outer_leg_field_t"],
        "rated_mmf": rated["mmf_a_turn"] <= limits["maximum_rated_mmf_a_turn"],
        "rated_phase_current": rated["phase_current_rms_a"] <= limits["maximum_rated_phase_current_a"],
        "rated_current_density": rated_current_density <= limits["maximum_rated_copper_current_density_a_m2"],
        "active_electromagnetic_mass": active_mass <= limits["maximum_active_electromagnetic_mass_kg"],
        "phase_voltage": max(
            reference["worst_voltage_point"]["peak_phase_voltage_rms_v"],
            qualification["worst_voltage_point"]["peak_phase_voltage_rms_v"],
        ) <= limits["maximum_phase_rms_voltage_v"],
        "required_dc_link_preferred": maximum_voltage <= limits["preferred_required_dc_link_v"],
        "required_dc_link_absolute": maximum_voltage <= limits["absolute_required_dc_link_v"],
        "reference_source_energy": reference["worst_source_energy_point"]["source_energy_j"] <= limits["maximum_reference_source_energy_j"],
        "reference_peak_power": reference["worst_peak_power_point"]["peak_dc_power_w"] <= limits["maximum_reference_peak_dc_power_w"],
        "qualification_peak_power": qualification["worst_peak_power_point"]["peak_dc_power_w"] <= limits["maximum_qualification_peak_dc_power_w"],
        "copper_temperature_rise": max_temperature <= limits["maximum_copper_adiabatic_rise_per_shot_k"],
        "terminal_frequency": maximum_frequency <= limits["maximum_terminal_frequency_hz"],
        "nominal_dc_link_margin": voltage_margin >= limits["minimum_voltage_margin_fraction_on_120v_link"],
    }

    return {
        "evidence": "LUMPED MAGNETIC/CIRCUIT MODEL OUTPUT from ASSUMPTION Gen1 geometry and loss inputs",
        "input_file": "cad/serpentine_stator_parameters.json",
        "fluxfoil_input_file": "cad/fluxfoil_a3d_parameters.json",
        "topology": architecture["topology"],
        "geometry": {
            "channel_count": channel_count,
            "phase_count": phase_count,
            "cells_in_series_per_phase": cells_per_phase,
            "total_phase_cells": channel_count * architecture["total_phase_cells_per_channel"],
            "active_stator_length_m": architecture["active_stator_length_m"],
            "slot_array_width_m": magnetic["slot_array_width_m"],
            "total_low_permeability_length_m": magnetic["total_low_permeability_length_m"],
            "outer_return_leg_width_m": magnetic["outer_return_leg_width_m"],
            "back_yoke_thickness_m": magnetic["back_yoke_thickness_m"],
        },
        "rated_magnetic_circuit": rated,
        "winding": {
            "turns_per_cell": turns,
            "copper_area_m2": winding["copper_area_m2"],
            "rated_current_density_a_m2": rated_current_density,
            "cell_resistance_ohm": cell_resistance,
            "phase_resistance_ohm": phase_resistance,
        },
        "active_electromagnetic_mass": {
            "copper_kg": copper_mass,
            "electrical_steel_kg": core_mass,
            "total_kg": active_mass,
            "excludes": "housing, clamps, insulation, coolant, sensors, inverter, DC link and gate",
        },
        "drive": {
            "nominal_dc_link_v": drive["nominal_dc_link_v"],
            "maximum_model_required_dc_link_v": maximum_voltage,
            "nominal_dc_link_margin_fraction": voltage_margin,
            "maximum_model_frequency_hz": maximum_frequency,
        },
        "reference_case": reference,
        "qualification_case": qualification,
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_SERPENTINE_STATOR_TO_FIELD_FEA_AND_CAD"
            if all(bands.values())
            else "DO_NOT_PROMOTE_SERPENTINE_STATOR"
        ),
        "limits": [
            "The magnetic circuit is one-dimensional and assumes uniform flux through four series slots.",
            "The 80 W/kg core-loss law and conservative H point are assumptions, not selected-material curves.",
            "Mutual inductance, slot leakage, end effects, inverter switching and cable inductance are absent.",
            "Prebias before gate release is assumed; no cold current-rise transient is modelled.",
            "Active electromagnetic mass excludes all structural, thermal, electronic and stored-energy hardware.",
            "Passing does not close force ripple, provider fit, structural preload, wear or hardware force.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = calculate()
    if args.write:
        dump_json(OUTPUT, result)
    elif args.check:
        compare_json(OUTPUT, result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
