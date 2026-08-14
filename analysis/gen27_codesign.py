"""Bolley A8b: Gen2.7 Fluxrelay axial, winding and cage/circuit co-design."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from fluxbridge_optimization import cage_state, compact_case, evaluate_case
from gen25_cage_circuit import load_inherited


BASE_INPUT = ROOT / "cad" / "fluxbridge_parameters.json"
FIELD_PARAMETERS = ROOT / "cad" / "gen26_field_parameters.json"
FIELD_RESULT = RESULTS / "gen26_field.json"
A7B_RESULT = RESULTS / "gen26_cage_circuit.json"
INPUT = ROOT / "cad" / "gen27_codesign_parameters.json"
OUTPUT = RESULTS / "gen27_codesign.json"
CANDIDATES_OUTPUT = RESULTS / "gen27_codesign_candidates.json.gz"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def maximum_intersected_cells(active_length: float, pitch: float) -> int:
    return math.ceil(active_length / pitch - 1e-12) + 1


def upper_demand(value: float, limit: float) -> float:
    return value / limit


def lower_demand(value: float, limit: float) -> float:
    return limit / value if value > 0.0 else math.inf


def candidate_geometry(
    base: dict,
    field: dict,
    a7b: dict,
    control: dict,
    total_cells: int,
    pitch: float,
    current: float,
    conductor_area_mm2: float,
) -> dict:
    fixed = control["fixed"]
    phases = fixed["phase_count"]
    turns = fixed["turns_per_cell"]
    stator_length = total_cells * pitch
    cage_length = (
        stator_length
        - fixed["powered_travel_m"]
        - fixed["active_cage_start_x_m"]
        - fixed["minimum_end_overlap_guard_m"]
    )
    active_cells = (
        maximum_intersected_cells(cage_length, pitch) if cage_length > 0.0 else 0
    )
    active_cells_per_phase = math.ceil(active_cells / phases) if active_cells else 0
    area = conductor_area_mm2 * 1e-6
    slot_width = pitch * (1.0 - fixed["tooth_duty_fraction"])
    available_slot_area = slot_width * fixed["winding_radial_height_m"]
    gross_fill = (
        2.0 * turns * area / available_slot_area if available_slot_area > 0.0 else math.inf
    )
    mean_turn_length = 2.0 * (
        pitch + fixed["mean_turn_transverse_allowance_m"]
    )
    cell_conductor_length = turns * mean_turn_length
    cell_resistance = (
        base["winding"]["copper_resistivity_ohm_m"]
        * cell_conductor_length
        / area
    )
    active_phase_resistance = active_cells_per_phase * cell_resistance
    installed_copper_volume = (
        base["architecture"]["channel_count"]
        * total_cells
        * cell_conductor_length
        * area
    )
    installed_copper_mass = (
        installed_copper_volume * base["winding"]["copper_density_kg_m3"]
    )
    energized_cell_equivalents = phases * active_cells_per_phase
    energized_copper_mass = (
        installed_copper_mass * energized_cell_equivalents / total_cells
    )
    installed_core_mass = (
        a7b["design"]["stationary_core_mass_kg"]
        * stator_length
        / a7b["design"]["active_stator_length_m"]
    )
    energized_core_mass = (
        installed_core_mass * energized_cell_equivalents / total_cells
    )
    installed_primary_mass = installed_copper_mass + installed_core_mass

    # Material scales with active cage length; the five-blade capture allowance stays fixed.
    gen26_length = fixed["gen26_active_cage_length_m"]
    length_ratio = cage_length / gen26_length
    cage_copper_mass = a7b["interface"]["cage_copper_kg"] * length_ratio
    magnetic_matrix_mass = a7b["interface"]["magnetic_matrix_kg"] * length_ratio
    interface_mass = (
        cage_copper_mass
        + magnetic_matrix_mass
        + fixed["capture_and_encapsulation_allowance_kg"]
    )

    current_ratio = current / a7b["rated"]["phase_current_rms_a"]
    minimum_mean_field = (
        field["physics_band_extrema"]["minimum_mean_tooth_slice_field_rms_t"]
        * current_ratio
    )
    maximum_mean_field = (
        field["physics_band_extrema"]["maximum_mean_tooth_slice_field_rms_t"]
        * current_ratio
    )
    equivalent_field = a7b["design"]["equivalent_field_rms_t"] * current_ratio
    tooth_field = a7b["design"]["tooth_field_rms_t"] * current_ratio
    moving_peak = (
        field["physics_band_extrema"]["maximum_inferred_magnetic_ligament_field_t"]
        * current_ratio
    )
    stationary_peak = (
        field["physics_band_extrema"]["maximum_stationary_core_field_t"]
        * current_ratio
    )
    phase_inductance = (
        a7b["field_trace"]["maximum_three_mesh_phase_inductance_h"]
        * active_cells_per_phase
        / a7b["design"]["cells_per_phase"]
        * pitch
        / a7b["design"]["cell_pitch_m"]
    )
    design = copy.deepcopy(a7b["design"])
    design.update(
        {
            "cell_pitch_m": pitch,
            "tooth_width_m": pitch * fixed["tooth_duty_fraction"],
            "winding_slot_width_m": slot_width,
            "electrical_wavelength_m": phases * pitch,
            "total_cells_per_channel": total_cells,
            "cells_per_phase": total_cells // phases,
            "simultaneously_energized_cells_per_phase": active_cells_per_phase,
            "active_stator_length_m": stator_length,
            "active_cage_length_m": cage_length,
            "equivalent_field_rms_t": equivalent_field,
            "tooth_field_rms_t": tooth_field,
            "magnetic_ligament_field_rms_t": moving_peak,
            "conductor_area_per_turn_m2": area,
            "available_slot_area_m2": available_slot_area,
            "gross_slot_fill_fraction": gross_fill,
            "mean_turn_length_m": mean_turn_length,
            "cell_resistance_ohm": cell_resistance,
            "phase_resistance_ohm": active_phase_resistance,
            "installed_primary_copper_mass_kg": installed_copper_mass,
            "installed_stationary_core_mass_kg": installed_core_mass,
            "installed_active_primary_mass_kg": installed_primary_mass,
            "primary_copper_mass_kg": energized_copper_mass,
            "stationary_core_mass_kg": energized_core_mass,
            "active_primary_mass_kg": installed_primary_mass,
        }
    )
    return {
        "candidate_id": (
            f"n{total_cells}_p{pitch * 1e3:.1f}_"
            f"I{current:.0f}_A{conductor_area_mm2:.1f}"
        ),
        "design": design,
        "interface": {
            "active_cage_start_x_m": fixed["active_cage_start_x_m"],
            "active_cage_length_m": cage_length,
            "end_overlap_guard_m": (
                stator_length
                - fixed["powered_travel_m"]
                - fixed["active_cage_start_x_m"]
                - cage_length
            ),
            "cage_copper_mass_kg": cage_copper_mass,
            "magnetic_matrix_mass_kg": magnetic_matrix_mass,
            "total_increment_kg": interface_mass,
        },
        "sectional": {
            "maximum_intersected_cells": active_cells,
            "simultaneously_energized_cells_per_phase": active_cells_per_phase,
            "energized_cell_equivalents": energized_cell_equivalents,
            "phase_resistance_ratio_to_a7b": (
                active_phase_resistance / a7b["design"]["phase_resistance_ohm"]
            ),
            "phase_inductance_h": phase_inductance,
            "phase_inductance_ratio_to_a7b": (
                phase_inductance
                / a7b["field_trace"]["maximum_three_mesh_phase_inductance_h"]
            ),
        },
        "rated": {
            "phase_current_rms_a": current,
            "ampere_turn_rms": turns * current,
            "primary_current_density_a_m2": current / area,
        },
        "field_surrogate": {
            "minimum_predicted_mean_tooth_field_rms_t": minimum_mean_field,
            "maximum_predicted_mean_tooth_field_rms_t": maximum_mean_field,
            "predicted_moving_material_peak_t": moving_peak,
            "predicted_stationary_core_peak_t": stationary_peak,
            "current_scaling_ratio_to_a6g": current_ratio,
        },
    }


def precheck(record: dict, control: dict, field: dict) -> dict:
    fixed = control["fixed"]
    limits = control["bands"]
    design = record["design"]
    interface = record["interface"]
    rated = record["rated"]
    surrogate = record["field_surrogate"]
    return {
        "a6g_transverse_topology": bool(field["screen_pass"]),
        "positive_cage_length": interface["active_cage_length_m"]
        >= limits["minimum_active_cage_length_m"],
        "maximum_cage_length": interface["active_cage_length_m"]
        <= limits["maximum_active_cage_length_m"],
        "cage_inside_payload": (
            interface["active_cage_start_x_m"] + interface["active_cage_length_m"]
            <= fixed["payload_length_m"]
        ),
        "full_overlap_guard": interface["end_overlap_guard_m"]
        >= fixed["minimum_end_overlap_guard_m"] - 1e-12,
        "three_phase_cell_count": design["total_cells_per_channel"]
        % fixed["phase_count"]
        == 0,
        "interface_mass_absolute": interface["total_increment_kg"]
        <= limits["maximum_interface_mass_kg"],
        "installed_active_primary_mass": design["installed_active_primary_mass_kg"]
        <= limits["maximum_installed_active_primary_mass_kg"],
        "rated_phase_current": rated["phase_current_rms_a"]
        <= limits["maximum_rated_phase_current_a"],
        "rated_mmf": rated["ampere_turn_rms"]
        <= limits["maximum_rated_mmf_a_turn"],
        "primary_current_density": rated["primary_current_density_a_m2"]
        <= limits["maximum_primary_current_density_a_m2"],
        "winding_slot_fill": design["gross_slot_fill_fraction"]
        <= limits["maximum_winding_slot_fill_fraction"],
        "predicted_mean_field_low": surrogate[
            "minimum_predicted_mean_tooth_field_rms_t"
        ]
        >= limits["minimum_predicted_mean_tooth_field_rms_t"],
        "predicted_mean_field_high": surrogate[
            "maximum_predicted_mean_tooth_field_rms_t"
        ]
        <= limits["maximum_predicted_mean_tooth_field_rms_t"],
        "predicted_moving_material_peak": surrogate[
            "predicted_moving_material_peak_t"
        ]
        <= limits["maximum_predicted_moving_material_field_t"],
        "predicted_stationary_core_peak": surrogate[
            "predicted_stationary_core_peak_t"
        ]
        <= limits["maximum_predicted_stationary_core_field_t"],
    }


def continuous_demands(
    record: dict,
    control: dict,
    corners: list[dict] | None = None,
) -> dict:
    limits = control["bands"]
    design = record["design"]
    interface = record["interface"]
    rated = record["rated"]
    surrogate = record["field_surrogate"]
    demands = {
        "interface_mass_absolute": upper_demand(
            interface["total_increment_kg"], limits["maximum_interface_mass_kg"]
        ),
        "installed_active_primary_mass": upper_demand(
            design["installed_active_primary_mass_kg"],
            limits["maximum_installed_active_primary_mass_kg"],
        ),
        "rated_phase_current": upper_demand(
            rated["phase_current_rms_a"], limits["maximum_rated_phase_current_a"]
        ),
        "rated_mmf": upper_demand(
            rated["ampere_turn_rms"], limits["maximum_rated_mmf_a_turn"]
        ),
        "primary_current_density": upper_demand(
            rated["primary_current_density_a_m2"],
            limits["maximum_primary_current_density_a_m2"],
        ),
        "winding_slot_fill": upper_demand(
            design["gross_slot_fill_fraction"],
            limits["maximum_winding_slot_fill_fraction"],
        ),
        "predicted_mean_field_low": lower_demand(
            surrogate["minimum_predicted_mean_tooth_field_rms_t"],
            limits["minimum_predicted_mean_tooth_field_rms_t"],
        ),
        "predicted_mean_field_high": upper_demand(
            surrogate["maximum_predicted_mean_tooth_field_rms_t"],
            limits["maximum_predicted_mean_tooth_field_rms_t"],
        ),
        "predicted_moving_material_peak": upper_demand(
            surrogate["predicted_moving_material_peak_t"],
            limits["maximum_predicted_moving_material_field_t"],
        ),
        "predicted_stationary_core_peak": upper_demand(
            surrogate["predicted_stationary_core_peak_t"],
            limits["maximum_predicted_stationary_core_field_t"],
        ),
    }
    if corners:
        worst_reference = max(
            corner["reference"]["maximum_source_energy_j"] for corner in corners
        )
        worst_qualification = max(
            corner["qualification"]["maximum_source_energy_j"] for corner in corners
        )
        maximum_voltage = max(corner["maximum_required_dc_link_v"] for corner in corners)
        dc_margin = 48.0 / maximum_voltage - 1.0
        demands.update(
            {
                "required_dc_link": upper_demand(
                    maximum_voltage, limits["maximum_required_dc_link_v"]
                ),
                "dc_link_margin": lower_demand(
                    dc_margin, limits["minimum_margin_on_48v_link_fraction"]
                ),
                "reference_source_energy": upper_demand(
                    worst_reference, limits["maximum_reference_source_energy_j"]
                ),
                "qualification_source_energy": upper_demand(
                    worst_qualification,
                    limits["maximum_qualification_source_energy_j"],
                ),
                "source_efficiency": lower_demand(
                    min(
                        corner[case]["minimum_source_to_payload_efficiency"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["minimum_source_to_payload_efficiency"],
                ),
                "peak_dc_power": upper_demand(
                    max(
                        corner[case]["maximum_peak_dc_power_w"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["maximum_peak_dc_power_w"],
                ),
                "primary_copper_rise": upper_demand(
                    max(
                        corner[case]["maximum_primary_copper_rise_k"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["maximum_primary_copper_rise_per_shot_k"],
                ),
                "cage_copper_rise": upper_demand(
                    max(
                        corner[case]["maximum_cage_copper_rise_k"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["maximum_cage_copper_rise_per_shot_k"],
                ),
                "cage_current_density": upper_demand(
                    max(
                        corner[case]["maximum_cage_current_density_a_m2"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["maximum_cage_current_density_a_m2"],
                ),
                "cage_slip": upper_demand(
                    max(
                        corner[case]["maximum_cage_slip_m_s"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["maximum_required_cage_slip_m_s"],
                ),
                "secondary_efficiency": lower_demand(
                    min(
                        corner[case]["minimum_secondary_only_efficiency"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["minimum_secondary_only_efficiency"],
                ),
                "terminal_frequency": upper_demand(
                    max(
                        corner[case]["maximum_terminal_frequency_hz"]
                        for corner in corners
                        for case in ("reference", "qualification")
                    ),
                    limits["maximum_terminal_frequency_hz"],
                ),
                "unbalanced_normal_force": upper_demand(
                    max(corner["unbalanced_normal_force_n"] for corner in corners),
                    limits["maximum_unbalanced_normal_force_n"],
                ),
            }
        )
    return demands


def calculate() -> dict:
    base = load(BASE_INPUT)
    field_parameters = load_inherited(FIELD_PARAMETERS)
    field = load(FIELD_RESULT)
    a7b = load(A7B_RESULT)
    control = load(INPUT)
    fixed = control["fixed"]
    limits = control["bands"]

    base = copy.deepcopy(base)
    base["interface"]["fins_per_channel"] = fixed["blades_per_face"]
    base["interface"]["active_cage_height_m"] = fixed["active_cage_height_m"]
    base["interface"]["fin_gross_thickness_m"] = (
        field_parameters["interface_accounting"]["magnetic_blade_active_width_mm"]
        * 1e-3
    )
    base["passive_cage"]["equivalent_copper_sheet_thickness_m"] = 0.000345
    base["passive_cage"]["magnetic_ligament_fraction"] = field_parameters[
        "geometry"
    ]["magnetic_ligament_axial_fraction"]

    cg_limit = base["interface"]["transverse_cg_limit_m"]
    points = base["interface"]["cg_grid_points_per_axis"]
    cg_grid = [
        -cg_limit + 2.0 * cg_limit * index / (points - 1)
        for index in range(points)
    ]
    nominal_conductance = (
        base["passive_cage"]["equivalent_copper_sheet_thickness_m"]
        / base["passive_cage"]["copper_resistivity_ohm_m"]
    )

    candidate_records = []
    grid = control["candidate_grid"]
    for total_cells, pitch, current, area_mm2 in itertools.product(
        grid["total_cells_per_face"],
        grid["cell_pitch_m"],
        grid["rated_phase_current_rms_a"],
        grid["conductor_area_per_turn_mm2"],
    ):
        record = candidate_geometry(
            base, field, a7b, control, total_cells, pitch, current, area_mm2
        )
        pre_bands = {name: bool(value) for name, value in precheck(record, control, field).items()}
        record["precheck_bands"] = pre_bands
        record["fully_evaluated"] = all(pre_bands.values())
        record["corners"] = []
        if record["fully_evaluated"]:
            base_candidate = copy.deepcopy(base)
            base_candidate["interface"]["active_length_m"] = record["interface"][
                "active_cage_length_m"
            ]
            magnetic = {
                "rated_mmf_a_turn": record["rated"]["ampere_turn_rms"],
                "rated_phase_current_a": record["rated"]["phase_current_rms_a"],
                "rated_primary_current_density_a_m2": record["rated"][
                    "primary_current_density_a_m2"
                ],
                "phase_inductance_h": record["sectional"]["phase_inductance_h"],
            }
            for conductance_multiplier, resistance_multiplier in itertools.product(
                control["robustness_corners"]["cage_sheet_conductance_multiplier"],
                control["robustness_corners"]["phase_resistance_multiplier"],
            ):
                design = copy.deepcopy(record["design"])
                design["phase_resistance_ohm"] *= resistance_multiplier
                design["cell_resistance_ohm"] *= resistance_multiplier
                conductance = nominal_conductance * conductance_multiplier
                reference = evaluate_case(
                    base_candidate,
                    design,
                    magnetic,
                    conductance,
                    base["interface"]["bare_payload_reference_mass_kg"],
                    record["interface"]["total_increment_kg"],
                    record["interface"]["cage_copper_mass_kg"],
                    record["interface"]["magnetic_matrix_mass_kg"],
                    cg_grid,
                )
                qualification = evaluate_case(
                    base_candidate,
                    design,
                    magnetic,
                    conductance,
                    base["interface"]["bare_payload_qualification_mass_kg"],
                    record["interface"]["total_increment_kg"],
                    record["interface"]["cage_copper_mass_kg"],
                    record["interface"]["magnetic_matrix_mass_kg"],
                    cg_grid,
                )
                rated_cage = cage_state(
                    base["drive"]["rated_channel_force_n"],
                    record["design"]["equivalent_field_rms_t"],
                    conductance,
                    fixed["blades_per_face"]
                    * fixed["active_cage_height_m"]
                    * record["interface"]["active_cage_length_m"],
                    base["passive_cage"]["equivalent_copper_sheet_thickness_m"],
                )
                mismatch = base["drive"][
                    "side_to_side_field_amplitude_mismatch_fraction"
                ]
                plus_field = rated_cage["field_at_cage_rms_t"] * (1.0 + 0.5 * mismatch)
                minus_field = rated_cage["field_at_cage_rms_t"] * (1.0 - 0.5 * mismatch)
                active_area = (
                    fixed["blades_per_face"]
                    * fixed["active_cage_height_m"]
                    * record["interface"]["active_cage_length_m"]
                )
                normal_residual = (
                    (plus_field**2 - minus_field**2)
                    * active_area
                    / (2.0 * MU_0_H_PER_M)
                )
                maximum_voltage = max(
                    reference["maximum_required_dc_link_v"],
                    qualification["maximum_required_dc_link_v"],
                )
                record["corners"].append(
                    {
                        "corner": {
                            "cage_sheet_conductance_multiplier": conductance_multiplier,
                            "phase_resistance_multiplier": resistance_multiplier,
                        },
                        "phase_resistance_ohm": design["phase_resistance_ohm"],
                        "cage_sheet_conductance_s": conductance,
                        "maximum_required_dc_link_v": maximum_voltage,
                        "dc_link_margin_fraction": 48.0 / maximum_voltage - 1.0,
                        "unbalanced_normal_force_n": normal_residual,
                        "reference": compact_case(reference),
                        "qualification": compact_case(qualification),
                    }
                )

        demands = continuous_demands(
            record, control, record["corners"] if record["fully_evaluated"] else None
        )
        all_bands = dict(pre_bands)
        if record["fully_evaluated"]:
            for name, demand in demands.items():
                all_bands[name] = bool(demand <= 1.0 + 1e-12)
        record["bands"] = all_bands
        record["band_pass_count"] = sum(all_bands.values())
        record["band_count"] = len(all_bands)
        record["failed_bands"] = [name for name, passed in all_bands.items() if not passed]
        record["continuous_demand_by_band"] = demands
        record["worst_continuous_demand"] = max(demands.values())
        record["feasible"] = record["fully_evaluated"] and all(all_bands.values())
        if record["corners"]:
            record["worst_reference_source_energy_j"] = max(
                corner["reference"]["maximum_source_energy_j"]
                for corner in record["corners"]
            )
            record["worst_qualification_source_energy_j"] = max(
                corner["qualification"]["maximum_source_energy_j"]
                for corner in record["corners"]
            )
        else:
            record["worst_reference_source_energy_j"] = None
            record["worst_qualification_source_energy_j"] = None
        record["selection_key"] = (
            [
                record["worst_continuous_demand"],
                record["design"]["installed_active_primary_mass_kg"],
                record["worst_reference_source_energy_j"],
                record["candidate_id"],
            ]
            if record["feasible"]
            else None
        )
        candidate_records.append(record)

    feasible = [record for record in candidate_records if record["feasible"]]
    selected = min(feasible, key=lambda record: tuple(record["selection_key"])) if feasible else None
    preferences = control["preferences"]
    return {
        "evidence": "A8b COUPLED AXIAL / SECTIONAL-WINDING / CAGE-CIRCUIT DESIGN-SPACE SEARCH",
        "input_file": str(INPUT.relative_to(ROOT)),
        "source_files": control["source_files"],
        "selection_rule": fixed["selection_rule"],
        "candidate_count": len(candidate_records),
        "fully_evaluated_candidate_count": sum(
            record["fully_evaluated"] for record in candidate_records
        ),
        "feasible_candidate_count": len(feasible),
        "corners_per_evaluated_candidate": 4,
        "cg_points_per_case_per_corner": len(cg_grid) ** 2,
        "selected_candidate_id": selected["candidate_id"] if selected else None,
        "selected_candidate": selected,
        "candidate_records": candidate_records,
        "preference_results": (
            {
                "target_interface_mass": selected["interface"]["total_increment_kg"]
                <= preferences["target_interface_mass_kg"],
                "preferred_interface_mass": selected["interface"]["total_increment_kg"]
                <= preferences["preferred_interface_mass_kg"],
            }
            if selected
            else None
        ),
        "screen_pass": selected is not None,
        "disposition": (
            "FREEZE_GEN27_FLUXRELAY_FOR_FIELD_AND_SELECTED_POINT_RECLOSURE"
            if selected
            else "NO_FEASIBLE_GEN27_FLUXRELAY_POINT"
        ),
        "limits": [
            "A6g transverse fields and peaks are scaled linearly with current; A8b is not a new nonlinear field solve.",
            "Axial force ripple, finite ends and switching transients are absent; active-window phase resistance and inductance use a conservative maximum intersected-cell count.",
            "Only simultaneously energized copper and core contribute pulse loss and temperature; the 16 kg band uses all installed active material.",
            "Capture allowance stays fixed while cage copper and magnetic material scale with active length; structure and manufacturing tolerance remain unproved.",
        ],
    }


def package(result: dict) -> tuple[dict, bytes]:
    summary = copy.deepcopy(result)
    candidates = summary.pop("candidate_records")
    raw = (
        json.dumps(candidates, separators=(",", ":"), sort_keys=True) + "\n"
    ).encode("utf-8")
    compressed = gzip.compress(raw, compresslevel=9, mtime=0)
    summary["candidate_artifact"] = {
        "path": str(CANDIDATES_OUTPUT.relative_to(ROOT)),
        "compression": "deterministic gzip JSON, mtime=0",
        "record_count": len(candidates),
        "uncompressed_bytes": len(raw),
        "bytes": len(compressed),
        "sha256": hashlib.sha256(compressed).hexdigest(),
    }
    return summary, compressed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = calculate()
    if args.write:
        summary, candidates = package(result)
        dump_json(OUTPUT, summary)
        CANDIDATES_OUTPUT.write_bytes(candidates)
    elif args.check:
        summary, candidates = package(result)
        compare_json(OUTPUT, summary)
        if not CANDIDATES_OUTPUT.exists() or CANDIDATES_OUTPUT.read_bytes() != candidates:
            raise SystemExit(
                "stale generated file: analysis/results/gen27_codesign_candidates.json.gz"
            )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
