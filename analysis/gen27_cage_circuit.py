"""Bolley A7c: reclose my selected Fluxrelay point from the fresh A6h field."""

from __future__ import annotations

import argparse
import copy
import csv
import gzip
import hashlib
import io
import itertools
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from fluxbridge_optimization import cage_state, compact_case, evaluate_case
from gen25_cage_circuit import load_inherited


BASE_INPUT = ROOT / "cad" / "fluxbridge_parameters.json"
FIELD_PARAMETERS = ROOT / "cad" / "gen27_field_parameters.json"
FIELD_RESULT = RESULTS / "gen27_field.json"
A8B_RESULT = RESULTS / "gen27_codesign.json"
INPUT = ROOT / "cad" / "gen27_cage_parameters.json"
OUTPUT = RESULTS / "gen27_cage_circuit.json"
POINTS_OUTPUT = RESULTS / "gen27_cage_circuit_points.csv.gz"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def shared_bands(selected: dict, field: dict, control: dict) -> dict:
    fixed = control["fixed"]
    limits = control["bands"]
    design = selected["design"]
    interface = selected["interface"]
    rated = selected["rated"]
    extrema = field["physics_band_extrema"]
    return {
        "a6h_field_pass": field["screen_pass"],
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
        "solved_mean_field_low": extrema["minimum_mean_tooth_slice_field_rms_t"]
        >= limits["minimum_predicted_mean_tooth_field_rms_t"],
        "solved_mean_field_high": extrema["maximum_mean_tooth_slice_field_rms_t"]
        <= limits["maximum_predicted_mean_tooth_field_rms_t"],
        "solved_moving_material_peak": extrema[
            "maximum_inferred_magnetic_ligament_field_t"
        ]
        <= limits["maximum_predicted_moving_material_field_t"],
        "solved_stationary_core_peak": extrema["maximum_stationary_core_field_t"]
        <= limits["maximum_predicted_stationary_core_field_t"],
    }


