"""Bolley A3c: thin-sheet travelling-field screen for the Fluxfoil interface.

The model includes thin-sheet reaction, CG force allocation, slip heating, skin depth and
two-sided normal-force mismatch. It does not include a designed stator, end effects or primary
losses. The bands in validation/A3c_fluxfoil_induction.md precede the first output.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from interface_fit_screen import cardinal_forces


INPUT = ROOT / "cad" / "fluxfoil_parameters.json"
BASELINE = RESULTS / "baseline.json"
OUTPUT = RESULTS / "induction_screen.json"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def low_slip_solution(force_density_pa: float, sheet_conductance_s: float, field_rms_t: float) -> float:
    """Solve q=G*u*B0^2/(1+(mu0*G*u/2)^2) on the low-slip branch."""

    a = 0.5 * MU_0_H_PER_M * sheet_conductance_s
    linear = sheet_conductance_s * field_rms_t**2
    discriminant = linear**2 - 4.0 * force_density_pa**2 * a**2
    if discriminant < 0.0:
        raise ValueError("requested force exceeds the thin-sheet travelling-field maximum")
    return (linear - math.sqrt(discriminant)) / (2.0 * force_density_pa * a**2)


def channel_state(force_n: float, active_area_m2: float, p: dict) -> dict:
    foil = p["fluxfoil"]
    conductor = p["conductor"]
    conductance = foil["conductor_thickness_m"] / conductor["resistivity_ohm_m"]
    if force_n <= 1e-12:
        return {
            "force_n": 0.0,
            "force_density_pa": 0.0,
            "slip_speed_m_s": 0.0,
            "sheet_reaction_number": 0.0,
            "field_at_sheet_rms_t": 0.0,
            "surface_current_rms_a_m": 0.0,
            "current_density_rms_a_m2": 0.0,
            "secondary_loss_w": 0.0,
        }
    force_density = force_n / active_area_m2
    slip = low_slip_solution(force_density, conductance, foil["external_field_rms_t"])
    reaction = 0.5 * MU_0_H_PER_M * conductance * slip
    sheet_field = foil["external_field_rms_t"] / math.sqrt(1.0 + reaction**2)
    surface_current = conductance * slip * sheet_field
    return {
        "force_n": force_n,
        "force_density_pa": force_density,
        "slip_speed_m_s": slip,
        "sheet_reaction_number": reaction,
        "field_at_sheet_rms_t": sheet_field,
        "surface_current_rms_a_m": surface_current,
        "current_density_rms_a_m2": surface_current / foil["conductor_thickness_m"],
        "secondary_loss_w": force_n * slip,
    }


def calculate() -> dict:
    p = load(INPUT)
    baseline = load(BASELINE)
    interface = p["interface"]
    foil = p["fluxfoil"]
    conductor = p["conductor"]
    guidance = p["external_guidance"]
    duty = p["duty"]
    limits = p["bands"]

    channels = interface["channel_count"]
    fins = foil["fins_per_channel"]
    active_height = foil["active_fin_height_m"]
    active_length = interface["active_length_m"]
    active_area_per_channel = fins * active_height * active_length
    slot_width = foil["conductor_thickness_m"] + 2.0 * foil["clearance_per_side_m"]
    footprint = fins * slot_width + (fins + 1) * foil["stationary_slot_separator_width_m"]
    usable_face_width = (
        interface["body_face_span_m"]
        - 2.0 * guidance["minimum_rail_width_to_first_protrusion_m"]
    )
    face_fraction = footprint / usable_face_width
    projection = active_height + foil["inactive_tip_radius_allowance_m"]
    protrusion_margin = guidance["maximum_side_protrusion_from_rail_plane_m"] - projection
    rail_edge_clearance = 0.5 * (interface["body_face_span_m"] - footprint)

    conductor_volume = channels * active_area_per_channel * foil["conductor_thickness_m"]
    conductor_mass = conductor_volume * conductor["density_kg_m3"]
    interface_mass = conductor_mass + foil["root_capture_fastener_allowance_kg"]
    conductor_mass_per_channel = conductor_mass / channels

    rating = channel_state(duty["rated_channel_force_n"], active_area_per_channel, p)
    conductance = foil["conductor_thickness_m"] / conductor["resistivity_ohm_m"]
    maximum_force_density = foil["external_field_rms_t"] ** 2 / MU_0_H_PER_M
    force_density_fraction = rating["force_density_pa"] / maximum_force_density
    slip_frequency = rating["slip_speed_m_s"] / foil["electrical_wavelength_m"]
    skin_depth = math.sqrt(
        conductor["resistivity_ohm_m"]
        / (math.pi * MU_0_H_PER_M * conductor["relative_permeability"] * slip_frequency)
    )
    local_heat = rating["secondary_loss_w"] * duty["pulse_duration_s"]
    local_temperature_rise = local_heat / (
        conductor_mass_per_channel * conductor["specific_heat_j_kg_k"]
    )

    pressure_per_side = rating["field_at_sheet_rms_t"] ** 2 / (2.0 * MU_0_H_PER_M)
    normal_force_per_side = pressure_per_side * active_area_per_channel
    mismatch = duty["side_to_side_field_amplitude_mismatch_fraction"]
    plus_field = rating["field_at_sheet_rms_t"] * (1.0 + 0.5 * mismatch)
    minus_field = rating["field_at_sheet_rms_t"] * (1.0 - 0.5 * mismatch)
    unbalanced_normal_force = (
        (plus_field**2 - minus_field**2)
        * active_area_per_channel
        / (2.0 * MU_0_H_PER_M)
    )

    total_force = baseline["qualification_case"]["total_force_n"]
    moving_mass = baseline["qualification_case"]["moving_mass_kg"]
    acceleration = total_force / moving_mass
    exit_velocity = math.sqrt(2.0 * acceleration * duty["powered_length_m"])
    stroke_time = exit_velocity / acceleration
    cg_limit = interface["transverse_cg_limit_m"]
    points = interface["cg_grid_points_per_axis"]
    grid = [(-cg_limit + 2.0 * cg_limit * index / (points - 1)) for index in range(points)]
    grid_records = []
    worst_heat = -1.0
    worst_record = None
    for y_cg in grid:
        for z_cg in grid:
            forces = cardinal_forces(
                total_force, y_cg, z_cg, interface["force_line_radius_m"]
            )
            states = {
                name: channel_state(max(0.0, force), active_area_per_channel, p)
                for name, force in forces.items()
            }
            secondary_power = sum(state["secondary_loss_w"] for state in states.values())
            secondary_heat = secondary_power * stroke_time
            peak_airgap_power = total_force * exit_velocity + secondary_power
            mechanical_energy = total_force * duty["powered_length_m"]
            secondary_only_efficiency = mechanical_energy / (
                mechanical_energy + secondary_heat
            )
            record = {
                "y_cg_m": y_cg,
                "z_cg_m": z_cg,
                "forces_n": forces,
                "channel_states": states,
                "secondary_power_w": secondary_power,
                "secondary_heat_j": secondary_heat,
                "peak_airgap_power_w": peak_airgap_power,
                "secondary_only_shot_efficiency": secondary_only_efficiency,
            }
            grid_records.append(record)
            if secondary_heat > worst_heat:
                worst_heat = secondary_heat
                worst_record = record

    assert worst_record is not None
    start_frequency = rating["slip_speed_m_s"] / foil["electrical_wavelength_m"]
    terminal_frequency = (
        exit_velocity + rating["slip_speed_m_s"]
    ) / foil["electrical_wavelength_m"]

    bands = {
        "side_protrusion": projection <= guidance["maximum_side_protrusion_from_rail_plane_m"],
        "nominal_protrusion_margin": protrusion_margin >= limits["minimum_nominal_protrusion_margin_m"],
        "rail_edge_keepout": rail_edge_clearance >= guidance["minimum_rail_width_to_first_protrusion_m"],
        "projected_usable_face_fraction": face_fraction <= limits["maximum_projected_usable_face_fraction"],
        "interface_mass_preferred": interface_mass <= limits["preferred_interface_mass_kg"],
        "interface_mass_absolute": interface_mass <= limits["absolute_interface_mass_kg"],
        "nominal_slot_clearance": foil["clearance_per_side_m"] >= limits["minimum_nominal_clearance_per_side_m"],
        "low_slip_solution_margin": force_density_fraction <= limits["maximum_force_density_to_sheet_limit_fraction"],
        "required_slip_speed": rating["slip_speed_m_s"] <= limits["maximum_required_slip_speed_m_s"],
        "sheet_reaction": rating["sheet_reaction_number"] <= limits["maximum_sheet_reaction_number"],
        "current_density": rating["current_density_rms_a_m2"] <= limits["maximum_rms_current_density_a_m2"],
        "local_temperature_rise": local_temperature_rise <= limits["maximum_local_adiabatic_temperature_rise_k"],
        "skin_depth": skin_depth / foil["conductor_thickness_m"] >= limits["minimum_skin_depth_to_thickness_ratio"],
        "start_frequency": start_frequency <= limits["maximum_start_frequency_hz"],
        "terminal_frequency": terminal_frequency <= limits["maximum_terminal_frequency_hz"],
        "unbalanced_normal_force": unbalanced_normal_force <= limits["maximum_unbalanced_normal_force_n"],
        "secondary_only_shot_efficiency": worst_record["secondary_only_shot_efficiency"] >= limits["minimum_secondary_only_shot_efficiency"],
        "peak_airgap_power": worst_record["peak_airgap_power_w"] <= limits["maximum_peak_airgap_power_w"],
    }

    return {
        "evidence": "ANALYTICAL THIN-SHEET MODEL OUTPUT from ASSUMPTION geometry/material inputs",
        "input_file": "cad/fluxfoil_parameters.json",
        "topology": "four passive aluminium fins per face between symmetric travelling-field stators",
        "geometry": {
            "channel_count": channels,
            "fins_per_channel": fins,
            "active_fin_height_m": active_height,
            "total_projection_from_rail_plane_m": projection,
            "nominal_protrusion_margin_m": protrusion_margin,
            "conductor_thickness_m": foil["conductor_thickness_m"],
            "slot_width_m": slot_width,
            "stationary_slot_array_footprint_m": footprint,
            "rail_edge_to_array_clearance_m": rail_edge_clearance,
            "usable_face_width_m": usable_face_width,
            "projected_usable_face_fraction": face_fraction,
            "active_sheet_area_m2_per_channel": active_area_per_channel,
            "electrical_wavelength_m": foil["electrical_wavelength_m"],
        },
        "moving_mass": {
            "continuous_aluminium_fins_kg": conductor_mass,
            "root_capture_fastener_allowance_kg": foil["root_capture_fastener_allowance_kg"],
            "interface_increment_kg": interface_mass,
        },
        "rated_channel": {
            **rating,
            "sheet_conductance_s": conductance,
            "maximum_thin_sheet_force_density_pa": maximum_force_density,
            "force_density_to_limit_fraction": force_density_fraction,
            "slip_frequency_hz": slip_frequency,
            "skin_depth_m": skin_depth,
            "skin_depth_to_thickness_ratio": skin_depth / foil["conductor_thickness_m"],
            "adiabatic_heat_j": local_heat,
            "adiabatic_temperature_rise_k": local_temperature_rise,
            "normal_force_per_side_n": normal_force_per_side,
            "field_amplitude_mismatch_fraction": mismatch,
            "unbalanced_normal_force_n": unbalanced_normal_force,
            "start_electrical_frequency_hz": start_frequency,
            "terminal_electrical_frequency_hz": terminal_frequency,
        },
        "qualification_shot": {
            "frozen_total_force_n": total_force,
            "frozen_moving_mass_kg": moving_mass,
            "acceleration_m_s2": acceleration,
            "powered_length_m": duty["powered_length_m"],
            "exit_velocity_m_s": exit_velocity,
            "stroke_time_s": stroke_time,
            "grid_point_count": len(grid_records),
            "worst_secondary_heat_point": worst_record,
            "records": grid_records,
        },
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_FLUXFOIL_TO_EXPLICIT_STATOR_AND_CIRCUIT_MODEL"
            if all(bands.values())
            else "DO_NOT_PROMOTE_FLUXFOIL"
        ),
        "limits": [
            "The conductor is an infinite thin sheet locally; axial ends, fin edges and slot harmonics are absent.",
            "The stated 0.5 T RMS travelling field is an input, not a designed stator result.",
            "Primary copper, core, inverter and DC-link losses are absent.",
            "Normal-force cancellation assumes symmetric stators and the declared field mismatch only.",
            "No structural, vibration, wear, provider-acceptance or hardware evidence is present.",
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
