"""Bolley A3f: homogenized Fluxbridge cage and compact-primary circuit screen."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from induction_screen import low_slip_solution
from interface_fit_screen import cardinal_forces


INPUT = ROOT / "cad" / "fluxbridge_parameters.json"
OUTPUT = RESULTS / "fluxbridge_cage.json"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7
GRAVITY_M_S2 = 9.81


def load() -> dict:
    with INPUT.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load()
    architecture = p["architecture"]
    interface = p["interface"]
    cage = p["passive_cage"]
    moving_core = p["moving_magnetic_matrix"]
    magnetic = p["magnetic_circuit"]
    winding = p["winding"]
    drive = p["drive"]
    guidance = p["external_guidance"]
    limits = p["bands"]

    channels = architecture["channel_count"]
    phases = architecture["phase_count"]
    cells_per_phase = architecture["cells_per_phase"]
    total_cells = architecture["total_cells_per_channel"]
    fins = interface["fins_per_channel"]
    active_height = interface["active_cage_height_m"]
    active_length = interface["active_length_m"]
    active_area_per_channel = fins * active_height * active_length
    total_fin_height = active_height + 2.0 * cage["end_bus_height_each_m"]

    copper_bar_volume = (
        channels
        * active_area_per_channel
        * cage["equivalent_copper_sheet_thickness_m"]
    )
    copper_bus_volume = (
        channels
        * fins
        * 2.0
        * active_length
        * cage["end_bus_height_each_m"]
        * interface["fin_gross_thickness_m"]
    )
    cage_copper_volume = copper_bar_volume + copper_bus_volume
    cage_copper_mass = cage_copper_volume * cage["copper_density_kg_m3"]
    gross_fin_volume = (
        channels
        * fins
        * active_length
        * total_fin_height
        * interface["fin_gross_thickness_m"]
    )
    magnetic_matrix_envelope_volume = gross_fin_volume - cage_copper_volume
    magnetic_matrix_mass = (
        magnetic_matrix_envelope_volume
        * moving_core["lamination_factor"]
        * moving_core["density_kg_m3"]
    )
    interface_mass = (
        cage_copper_mass
        + magnetic_matrix_mass
        + interface["root_capture_and_encapsulation_allowance_kg"]
    )

    conductance = (
        cage["equivalent_copper_sheet_thickness_m"]
        / cage["copper_resistivity_ohm_m"]
    )
    rated_equivalent_field = magnetic["rated_equivalent_sheet_field_rms_t"]
    tooth_field = rated_equivalent_field / math.sqrt(
        architecture["tooth_duty_fraction"]
    )
    ligament_field = tooth_field / cage["magnetic_ligament_fraction"]
    gap_mmf = (
        tooth_field
        * magnetic["total_series_low_permeability_length_m"]
        / MU_0_H_PER_M
    )
    stationary_core_mmf = (
        magnetic["conservative_stationary_core_h_at_rated_a_m"]
        * magnetic["mean_stationary_core_path_length_m"]
    )
    moving_core_path = fins * interface["fin_gross_thickness_m"]
    moving_core_mmf = moving_core["conservative_h_at_rated_a_m"] * moving_core_path
    rated_mmf = gap_mmf + stationary_core_mmf + moving_core_mmf

    turns = winding["turns_per_cell"]
    conductor_area = winding["conductor_area_per_turn_m2"]
    rated_current = rated_mmf / turns
    rated_primary_current_density = rated_current / conductor_area
    required_slot_copper_area = (
        winding["coil_sides_per_slot"] * turns * conductor_area
    )
    available_slot_area = (
        architecture["winding_slot_width_m"]
        * winding["available_slot_radial_height_m"]
    )
    winding_fill = required_slot_copper_area / available_slot_area

    cell_conductor_length = turns * winding["mean_turn_length_m"]
    cell_resistance = (
        winding["copper_resistivity_ohm_m"]
        * cell_conductor_length
        / conductor_area
    )
    phase_resistance = cells_per_phase * cell_resistance
    primary_copper_volume = (
        channels * total_cells * cell_conductor_length * conductor_area
    )
    primary_copper_mass = primary_copper_volume * winding["copper_density_kg_m3"]
    stationary_core_volume = (
        channels
        * total_cells
        * magnetic["equivalent_stationary_core_cross_section_m2"]
        * magnetic["mean_stationary_core_path_length_m"]
    )
    stationary_core_mass = (
        stationary_core_volume * magnetic["stationary_core_density_kg_m3"]
    )
    active_primary_mass = primary_copper_mass + stationary_core_mass

    pole_area = active_height * architecture["tooth_width_m"]
    flux_per_cell = tooth_field * pole_area
    phase_linkage = cells_per_phase * turns * flux_per_cell
    phase_inductance = phase_linkage / rated_current

    def electrical_state(field_equivalent_t: float) -> dict:
        if field_equivalent_t <= 0.0:
            return {
                "equivalent_field_rms_t": 0.0,
                "tooth_field_rms_t": 0.0,
                "magnetic_ligament_field_rms_t": 0.0,
                "mmf_a_turn": 0.0,
                "phase_current_rms_a": 0.0,
                "phase_inductance_h": phase_inductance,
            }
        ratio = field_equivalent_t / rated_equivalent_field
        return {
            "equivalent_field_rms_t": field_equivalent_t,
            "tooth_field_rms_t": tooth_field * ratio,
            "magnetic_ligament_field_rms_t": ligament_field * ratio,
            "mmf_a_turn": rated_mmf * ratio,
            "phase_current_rms_a": rated_current * ratio,
            "phase_inductance_h": phase_inductance,
        }

    def cage_state(force_n: float, field_t: float) -> dict:
        if force_n <= 1e-12 or field_t <= 0.0:
            return {
                "force_n": 0.0,
                "force_density_pa": 0.0,
                "slip_speed_m_s": 0.0,
                "sheet_reaction_number": 0.0,
                "field_at_cage_rms_t": 0.0,
                "surface_current_rms_a_m": 0.0,
                "bar_current_density_rms_a_m2": 0.0,
                "cage_loss_w": 0.0,
            }
        force_density = force_n / active_area_per_channel
        slip = low_slip_solution(force_density, conductance, field_t)
        reaction = 0.5 * MU_0_H_PER_M * conductance * slip
        sheet_field = field_t / math.sqrt(1.0 + reaction**2)
        surface_current = conductance * slip * sheet_field
        return {
            "force_n": force_n,
            "force_density_pa": force_density,
            "slip_speed_m_s": slip,
            "sheet_reaction_number": reaction,
            "field_at_cage_rms_t": sheet_field,
            "surface_current_rms_a_m": surface_current,
            "bar_current_density_rms_a_m2": surface_current
            / cage["equivalent_copper_sheet_thickness_m"],
            "cage_loss_w": force_n * slip,
        }

    def specific_loss(
        rated_specific_w_kg: float,
        field_t: float,
        rated_field_t: float,
        frequency_hz: float,
        reference_frequency_hz: float,
        flux_exponent: float,
        frequency_exponent: float,
    ) -> float:
        if field_t <= 0.0 or frequency_hz <= 0.0:
            return 0.0
        return rated_specific_w_kg * (field_t / rated_field_t) ** flux_exponent * (
            frequency_hz / reference_frequency_hz
        ) ** frequency_exponent

    rated_cage = cage_state(
        drive["rated_channel_force_n"], rated_equivalent_field
    )
    pressure_per_side = (
        rated_cage["field_at_cage_rms_t"] ** 2 / (2.0 * MU_0_H_PER_M)
    )
    normal_force_per_side = pressure_per_side * active_area_per_channel
    mismatch = drive["side_to_side_field_amplitude_mismatch_fraction"]
    plus_field = rated_cage["field_at_cage_rms_t"] * (1.0 + 0.5 * mismatch)
    minus_field = rated_cage["field_at_cage_rms_t"] * (1.0 - 0.5 * mismatch)
    unbalanced_normal_force = (
        (plus_field**2 - minus_field**2)
        * active_area_per_channel
        / (2.0 * MU_0_H_PER_M)
    )

    def point_shot(bare_payload_mass_kg: float, y_cg: float, z_cg: float) -> dict:
        moving_mass = bare_payload_mass_kg + interface_mass
        acceleration = drive["acceleration_g"] * GRAVITY_M_S2
        total_force = moving_mass * acceleration
        exit_velocity = math.sqrt(2.0 * acceleration * drive["powered_length_m"])
        stroke_time = exit_velocity / acceleration
        forces = cardinal_forces(
            total_force,
            y_cg,
            z_cg,
            interface["force_line_radius_m"],
        )
        channels_state = {}
        for name, force in forces.items():
            field = rated_equivalent_field * math.sqrt(
                max(0.0, force) / drive["rated_channel_force_n"]
            )
            field = min(field, rated_equivalent_field)
            electrical = electrical_state(field)
            secondary = cage_state(force, field)
            channels_state[name] = {
                **secondary,
                **electrical,
            }

        steps = drive["integration_steps"]
        dt = stroke_time / (steps - 1)
        energies = {
            "source_energy_j": 0.0,
            "primary_copper_energy_j": 0.0,
            "stationary_core_energy_j": 0.0,
            "moving_matrix_energy_j": 0.0,
            "cage_copper_energy_j": 0.0,
        }
        cage_energy_by_channel = {name: 0.0 for name in channels_state}
        peak_dc_power = 0.0
        peak_phase_voltage = 0.0
        peak_required_dc_link = 0.0
        peak_frequency = 0.0
        for index in range(steps):
            velocity = acceleration * index * dt
            mechanical_power = total_force * velocity
            cage_power = 0.0
            primary_copper_power = 0.0
            stationary_core_power = 0.0
            moving_matrix_power = 0.0
            for name, state in channels_state.items():
                if state["force_n"] <= 0.0:
                    continue
                frequency = (velocity + state["slip_speed_m_s"]) / architecture[
                    "electrical_wavelength_m"
                ]
                peak_frequency = max(peak_frequency, frequency)
                current = state["phase_current_rms_a"]
                channel_copper_power = phases * current**2 * phase_resistance
                channel_stationary_core_power = specific_loss(
                    magnetic["stationary_specific_loss_at_rated_w_kg"],
                    state["tooth_field_rms_t"],
                    tooth_field,
                    frequency,
                    magnetic["loss_reference_frequency_hz"],
                    magnetic["loss_flux_exponent"],
                    magnetic["loss_frequency_exponent"],
                ) * (stationary_core_mass / channels)
                channel_moving_core_power = specific_loss(
                    moving_core["conservative_specific_loss_at_rated_w_kg"],
                    state["magnetic_ligament_field_rms_t"],
                    ligament_field,
                    frequency,
                    moving_core["loss_reference_frequency_hz"],
                    moving_core["loss_flux_exponent"],
                    moving_core["loss_frequency_exponent"],
                ) * (magnetic_matrix_mass / channels)
                cage_power += state["cage_loss_w"]
                primary_copper_power += channel_copper_power
                stationary_core_power += channel_stationary_core_power
                moving_matrix_power += channel_moving_core_power
                airgap_power = state["force_n"] * (
                    velocity + state["slip_speed_m_s"]
                )
                real_load_resistance = (
                    airgap_power
                    + channel_stationary_core_power
                    + channel_moving_core_power
                ) / (phases * current**2)
                phase_voltage = current * math.hypot(
                    phase_resistance + real_load_resistance,
                    2.0
                    * math.pi
                    * frequency
                    * state["phase_inductance_h"],
                )
                required_dc_link = (
                    math.sqrt(6.0)
                    * phase_voltage
                    / drive["space_vector_modulation_utilisation"]
                )
                peak_phase_voltage = max(peak_phase_voltage, phase_voltage)
                peak_required_dc_link = max(peak_required_dc_link, required_dc_link)

            dc_power = (
                mechanical_power
                + cage_power
                + primary_copper_power
                + stationary_core_power
                + moving_matrix_power
            ) / drive["inverter_efficiency"]
            peak_dc_power = max(peak_dc_power, dc_power)
            weight = 0.5 if index in (0, steps - 1) else 1.0
            energies["source_energy_j"] += weight * dc_power * dt
            energies["primary_copper_energy_j"] += (
                weight * primary_copper_power * dt
            )
            energies["stationary_core_energy_j"] += (
                weight * stationary_core_power * dt
            )
            energies["moving_matrix_energy_j"] += (
                weight * moving_matrix_power * dt
            )
            energies["cage_copper_energy_j"] += weight * cage_power * dt
            for name, state in channels_state.items():
                cage_energy_by_channel[name] += (
                    weight * state["cage_loss_w"] * dt
                )

        mechanical_energy = total_force * drive["powered_length_m"]
        worst_cage_channel_energy = max(cage_energy_by_channel.values())
        cage_mass_per_channel = cage_copper_mass / channels
        primary_copper_rise = energies["primary_copper_energy_j"] / (
            primary_copper_mass * winding["copper_specific_heat_j_kg_k"]
        )
        cage_copper_rise = worst_cage_channel_energy / (
            cage_mass_per_channel * cage["copper_specific_heat_j_kg_k"]
        )
        max_slip = max(state["slip_speed_m_s"] for state in channels_state.values())
        max_cage_j = max(
            state["bar_current_density_rms_a_m2"]
            for state in channels_state.values()
        )
        return {
            "bare_payload_mass_kg": bare_payload_mass_kg,
            "moving_mass_kg": moving_mass,
            "y_cg_m": y_cg,
            "z_cg_m": z_cg,
            "total_force_n": total_force,
            "forces_n": forces,
            "channel_states": channels_state,
            "acceleration_m_s2": acceleration,
            "exit_velocity_m_s": exit_velocity,
            "stroke_time_s": stroke_time,
            "mechanical_energy_j": mechanical_energy,
            **energies,
            "source_to_payload_efficiency": mechanical_energy
            / energies["source_energy_j"],
            "secondary_only_efficiency": mechanical_energy
            / (mechanical_energy + energies["cage_copper_energy_j"]),
            "peak_dc_power_w": peak_dc_power,
            "peak_phase_voltage_rms_v": peak_phase_voltage,
            "required_dc_link_v": peak_required_dc_link,
            "peak_electrical_frequency_hz": peak_frequency,
            "maximum_cage_slip_speed_m_s": max_slip,
            "maximum_cage_current_density_a_m2": max_cage_j,
            "primary_copper_adiabatic_rise_k": primary_copper_rise,
            "maximum_channel_cage_copper_adiabatic_rise_k": cage_copper_rise,
        }

    def grid_case(bare_payload_mass_kg: float) -> dict:
        cg_limit = interface["transverse_cg_limit_m"]
        points = interface["cg_grid_points_per_axis"]
        grid = [
            -cg_limit + 2.0 * cg_limit * index / (points - 1)
            for index in range(points)
        ]
        details = []
        records = []
        for y_cg in grid:
            for z_cg in grid:
                detail = point_shot(bare_payload_mass_kg, y_cg, z_cg)
                details.append(detail)
                records.append(
                    [
                        y_cg,
                        z_cg,
                        detail["source_energy_j"],
                        detail["peak_dc_power_w"],
                        detail["required_dc_link_v"],
                        detail["secondary_only_efficiency"],
                        detail["maximum_channel_cage_copper_adiabatic_rise_k"],
                    ]
                )

        def maximum(key: str):
            return max(details, key=lambda record: record[key])

        def minimum(key: str):
            return min(details, key=lambda record: record[key])

        return {
            "grid_point_count": len(records),
            "record_columns": [
                "y_cg_m",
                "z_cg_m",
                "source_energy_j",
                "peak_dc_power_w",
                "required_dc_link_v",
                "secondary_only_efficiency",
                "maximum_channel_cage_copper_adiabatic_rise_k",
            ],
            "records": records,
            "worst_source_energy_point": maximum("source_energy_j"),
            "worst_peak_power_point": maximum("peak_dc_power_w"),
            "worst_voltage_point": maximum("required_dc_link_v"),
            "worst_primary_copper_rise_point": maximum(
                "primary_copper_adiabatic_rise_k"
            ),
            "worst_cage_copper_rise_point": maximum(
                "maximum_channel_cage_copper_adiabatic_rise_k"
            ),
            "worst_cage_current_density_point": maximum(
                "maximum_cage_current_density_a_m2"
            ),
            "worst_slip_point": maximum("maximum_cage_slip_speed_m_s"),
            "worst_secondary_efficiency_point": minimum(
                "secondary_only_efficiency"
            ),
            "worst_frequency_point": maximum("peak_electrical_frequency_hz"),
        }

    reference = grid_case(interface["bare_payload_reference_mass_kg"])
    qualification = grid_case(interface["bare_payload_qualification_mass_kg"])

    def worst_max(record_key: str, field: str) -> float:
        return max(reference[record_key][field], qualification[record_key][field])

    maximum_required_dc_link = worst_max(
        "worst_voltage_point", "required_dc_link_v"
    )
    nominal_dc_margin = drive["nominal_dc_link_v"] / maximum_required_dc_link - 1.0
    bands = {
        "face_footprint": interface["face_footprint_m"]
        <= limits["maximum_face_footprint_m"],
        "nominal_clearance": interface["clearance_per_side_m"]
        >= limits["minimum_nominal_clearance_per_side_m"],
        "side_protrusion": interface["total_projection_from_rail_plane_m"]
        <= limits["maximum_side_protrusion_m"],
        "interface_mass_preferred": interface_mass
        <= limits["preferred_interface_mass_kg"],
        "interface_mass_absolute": interface_mass
        <= limits["absolute_interface_mass_kg"],
        "magnetic_ligament_field": ligament_field
        <= limits["maximum_magnetic_ligament_field_t"],
        "rated_mmf": rated_mmf <= limits["maximum_rated_mmf_a_turn"],
        "rated_phase_current": rated_current
        <= limits["maximum_rated_phase_current_a"],
        "primary_current_density": rated_primary_current_density
        <= limits["maximum_primary_current_density_a_m2"],
        "winding_slot_fill": winding_fill
        <= limits["maximum_winding_slot_fill_fraction"],
        "active_primary_mass": active_primary_mass
        <= limits["maximum_active_primary_mass_kg"],
        "required_dc_link": maximum_required_dc_link
        <= limits["maximum_required_dc_link_v"],
        "nominal_dc_link_margin": nominal_dc_margin
        >= limits["minimum_margin_on_nominal_dc_link_fraction"],
        "reference_source_energy": reference["worst_source_energy_point"][
            "source_energy_j"
        ]
        <= limits["maximum_reference_source_energy_j"],
        "qualification_source_energy": qualification["worst_source_energy_point"][
            "source_energy_j"
        ]
        <= limits["maximum_qualification_source_energy_j"],
        "peak_dc_power": worst_max("worst_peak_power_point", "peak_dc_power_w")
        <= limits["maximum_peak_dc_power_w"],
        "primary_copper_rise": worst_max(
            "worst_primary_copper_rise_point", "primary_copper_adiabatic_rise_k"
        )
        <= limits["maximum_primary_copper_rise_per_shot_k"],
        "cage_copper_rise": worst_max(
            "worst_cage_copper_rise_point",
            "maximum_channel_cage_copper_adiabatic_rise_k",
        )
        <= limits["maximum_cage_copper_rise_per_shot_k"],
        "cage_current_density": worst_max(
            "worst_cage_current_density_point",
            "maximum_cage_current_density_a_m2",
        )
        <= limits["maximum_cage_current_density_a_m2"],
        "cage_slip": worst_max(
            "worst_slip_point", "maximum_cage_slip_speed_m_s"
        )
        <= limits["maximum_required_cage_slip_m_s"],
        "secondary_only_efficiency": min(
            reference["worst_secondary_efficiency_point"][
                "secondary_only_efficiency"
            ],
            qualification["worst_secondary_efficiency_point"][
                "secondary_only_efficiency"
            ],
        )
        >= limits["minimum_secondary_only_shot_efficiency"],
        "terminal_frequency": worst_max(
            "worst_frequency_point", "peak_electrical_frequency_hz"
        )
        <= limits["maximum_terminal_frequency_hz"],
        "unbalanced_normal_force": unbalanced_normal_force
        <= limits["maximum_unbalanced_normal_force_n"],
    }
    failed = [name for name, passed in bands.items() if not passed]
    return {
        "evidence": "A3f HOMOGENIZED PASSIVE-CAGE + LUMPED MAGNETIC/CIRCUIT MODEL OUTPUT",
        "input_file": str(INPUT.relative_to(ROOT)),
        "topology": architecture["topology"],
        "interface": {
            "active_area_per_channel_m2": active_area_per_channel,
            "cage_copper_kg": cage_copper_mass,
            "magnetic_matrix_kg": magnetic_matrix_mass,
            "root_capture_and_encapsulation_allowance_kg": interface[
                "root_capture_and_encapsulation_allowance_kg"
            ],
            "total_increment_kg": interface_mass,
            "cage_copper_equivalent_sheet_thickness_m": cage[
                "equivalent_copper_sheet_thickness_m"
            ],
            "cage_sheet_conductance_s": conductance,
            "magnetic_ligament_fraction": cage["magnetic_ligament_fraction"],
        },
        "rated_magnetic_circuit": {
            "equivalent_sheet_field_rms_t": rated_equivalent_field,
            "tooth_field_rms_t": tooth_field,
            "magnetic_ligament_field_rms_t": ligament_field,
            "gap_mmf_a_turn": gap_mmf,
            "stationary_core_mmf_a_turn": stationary_core_mmf,
            "moving_matrix_mmf_a_turn": moving_core_mmf,
            "total_mmf_a_turn": rated_mmf,
            "normal_force_per_side_n": normal_force_per_side,
            "unbalanced_normal_force_n": unbalanced_normal_force,
        },
        "rated_cage": rated_cage,
        "winding": {
            "turns_per_cell": turns,
            "rated_phase_current_rms_a": rated_current,
            "conductor_area_per_turn_m2": conductor_area,
            "rated_current_density_a_m2": rated_primary_current_density,
            "required_slot_copper_area_m2": required_slot_copper_area,
            "available_slot_area_m2": available_slot_area,
            "gross_slot_fill_fraction": winding_fill,
            "cell_resistance_ohm": cell_resistance,
            "phase_resistance_ohm": phase_resistance,
            "phase_inductance_h": phase_inductance,
        },
        "active_primary_mass": {
            "copper_kg": primary_copper_mass,
            "stationary_core_kg": stationary_core_mass,
            "total_kg": active_primary_mass,
            "excludes": "housing, insulation, coolant, inverter, DC link, sensors, cables, gate and structure",
        },
        "drive": {
            "nominal_dc_link_v": drive["nominal_dc_link_v"],
            "maximum_required_dc_link_v": maximum_required_dc_link,
            "nominal_dc_link_margin_fraction": nominal_dc_margin,
        },
        "reference_case": reference,
        "qualification_case": qualification,
        "bands": bands,
        "band_count": len(bands),
        "band_pass_count": sum(bands.values()),
        "failed_bands": failed,
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_FLUXBRIDGE_TO_FIELD_FEA_AND_GEN2_CAD"
            if all(bands.values())
            else "DO_NOT_PROMOTE_A3F_FLUXBRIDGE"
        ),
        "limits": [
            "The discrete bar cage is homogenized as an equivalent sheet.",
            "No nonlinear field, cogging, slot-harmonic, end-bus or current-crowding solve is present.",
            "Supplier ribbon data do not prove a cut, bonded or perforated blade.",
            "No provider has accepted the interface or 0.20 mm nominal clearance.",
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