def circuit_bands(
    reference: dict,
    qualification: dict,
    maximum_voltage: float,
    dc_margin: float,
    normal_residual: float,
    limits: dict,
) -> dict:
    return {
        "required_dc_link": maximum_voltage <= limits["maximum_required_dc_link_v"],
        "dc_link_margin": dc_margin >= limits["minimum_margin_on_48v_link_fraction"],
        "reference_source_energy": reference["maximum_source_energy_j"]
        <= limits["maximum_reference_source_energy_j"],
        "qualification_source_energy": qualification["maximum_source_energy_j"]
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


def calculate() -> dict:
    base = load(BASE_INPUT)
    field_parameters = load_inherited(FIELD_PARAMETERS)
    field = load(FIELD_RESULT)
    a8b = load(A8B_RESULT)
    control = load_inherited(INPUT)
    limits = control["bands"]
    fixed = control["fixed"]
    selected = copy.deepcopy(a8b["selected_candidate"])

    if selected["candidate_id"] != control["selected_candidate_id"]:
        raise SystemExit("A7c selected-candidate identity no longer matches A8b")
    if not selected["feasible"] or not a8b["screen_pass"]:
        raise SystemExit("A7c requires the passing A8b selected point")
    if not field["screen_pass"] or field["band_pass_count"] != field["band_count"]:
        raise SystemExit("A7c requires a passing A6h field result")

    base = copy.deepcopy(base)
    base["interface"]["fins_per_channel"] = fixed["blades_per_face"]
    base["interface"]["active_cage_height_m"] = fixed["active_cage_height_m"]
    base["interface"]["active_length_m"] = selected["interface"][
        "active_cage_length_m"
    ]
    base["interface"]["fin_gross_thickness_m"] = (
        field_parameters["interface_accounting"]["magnetic_blade_active_width_mm"]
        * 1e-3
    )
    base["passive_cage"]["equivalent_copper_sheet_thickness_m"] = control[
        "model"
    ]["equivalent_copper_sheet_thickness_m"]
    base["passive_cage"]["magnetic_ligament_fraction"] = field_parameters[
        "geometry"
    ]["magnetic_ligament_axial_fraction"]

    extrema = field["physics_band_extrema"]
    sectional = field["sectional_drive"]
    tooth_field = extrema["minimum_mean_tooth_slice_field_rms_t"]
    equivalent_field = tooth_field * math.sqrt(fixed["tooth_duty_fraction"])
    moving_peak = extrema["maximum_inferred_magnetic_ligament_field_t"]
    stationary_peak = extrema["maximum_stationary_core_field_t"]
    phase_inductance = sectional["fine_active_window_phase_inductance_h"]

    selected["design"].update(
        {
            "equivalent_field_rms_t": equivalent_field,
            "tooth_field_rms_t": tooth_field,
            "magnetic_ligament_field_rms_t": moving_peak,
        }
    )
    selected["sectional"]["phase_inductance_h"] = phase_inductance
    selected["field_solution"] = {
        "minimum_mean_tooth_field_rms_t": tooth_field,
        "maximum_mean_tooth_field_rms_t": extrema[
            "maximum_mean_tooth_slice_field_rms_t"
        ],
        "maximum_moving_material_peak_t": moving_peak,
        "maximum_stationary_core_peak_t": stationary_peak,
    }

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
    magnetic = {
        "rated_mmf_a_turn": selected["rated"]["ampere_turn_rms"],
        "rated_phase_current_a": selected["rated"]["phase_current_rms_a"],
        "rated_primary_current_density_a_m2": selected["rated"][
            "primary_current_density_a_m2"
        ],
        "phase_inductance_h": phase_inductance,
    }
    common = {name: bool(value) for name, value in shared_bands(selected, field, control).items()}
    corners = []
    for conductance_multiplier, resistance_multiplier in itertools.product(
        control["robustness_corners"]["cage_sheet_conductance_multiplier"],
        control["robustness_corners"]["phase_resistance_multiplier"],
    ):
        design = copy.deepcopy(selected["design"])
        design["phase_resistance_ohm"] *= resistance_multiplier
        design["cell_resistance_ohm"] *= resistance_multiplier
        conductance = nominal_conductance * conductance_multiplier
        reference = evaluate_case(
            base,
            design,
            magnetic,
            conductance,
            base["interface"]["bare_payload_reference_mass_kg"],
            selected["interface"]["total_increment_kg"],
            selected["interface"]["cage_copper_mass_kg"],
            selected["interface"]["magnetic_matrix_mass_kg"],
            cg_grid,
            retain_point_records=True,
        )
        qualification = evaluate_case(
            base,
            design,
            magnetic,
            conductance,
            base["interface"]["bare_payload_qualification_mass_kg"],
            selected["interface"]["total_increment_kg"],
            selected["interface"]["cage_copper_mass_kg"],
            selected["interface"]["magnetic_matrix_mass_kg"],
            cg_grid,
            retain_point_records=True,
        )
        rated_cage = cage_state(
            base["drive"]["rated_channel_force_n"],
            equivalent_field,
            conductance,
            fixed["blades_per_face"]
            * fixed["active_cage_height_m"]
            * selected["interface"]["active_cage_length_m"],
            base["passive_cage"]["equivalent_copper_sheet_thickness_m"],
        )
        mismatch = base["drive"]["side_to_side_field_amplitude_mismatch_fraction"]
        plus_field = rated_cage["field_at_cage_rms_t"] * (1.0 + 0.5 * mismatch)
        minus_field = rated_cage["field_at_cage_rms_t"] * (1.0 - 0.5 * mismatch)
        active_area = (
            fixed["blades_per_face"]
            * fixed["active_cage_height_m"]
            * selected["interface"]["active_cage_length_m"]
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
        dc_margin = base["drive"]["nominal_dc_link_v"] / maximum_voltage - 1.0
        bands = dict(common)
        bands.update(
            {
                name: bool(value)
                for name, value in circuit_bands(
                    reference,
                    qualification,
                    maximum_voltage,
                    dc_margin,
                    normal_residual,
                    limits,
                ).items()
            }
        )
        corners.append(
            {
                "corner": {
                    "cage_sheet_conductance_multiplier": conductance_multiplier,
                    "phase_resistance_multiplier": resistance_multiplier,
                },
                "cage_sheet_conductance_s": conductance,
                "phase_resistance_ohm": design["phase_resistance_ohm"],
                "maximum_required_dc_link_v": maximum_voltage,
                "dc_link_margin_fraction": dc_margin,
                "unbalanced_normal_force_n": normal_residual,
                "reference": compact_case(reference),
                "qualification": compact_case(qualification),
                "bands": bands,
                "band_pass_count": sum(bands.values()),
                "band_count": len(bands),
                "failed_bands": [name for name, passed in bands.items() if not passed],
                "pass": all(bands.values()),
            }
        )

    failed_union = sorted(
        {name for corner in corners for name in corner["failed_bands"]}
    )
    preferences = control["preferences"]
    return {
        "evidence": "A7c SELECTED-POINT POST-FIELD HOMOGENIZED CAGE + LUMPED SECTIONAL CIRCUIT/CG SHOT MODEL",
        "input_file": str(INPUT.relative_to(ROOT)),
        "source_files": control["source_files"],
        "selected_candidate_id": selected["candidate_id"],
        "field_trace": {
            "minimum_three_mesh_tooth_field_rms_t": tooth_field,
            "maximum_three_mesh_tooth_field_rms_t": extrema[
                "maximum_mean_tooth_slice_field_rms_t"
            ],
            "equivalent_sheet_field_rms_t": equivalent_field,
            "maximum_three_mesh_moving_material_field_t": moving_peak,
            "maximum_three_mesh_stationary_core_field_t": stationary_peak,
            "fine_active_window_phase_inductance_h": phase_inductance,
        },
        "design": selected["design"],
        "rated": {
            **selected["rated"],
            "nominal_cage_sheet_conductance_s": nominal_conductance,
        },
        "interface": selected["interface"],
        "sectional": selected["sectional"],
        "preference_results": {
            "target_interface_mass": selected["interface"]["total_increment_kg"]
            <= preferences["target_interface_mass_kg"],
            "preferred_interface_mass": selected["interface"]["total_increment_kg"]
            <= preferences["preferred_interface_mass_kg"],
        },
        "cg_points_per_case": len(cg_grid) ** 2,
        "corner_count": len(corners),
        "corners": corners,
        "corner_band_order": sorted(corners[0]["bands"]),
        "band_count": corners[0]["band_count"],
        "minimum_corner_band_pass_count": min(
            corner["band_pass_count"] for corner in corners
        ),
        "failed_band_union": failed_union,
        "screen_pass": all(corner["pass"] for corner in corners),
        "disposition": (
            "PROMOTE_SELECTED_GEN27_FLUXRELAY_TO_GEN3_CAD_AND_TRANSIENT_SECTIONAL_DRIVE"
            if all(corner["pass"] for corner in corners)
            else "DO_NOT_PROMOTE_SELECTED_GEN27_FLUXRELAY_CAGE_CIRCUIT_POINT"
        ),
        "limits": [
            "The cage remains a homogenized equivalent sheet; discrete rungs, end buses and current crowding are absent.",
            "The shot model is quasi-steady and assumes prebias; switching, end effects, force ripple and six-degree-of-freedom motion are absent.",
            "A6h supplies fresh transverse field and fine active-window inductance; it does not supply transient force or axial handoff evidence.",
            "Installed active mass excludes structure, cooling, containment, wiring and power electronics.",
        ],
    }


def package_points(result: dict) -> tuple[bytes, int]:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    metric_columns = [
        "y_cg_m",
        "z_cg_m",
        "maximum_source_energy_j",
        "minimum_source_to_payload_efficiency",
        "maximum_peak_dc_power_w",
        "maximum_required_dc_link_v",
        "maximum_primary_copper_rise_k",
        "maximum_cage_copper_rise_k",
        "maximum_cage_current_density_a_m2",
        "maximum_cage_slip_m_s",
        "minimum_secondary_only_efficiency",
        "maximum_terminal_frequency_hz",
    ]
    writer.writerow(
        [
            "corner_index",
            "cage_sheet_conductance_multiplier",
            "phase_resistance_multiplier",
            "payload_case",
            *metric_columns,
        ]
    )
    record_count = 0
    for corner_index, corner in enumerate(result["corners"], start=1):
        for case_name in ("reference", "qualification"):
            records = corner[case_name].pop("cg_point_records")
            for record in records:
                writer.writerow(
                    [
                        corner_index,
                        corner["corner"]["cage_sheet_conductance_multiplier"],
                        corner["corner"]["phase_resistance_multiplier"],
                        case_name,
                        *(record[column] for column in metric_columns),
                    ]
                )
                record_count += 1
    payload = gzip.compress(stream.getvalue().encode("utf-8"), compresslevel=9, mtime=0)
    return payload, record_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = calculate()
    points, point_count = package_points(result)
    result["cg_point_artifact"] = {
        "path": str(POINTS_OUTPUT.relative_to(ROOT)),
        "compression": "deterministic gzip CSV, mtime=0",
        "record_count": point_count,
        "bytes": len(points),
        "sha256": hashlib.sha256(points).hexdigest(),
    }
    if args.write:
        POINTS_OUTPUT.write_bytes(points)
        dump_json(OUTPUT, result)
    elif args.check:
        if not POINTS_OUTPUT.exists() or POINTS_OUTPUT.read_bytes() != points:
            raise SystemExit("stale A7c CG-point artifact")
        compare_json(OUTPUT, result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
