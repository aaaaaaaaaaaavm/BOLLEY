"""Bolley A3g: robust pitch/field/copper search over the frozen A3f model."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from induction_screen import low_slip_solution
from interface_fit_screen import cardinal_forces


BASE_INPUT = ROOT / "cad" / "fluxbridge_parameters.json"
SEARCH_INPUT = ROOT / "cad" / "fluxbridge_optimization.json"
OUTPUT = RESULTS / "fluxbridge_optimization.json"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7
GRAVITY_M_S2 = 9.81


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    base = load(BASE_INPUT)
    search = load(SEARCH_INPUT)
    architecture = base["architecture"]
    interface = base["interface"]
    cage = base["passive_cage"]
    moving_core = base["moving_magnetic_matrix"]
    magnetic = base["magnetic_circuit"]
    winding = base["winding"]
    drive = base["drive"]
    fixed = search["fixed"]
    limits = search["bands"]

    channels = architecture["channel_count"]
    phases = fixed["phase_count"]
    turns = fixed["turns_per_cell"]
    fins = interface["fins_per_channel"]
    active_height = interface["active_cage_height_m"]
    active_length = interface["active_length_m"]
    active_area = fins * active_height * active_length
    tooth_duty = fixed["tooth_duty_fraction"]
    conductor_mass = _interface_copper_mass(base)
    magnetic_matrix_mass = _interface_magnetic_mass(base, conductor_mass)
    interface_mass = (
        conductor_mass
        + magnetic_matrix_mass
        + interface["root_capture_and_encapsulation_allowance_kg"]
    )
    cage_mass_per_channel = conductor_mass / channels
    base_conductance = (
        cage["equivalent_copper_sheet_thickness_m"]
        / cage["copper_resistivity_ohm_m"]
    )
    base_tooth_field = magnetic["rated_equivalent_sheet_field_rms_t"] / math.sqrt(
        architecture["tooth_duty_fraction"]
    )
    base_ligament_field = base_tooth_field / cage["magnetic_ligament_fraction"]

    cg_limit = interface["transverse_cg_limit_m"]
    cg_points = interface["cg_grid_points_per_axis"]
    cg_grid = [
        -cg_limit + 2.0 * cg_limit * index / (cg_points - 1)
        for index in range(cg_points)
    ]
    corner_values = search["robustness_corners"]
    robustness_corners = [
        {
            "clearance_per_side_m": clearance,
            "cage_sheet_conductance_multiplier": conductance_multiplier,
            "stationary_core_h_multiplier": h_multiplier,
        }
        for clearance, conductance_multiplier, h_multiplier in itertools.product(
            corner_values["clearance_per_side_m"],
            corner_values["cage_sheet_conductance_multiplier"],
            corner_values["stationary_core_h_multiplier"],
        )
    ]

    candidate_records = []
    for geometry in search["candidate_geometry"]:
        for equivalent_field in search["candidate_equivalent_sheet_field_rms_t"]:
            design = design_state(
                base,
                search,
                geometry,
                equivalent_field,
                base_tooth_field,
                base_ligament_field,
            )
            corner_records = []
            for corner in robustness_corners:
                corner_state = magnetic_corner_state(
                    base,
                    design,
                    corner,
                    base_tooth_field,
                    base_ligament_field,
                )
                conductance = (
                    base_conductance
                    * corner["cage_sheet_conductance_multiplier"]
                )
                reference = evaluate_case(
                    base,
                    design,
                    corner_state,
                    conductance,
                    interface["bare_payload_reference_mass_kg"],
                    interface_mass,
                    conductor_mass,
                    magnetic_matrix_mass,
                    cg_grid,
                )
                qualification = evaluate_case(
                    base,
                    design,
                    corner_state,
                    conductance,
                    interface["bare_payload_qualification_mass_kg"],
                    interface_mass,
                    conductor_mass,
                    magnetic_matrix_mass,
                    cg_grid,
                )
                rated_cage = cage_state(
                    drive["rated_channel_force_n"],
                    design["equivalent_field_rms_t"],
                    conductance,
                    active_area,
                    cage["equivalent_copper_sheet_thickness_m"],
                )
                mismatch = drive[
                    "side_to_side_field_amplitude_mismatch_fraction"
                ]
                plus_field = rated_cage["field_at_cage_rms_t"] * (
                    1.0 + 0.5 * mismatch
                )
                minus_field = rated_cage["field_at_cage_rms_t"] * (
                    1.0 - 0.5 * mismatch
                )
                normal_residual = (
                    (plus_field**2 - minus_field**2)
                    * active_area
                    / (2.0 * MU_0_H_PER_M)
                )
                maximum_dc_link = max(
                    reference["maximum_required_dc_link_v"],
                    qualification["maximum_required_dc_link_v"],
                )
                dc_margin = drive["nominal_dc_link_v"] / maximum_dc_link - 1.0
                bands = {
                    "active_length": fixed["minimum_active_stator_length_m"] - 1e-12
                    <= design["active_stator_length_m"]
                    <= fixed["maximum_active_stator_length_m"] + 1e-12,
                    "three_phase_cell_count": design["total_cells_per_channel"]
                    % phases
                    == 0,
                    "magnetic_ligament_field": design[
                        "magnetic_ligament_field_rms_t"
                    ]
                    <= limits["maximum_magnetic_ligament_field_t"],
                    "rated_mmf": corner_state["rated_mmf_a_turn"]
                    <= limits["maximum_rated_mmf_a_turn"],
                    "rated_phase_current": corner_state["rated_phase_current_a"]
                    <= limits["maximum_rated_phase_current_a"],
                    "primary_current_density": corner_state[
                        "rated_primary_current_density_a_m2"
                    ]
                    <= limits["maximum_primary_current_density_a_m2"],
                    "winding_slot_fill": design["gross_slot_fill_fraction"]
                    <= limits["maximum_winding_slot_fill_fraction"] + 1e-12,
                    "active_primary_mass": design["active_primary_mass_kg"]
                    <= limits["maximum_active_primary_mass_kg"],
                    "required_dc_link": maximum_dc_link
                    <= limits["maximum_required_dc_link_v"],
                    "dc_link_margin": dc_margin
                    >= limits["minimum_margin_on_48v_link_fraction"],
                    "reference_source_energy": reference[
                        "maximum_source_energy_j"
                    ]
                    <= limits["maximum_reference_source_energy_j"],
                    "qualification_source_energy": qualification[
                        "maximum_source_energy_j"
                    ]
                    <= limits["maximum_qualification_source_energy_j"],
                    "source_efficiency": min(
                        reference["minimum_source_to_payload_efficiency"],
                        qualification["minimum_source_to_payload_efficiency"],
                    )
                    >= limits["minimum_source_to_payload_efficiency"],
                    "peak_dc_power": max(
                        reference["maximum_peak_dc_power_w"],
                        qualification["maximum_peak_dc_power_w"],
                    )
                    <= limits["maximum_peak_dc_power_w"],
                    "primary_copper_rise": max(
                        reference["maximum_primary_copper_rise_k"],
                        qualification["maximum_primary_copper_rise_k"],
                    )
                    <= limits["maximum_primary_copper_rise_per_shot_k"],
                    "cage_copper_rise": max(
                        reference["maximum_cage_copper_rise_k"],
                        qualification["maximum_cage_copper_rise_k"],
                    )
                    <= limits["maximum_cage_copper_rise_per_shot_k"],
                    "cage_current_density": max(
                        reference["maximum_cage_current_density_a_m2"],
                        qualification["maximum_cage_current_density_a_m2"],
                    )
                    <= limits["maximum_cage_current_density_a_m2"],
                    "cage_slip": max(
                        reference["maximum_cage_slip_m_s"],
                        qualification["maximum_cage_slip_m_s"],
                    )
                    <= limits["maximum_required_cage_slip_m_s"],
                    "secondary_efficiency": min(
                        reference["minimum_secondary_only_efficiency"],
                        qualification["minimum_secondary_only_efficiency"],
                    )
                    >= limits["minimum_secondary_only_efficiency"],
                    "terminal_frequency": max(
                        reference["maximum_terminal_frequency_hz"],
                        qualification["maximum_terminal_frequency_hz"],
                    )
                    <= limits["maximum_terminal_frequency_hz"],
                    "unbalanced_normal_force": normal_residual
                    <= limits["maximum_unbalanced_normal_force_n"],
                }
                corner_records.append(
                    {
                        "corner": corner,
                        "magnetic": {
                            "rated_mmf_a_turn": corner_state["rated_mmf_a_turn"],
                            "rated_phase_current_a": corner_state["rated_phase_current_a"],
                            "rated_primary_current_density_a_m2": corner_state[
                                "rated_primary_current_density_a_m2"
                            ],
                            "phase_inductance_h": corner_state["phase_inductance_h"],
                        },
                        "reference": compact_case(reference),
                        "qualification": compact_case(qualification),
                        "maximum_required_dc_link_v": maximum_dc_link,
                        "dc_link_margin_fraction": dc_margin,
                        "unbalanced_normal_force_n": normal_residual,
                        "band_pass_count": sum(bands.values()),
                        "band_count": len(bands),
                        "pass": all(bands.values()),
                        "failed_bands": [
                            name for name, passed in bands.items() if not passed
                        ],
                    }
                )

            feasible = all(record["pass"] for record in corner_records)
            worst_qualification_energy = max(
                record["qualification"]["maximum_source_energy_j"]
                for record in corner_records
            )
            worst_reference_energy = max(
                record["reference"]["maximum_source_energy_j"]
                for record in corner_records
            )
            failed_union = sorted(
                {
                    band
                    for record in corner_records
                    for band in record["failed_bands"]
                }
            )
            candidate_records.append(
                {
                    "candidate_id": (
                        f"p{design['cell_pitch_m'] * 1e3:.0f}_"
                        f"B{design['equivalent_field_rms_t']:.2f}"
                    ),
                    "design": design,
                    "corner_count": len(corner_records),
                    "corners": corner_records,
                    "feasible": feasible,
                    "failed_band_union": failed_union,
                    "worst_reference_source_energy_j": worst_reference_energy,
                    "worst_qualification_source_energy_j": worst_qualification_energy,
                    "selection_key": [
                        worst_qualification_energy,
                        design["active_primary_mass_kg"],
                        design["equivalent_field_rms_t"],
                    ],
                }
            )

    feasible_candidates = [record for record in candidate_records if record["feasible"]]
    selected = (
        min(feasible_candidates, key=lambda record: tuple(record["selection_key"]))
        if feasible_candidates
        else None
    )
    return {
        "evidence": "A3g ROBUST CONSTRAINED ANALYTICAL DESIGN-SPACE SEARCH",
        "base_input_file": str(BASE_INPUT.relative_to(ROOT)),
        "search_input_file": str(SEARCH_INPUT.relative_to(ROOT)),
        "selection_rule": fixed["objective"],
        "candidate_count": len(candidate_records),
        "corners_per_candidate": len(robustness_corners),
        "total_candidate_corner_evaluations": len(candidate_records)
        * len(robustness_corners),
        "cg_points_per_case_per_corner": len(cg_grid) ** 2,
        "interface_increment_kg": interface_mass,
        "candidate_records": candidate_records,
        "corner_band_order": sorted(
            [
                "active_length",
                "three_phase_cell_count",
                "magnetic_ligament_field",
                "rated_mmf",
                "rated_phase_current",
                "primary_current_density",
                "winding_slot_fill",
                "active_primary_mass",
                "required_dc_link",
                "dc_link_margin",
                "reference_source_energy",
                "qualification_source_energy",
                "source_efficiency",
                "peak_dc_power",
                "primary_copper_rise",
                "cage_copper_rise",
                "cage_current_density",
                "cage_slip",
                "secondary_efficiency",
                "terminal_frequency",
                "unbalanced_normal_force",
            ]
        ),
        "feasible_candidate_count": len(feasible_candidates),
        "selected_candidate_id": selected["candidate_id"] if selected else None,
        "selected_candidate": selected,
        "screen_pass": selected is not None,
        "disposition": (
            "FREEZE_SELECTED_A3G_POINT_FOR_FIELD_FEA_AND_GEN2_CAD"
            if selected
            else "NO_ROBUST_A3G_CANDIDATE"
        ),
        "limits": [
            "The search inherits A3f's homogenized cage and lumped magnetic model.",
            "Robustness corners are declared model perturbations, not measured tolerances.",
            "The winding window is sectional; end-turn routing remains a CAD gate.",
        ],
    }


def _interface_copper_mass(base: dict) -> float:
    architecture = base["architecture"]
    interface = base["interface"]
    cage = base["passive_cage"]
    channels = architecture["channel_count"]
    fins = interface["fins_per_channel"]
    bar_volume = (
        channels
        * fins
        * interface["active_cage_height_m"]
        * interface["active_length_m"]
        * cage["equivalent_copper_sheet_thickness_m"]
    )
    bus_volume = (
        channels
        * fins
        * 2.0
        * interface["active_length_m"]
        * cage["end_bus_height_each_m"]
        * interface["fin_gross_thickness_m"]
    )
    return (bar_volume + bus_volume) * cage["copper_density_kg_m3"]


def compact_case(record: dict) -> dict:
    """Drop repeated per-metric locations while preserving every evaluated limit quantity."""

    return {
        key: value
        for key, value in record.items()
        if key != "worst_metric_locations_yz_m"
    }


def _interface_magnetic_mass(base: dict, copper_mass: float) -> float:
    architecture = base["architecture"]
    interface = base["interface"]
    cage = base["passive_cage"]
    moving_core = base["moving_magnetic_matrix"]
    channels = architecture["channel_count"]
    fins = interface["fins_per_channel"]
    total_height = interface["active_cage_height_m"] + 2.0 * cage[
        "end_bus_height_each_m"
    ]
    gross_volume = (
        channels
        * fins
        * interface["active_length_m"]
        * total_height
        * interface["fin_gross_thickness_m"]
    )
    copper_volume = copper_mass / cage["copper_density_kg_m3"]
    return (
        (gross_volume - copper_volume)
        * moving_core["lamination_factor"]
        * moving_core["density_kg_m3"]
    )


def design_state(
    base: dict,
    search: dict,
    geometry: dict,
    equivalent_field: float,
    base_tooth_field: float,
    base_ligament_field: float,
) -> dict:
    architecture = base["architecture"]
    interface = base["interface"]
    cage = base["passive_cage"]
    magnetic = base["magnetic_circuit"]
    winding = base["winding"]
    fixed = search["fixed"]
    pitch = geometry["cell_pitch_m"]
    cells = geometry["total_cells_per_channel"]
    tooth_width = pitch * fixed["tooth_duty_fraction"]
    slot_width = pitch - tooth_width
    available_slot_area = slot_width * fixed["winding_slot_radial_height_m"]
    conductor_area = (
        fixed["design_gross_slot_fill_fraction"]
        * available_slot_area
        / (winding["coil_sides_per_slot"] * fixed["turns_per_cell"])
    )
    gross_fill = (
        winding["coil_sides_per_slot"]
        * fixed["turns_per_cell"]
        * conductor_area
        / available_slot_area
    )
    mean_turn_length = 2.0 * (pitch + 0.014)
    cell_conductor_length = fixed["turns_per_cell"] * mean_turn_length
    cell_resistance = (
        winding["copper_resistivity_ohm_m"]
        * cell_conductor_length
        / conductor_area
    )
    phase_resistance = (cells // fixed["phase_count"]) * cell_resistance
    primary_copper_volume = (
        architecture["channel_count"]
        * cells
        * cell_conductor_length
        * conductor_area
    )
    primary_copper_mass = primary_copper_volume * winding["copper_density_kg_m3"]
    core_cross_section = interface["active_cage_height_m"] * tooth_width
    core_volume = (
        architecture["channel_count"]
        * cells
        * core_cross_section
        * magnetic["mean_stationary_core_path_length_m"]
    )
    core_mass = core_volume * magnetic["stationary_core_density_kg_m3"]
    tooth_field = equivalent_field / math.sqrt(fixed["tooth_duty_fraction"])
    ligament_field = tooth_field / cage["magnetic_ligament_fraction"]
    return {
        "cell_pitch_m": pitch,
        "tooth_width_m": tooth_width,
        "winding_slot_width_m": slot_width,
        "electrical_wavelength_m": fixed["phase_count"] * pitch,
        "total_cells_per_channel": cells,
        "cells_per_phase": cells // fixed["phase_count"],
        "active_stator_length_m": pitch * cells,
        "equivalent_field_rms_t": equivalent_field,
        "tooth_field_rms_t": tooth_field,
        "magnetic_ligament_field_rms_t": ligament_field,
        "conductor_area_per_turn_m2": conductor_area,
        "available_slot_area_m2": available_slot_area,
        "gross_slot_fill_fraction": gross_fill,
        "mean_turn_length_m": mean_turn_length,
        "cell_resistance_ohm": cell_resistance,
        "phase_resistance_ohm": phase_resistance,
        "primary_copper_mass_kg": primary_copper_mass,
        "stationary_core_mass_kg": core_mass,
        "active_primary_mass_kg": primary_copper_mass + core_mass,
        "base_tooth_field_ratio": tooth_field / base_tooth_field,
        "base_ligament_field_ratio": ligament_field / base_ligament_field,
    }


def magnetic_corner_state(
    base: dict,
    design: dict,
    corner: dict,
    base_tooth_field: float,
    base_ligament_field: float,
) -> dict:
    interface = base["interface"]
    magnetic = base["magnetic_circuit"]
    moving_core = base["moving_magnetic_matrix"]
    winding = base["winding"]
    low_mu_length = interface["fins_per_channel"] * (
        2.0 * corner["clearance_per_side_m"]
        + 2.0 * interface["surface_encapsulant_per_side_m"]
    )
    gap_mmf = design["tooth_field_rms_t"] * low_mu_length / MU_0_H_PER_M
    stationary_mmf = (
        magnetic["conservative_stationary_core_h_at_rated_a_m"]
        * corner["stationary_core_h_multiplier"]
        * (design["tooth_field_rms_t"] / base_tooth_field)
        * magnetic["mean_stationary_core_path_length_m"]
    )
    moving_mmf = (
        moving_core["conservative_h_at_rated_a_m"]
        * (design["magnetic_ligament_field_rms_t"] / base_ligament_field)
        * interface["fins_per_channel"]
        * interface["fin_gross_thickness_m"]
    )
    mmf = gap_mmf + stationary_mmf + moving_mmf
    current = mmf / base["winding"]["turns_per_cell"]
    current_density = current / design["conductor_area_per_turn_m2"]
    pole_area = interface["active_cage_height_m"] * design["tooth_width_m"]
    flux = design["tooth_field_rms_t"] * pole_area
    linkage = (
        design["cells_per_phase"]
        * base["winding"]["turns_per_cell"]
        * flux
    )
    inductance = linkage / current
    return {
        "series_low_permeability_length_m": low_mu_length,
        "gap_mmf_a_turn": gap_mmf,
        "stationary_core_mmf_a_turn": stationary_mmf,
        "moving_matrix_mmf_a_turn": moving_mmf,
        "rated_mmf_a_turn": mmf,
        "rated_phase_current_a": current,
        "rated_primary_current_density_a_m2": current_density,
        "phase_inductance_h": inductance,
    }


def cage_state(
    force_n: float,
    field_t: float,
    conductance_s: float,
    active_area_m2: float,
    equivalent_thickness_m: float,
) -> dict:
    if force_n <= 1e-12 or field_t <= 0.0:
        return {
            "slip_speed_m_s": 0.0,
            "field_at_cage_rms_t": 0.0,
            "bar_current_density_a_m2": 0.0,
            "cage_loss_w": 0.0,
        }
    force_density = force_n / active_area_m2
    slip = low_slip_solution(force_density, conductance_s, field_t)
    reaction = 0.5 * MU_0_H_PER_M * conductance_s * slip
    field_at_cage = field_t / math.sqrt(1.0 + reaction**2)
    surface_current = conductance_s * slip * field_at_cage
    return {
        "slip_speed_m_s": slip,
        "field_at_cage_rms_t": field_at_cage,
        "bar_current_density_a_m2": surface_current / equivalent_thickness_m,
        "cage_loss_w": force_n * slip,
    }


def frequency_power_integral(
    slip_m_s: float,
    exit_velocity_m_s: float,
    acceleration_m_s2: float,
    wavelength_m: float,
    exponent: float,
) -> float:
    return (
        (exit_velocity_m_s + slip_m_s) ** (exponent + 1.0)
        - slip_m_s ** (exponent + 1.0)
    ) / (
        acceleration_m_s2
        * (exponent + 1.0)
        * wavelength_m**exponent
    )


def evaluate_case(
    base: dict,
    design: dict,
    magnetic_corner: dict,
    conductance: float,
    bare_payload_mass: float,
    interface_mass: float,
    cage_copper_mass: float,
    magnetic_matrix_mass: float,
    cg_grid: list[float],
) -> dict:
    architecture = base["architecture"]
    interface = base["interface"]
    cage = base["passive_cage"]
    moving_core = base["moving_magnetic_matrix"]
    magnetic = base["magnetic_circuit"]
    winding = base["winding"]
    drive = base["drive"]
    channels = architecture["channel_count"]
    phases = architecture["phase_count"]
    active_area = (
        interface["fins_per_channel"]
        * interface["active_cage_height_m"]
        * interface["active_length_m"]
    )
    moving_mass = bare_payload_mass + interface_mass
    acceleration = drive["acceleration_g"] * GRAVITY_M_S2
    total_force = moving_mass * acceleration
    exit_velocity = math.sqrt(2.0 * acceleration * drive["powered_length_m"])
    stroke_time = exit_velocity / acceleration
    mechanical_energy = total_force * drive["powered_length_m"]
    cage_mass_per_channel = cage_copper_mass / channels

    metric_modes = {
        "maximum_source_energy_j": "max",
        "minimum_source_to_payload_efficiency": "min",
        "maximum_peak_dc_power_w": "max",
        "maximum_required_dc_link_v": "max",
        "maximum_primary_copper_rise_k": "max",
        "maximum_cage_copper_rise_k": "max",
        "maximum_cage_current_density_a_m2": "max",
        "maximum_cage_slip_m_s": "max",
        "minimum_secondary_only_efficiency": "min",
        "maximum_terminal_frequency_hz": "max",
    }
    metrics = {
        key: (-math.inf if mode == "max" else math.inf)
        for key, mode in metric_modes.items()
    }
    locations = {}
    for y_cg in cg_grid:
        for z_cg in cg_grid:
            forces = cardinal_forces(
                total_force,
                y_cg,
                z_cg,
                interface["force_line_radius_m"],
            )
            cage_energy = 0.0
            primary_copper_energy = 0.0
            stationary_core_energy = 0.0
            moving_core_energy = 0.0
            peak_nonmechanical_power = 0.0
            maximum_required_dc_link = 0.0
            maximum_cage_rise = 0.0
            maximum_cage_j = 0.0
            maximum_slip = 0.0
            maximum_frequency = 0.0
            for force in forces.values():
                field = design["equivalent_field_rms_t"] * math.sqrt(
                    max(0.0, force) / drive["rated_channel_force_n"]
                )
                field = min(field, design["equivalent_field_rms_t"])
                ratio = field / design["equivalent_field_rms_t"] if field else 0.0
                current = magnetic_corner["rated_phase_current_a"] * ratio
                state = cage_state(
                    force,
                    field,
                    conductance,
                    active_area,
                    cage["equivalent_copper_sheet_thickness_m"],
                )
                slip = state["slip_speed_m_s"]
                cage_channel_energy = state["cage_loss_w"] * stroke_time
                cage_energy += cage_channel_energy
                channel_copper_power = (
                    phases * current**2 * design["phase_resistance_ohm"]
                )
                primary_copper_energy += channel_copper_power * stroke_time
                freq_integral = frequency_power_integral(
                    slip,
                    exit_velocity,
                    acceleration,
                    design["electrical_wavelength_m"],
                    magnetic["loss_frequency_exponent"],
                )
                stationary_specific_scale = (
                    (design["tooth_field_rms_t"] * ratio)
                    / (base["magnetic_circuit"]["rated_equivalent_sheet_field_rms_t"]
                       / math.sqrt(base["architecture"]["tooth_duty_fraction"]))
                ) ** magnetic["loss_flux_exponent"]
                moving_specific_scale = (
                    (design["magnetic_ligament_field_rms_t"] * ratio)
                    / (
                        base["magnetic_circuit"]["rated_equivalent_sheet_field_rms_t"]
                        / math.sqrt(base["architecture"]["tooth_duty_fraction"])
                        / cage["magnetic_ligament_fraction"]
                    )
                ) ** moving_core["loss_flux_exponent"]
                stationary_channel_energy = (
                    magnetic["stationary_specific_loss_at_rated_w_kg"]
                    * stationary_specific_scale
                    * (design["stationary_core_mass_kg"] / channels)
                    * freq_integral
                    / magnetic["loss_reference_frequency_hz"]
                    ** magnetic["loss_frequency_exponent"]
                )
                moving_channel_energy = (
                    moving_core["conservative_specific_loss_at_rated_w_kg"]
                    * moving_specific_scale
                    * (magnetic_matrix_mass / channels)
                    * freq_integral
                    / moving_core["loss_reference_frequency_hz"]
                    ** moving_core["loss_frequency_exponent"]
                )
                stationary_core_energy += stationary_channel_energy
                moving_core_energy += moving_channel_energy
                terminal_frequency = (exit_velocity + slip) / design[
                    "electrical_wavelength_m"
                ]
                stationary_core_power_end = (
                    magnetic["stationary_specific_loss_at_rated_w_kg"]
                    * stationary_specific_scale
                    * (terminal_frequency / magnetic["loss_reference_frequency_hz"])
                    ** magnetic["loss_frequency_exponent"]
                    * (design["stationary_core_mass_kg"] / channels)
                )
                moving_core_power_end = (
                    moving_core["conservative_specific_loss_at_rated_w_kg"]
                    * moving_specific_scale
                    * (
                        terminal_frequency
                        / moving_core["loss_reference_frequency_hz"]
                    )
                    ** moving_core["loss_frequency_exponent"]
                    * (magnetic_matrix_mass / channels)
                )
                peak_nonmechanical_power += (
                    state["cage_loss_w"]
                    + channel_copper_power
                    + stationary_core_power_end
                    + moving_core_power_end
                )
                if current > 0.0:
                    airgap_power = force * (exit_velocity + slip)
                    real_load_resistance = (
                        airgap_power
                        + stationary_core_power_end
                        + moving_core_power_end
                    ) / (phases * current**2)
                    phase_voltage = current * math.hypot(
                        design["phase_resistance_ohm"] + real_load_resistance,
                        2.0
                        * math.pi
                        * terminal_frequency
                        * magnetic_corner["phase_inductance_h"],
                    )
                    required_dc = (
                        math.sqrt(6.0)
                        * phase_voltage
                        / drive["space_vector_modulation_utilisation"]
                    )
                    maximum_required_dc_link = max(
                        maximum_required_dc_link, required_dc
                    )
                maximum_cage_rise = max(
                    maximum_cage_rise,
                    cage_channel_energy
                    / (cage_mass_per_channel * cage["copper_specific_heat_j_kg_k"]),
                )
                maximum_cage_j = max(
                    maximum_cage_j, state["bar_current_density_a_m2"]
                )
                maximum_slip = max(maximum_slip, slip)
                maximum_frequency = max(maximum_frequency, terminal_frequency)

            source_energy = (
                mechanical_energy
                + cage_energy
                + primary_copper_energy
                + stationary_core_energy
                + moving_core_energy
            ) / drive["inverter_efficiency"]
            source_efficiency = mechanical_energy / source_energy
            peak_dc_power = (
                total_force * exit_velocity + peak_nonmechanical_power
            ) / drive["inverter_efficiency"]
            primary_rise = primary_copper_energy / (
                design["primary_copper_mass_kg"]
                * winding["copper_specific_heat_j_kg_k"]
            )
            secondary_efficiency = mechanical_energy / (
                mechanical_energy + cage_energy
            )
            values = {
                "maximum_source_energy_j": source_energy,
                "minimum_source_to_payload_efficiency": source_efficiency,
                "maximum_peak_dc_power_w": peak_dc_power,
                "maximum_required_dc_link_v": maximum_required_dc_link,
                "maximum_primary_copper_rise_k": primary_rise,
                "maximum_cage_copper_rise_k": maximum_cage_rise,
                "maximum_cage_current_density_a_m2": maximum_cage_j,
                "maximum_cage_slip_m_s": maximum_slip,
                "minimum_secondary_only_efficiency": secondary_efficiency,
                "maximum_terminal_frequency_hz": maximum_frequency,
            }
            for key, value in values.items():
                mode = metric_modes[key]
                better = value > metrics[key] if mode == "max" else value < metrics[key]
                if better:
                    metrics[key] = value
                    locations[key] = [y_cg, z_cg]

    return {
        "bare_payload_mass_kg": bare_payload_mass,
        "moving_mass_kg": moving_mass,
        "mechanical_energy_j": mechanical_energy,
        **metrics,
        "worst_metric_locations_yz_m": locations,
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
