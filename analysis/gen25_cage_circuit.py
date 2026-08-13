"""Bolley A7a: Gen2.5 post-field homogenized cage/circuit reclosure."""

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


BASE_INPUT = ROOT / "cad" / "fluxbridge_parameters.json"
A3G_INPUT = RESULTS / "fluxbridge_optimization.json"
FIELD_PARAMETERS = ROOT / "cad" / "gen25_field_parameters.json"
FIELD_RESULT = RESULTS / "gen25_field.json"
INPUT = ROOT / "cad" / "gen25_cage_parameters.json"
OUTPUT = RESULTS / "gen25_cage_circuit.json"
POINTS_OUTPUT = RESULTS / "gen25_cage_circuit_points.csv.gz"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    base = load(BASE_INPUT)
    a3g = load(A3G_INPUT)
    field_parameters = load(FIELD_PARAMETERS)
    field = load(FIELD_RESULT)
    control = load(INPUT)
    declared = control["design"]
    limits = control["bands"]

    if not field["screen_pass"] or field["band_pass_count"] != field["band_count"]:
        raise SystemExit("A7a requires a passing A6f field result")

    base = copy.deepcopy(base)
    base["winding"]["turns_per_cell"] = declared["turns_per_cell"]
    base["passive_cage"]["equivalent_copper_sheet_thickness_m"] = declared[
        "equivalent_copper_sheet_thickness_m"
    ]
    base["passive_cage"]["magnetic_ligament_fraction"] = field_parameters[
        "geometry"
    ]["magnetic_ligament_axial_fraction"]
    base["interface"]["fin_gross_thickness_m"] = (
        field_parameters["interface_accounting"]["magnetic_blade_active_width_mm"]
        * 1e-3
    )

    tooth_field = field["physics_band_extrema"][
        "minimum_mean_tooth_slice_field_rms_t"
    ]
    equivalent_field = tooth_field * math.sqrt(
        base["architecture"]["tooth_duty_fraction"]
    )
    magnetic_peak = field["physics_band_extrema"][
        "maximum_inferred_magnetic_ligament_field_t"
    ]
    phase_inductance = max(
        mesh["per_cell_inductance_h"] for mesh in field["mesh_results"].values()
    ) * declared["cells_per_phase"]

    selected = copy.deepcopy(a3g["selected_candidate"]["design"])
    resistance_ratio = 0.5625
    selected.update(
        {
            "equivalent_field_rms_t": equivalent_field,
            "tooth_field_rms_t": tooth_field,
            "magnetic_ligament_field_rms_t": magnetic_peak,
            "conductor_area_per_turn_m2": declared["conductor_area_per_turn_m2"],
            "gross_slot_fill_fraction": declared["gross_slot_fill_fraction"],
            "cell_resistance_ohm": selected["cell_resistance_ohm"]
            * resistance_ratio,
            "phase_resistance_ohm": selected["phase_resistance_ohm"]
            * resistance_ratio,
            "primary_copper_mass_kg": declared["primary_copper_mass_kg"],
            "stationary_core_mass_kg": declared["stationary_core_mass_kg"],
            "active_primary_mass_kg": declared["active_primary_mass_kg"],
        }
    )

    cg_limit = base["interface"]["transverse_cg_limit_m"]
    points = base["interface"]["cg_grid_points_per_axis"]
    cg_grid = [
        -cg_limit + 2.0 * cg_limit * index / (points - 1)
        for index in range(points)
    ]
    nominal_conductance = (
        declared["equivalent_copper_sheet_thickness_m"]
        / base["passive_cage"]["copper_resistivity_ohm_m"]
    )
    corner_values = control["robustness_corners"]
    corners = [
        {
            "cage_sheet_conductance_multiplier": conductance,
            "phase_resistance_multiplier": resistance,
        }
        for conductance, resistance in itertools.product(
            corner_values["cage_sheet_conductance_multiplier"],
            corner_values["phase_resistance_multiplier"],
        )
    ]

    records = []
    for corner in corners:
        design = copy.deepcopy(selected)
        design["phase_resistance_ohm"] *= corner["phase_resistance_multiplier"]
        design["cell_resistance_ohm"] *= corner["phase_resistance_multiplier"]
        magnetic = {
            "rated_mmf_a_turn": declared["rated_mmf_a_turn"],
            "rated_phase_current_a": declared["rated_phase_current_rms_a"],
            "rated_primary_current_density_a_m2": declared[
                "rated_primary_current_density_a_m2"
            ],
            "phase_inductance_h": phase_inductance,
        }
        conductance = (
            nominal_conductance
            * corner["cage_sheet_conductance_multiplier"]
        )
        reference = evaluate_case(
            base,
            design,
            magnetic,
            conductance,
            base["interface"]["bare_payload_reference_mass_kg"],
            declared["interface_increment_kg"],
            declared["cage_copper_mass_kg"],
            declared["magnetic_matrix_mass_kg"],
            cg_grid,
            retain_point_records=True,
        )
        qualification = evaluate_case(
            base,
            design,
            magnetic,
            conductance,
            base["interface"]["bare_payload_qualification_mass_kg"],
            declared["interface_increment_kg"],
            declared["cage_copper_mass_kg"],
            declared["magnetic_matrix_mass_kg"],
            cg_grid,
            retain_point_records=True,
        )
        rated = cage_state(
            base["drive"]["rated_channel_force_n"],
            equivalent_field,
            conductance,
            base["interface"]["fins_per_channel"]
            * base["interface"]["active_cage_height_m"]
            * base["interface"]["active_length_m"],
            declared["equivalent_copper_sheet_thickness_m"],
        )
        mismatch = base["drive"]["side_to_side_field_amplitude_mismatch_fraction"]
        plus_field = rated["field_at_cage_rms_t"] * (1.0 + 0.5 * mismatch)
        minus_field = rated["field_at_cage_rms_t"] * (1.0 - 0.5 * mismatch)
        active_area = (
            base["interface"]["fins_per_channel"]
            * base["interface"]["active_cage_height_m"]
            * base["interface"]["active_length_m"]
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
        dc_margin = base["drive"]["nominal_dc_link_v"] / maximum_dc_link - 1.0
        bands = {
            "a6f_field_pass": field["screen_pass"],
            "interface_mass_absolute": declared["interface_increment_kg"]
            <= limits["maximum_interface_mass_kg"],
            "active_primary_mass": declared["active_primary_mass_kg"]
            <= limits["maximum_active_primary_mass_kg"],
            "rated_phase_current": declared["rated_phase_current_rms_a"]
            <= limits["maximum_rated_phase_current_a"],
            "primary_current_density": declared[
                "rated_primary_current_density_a_m2"
            ]
            <= limits["maximum_primary_current_density_a_m2"],
            "winding_slot_fill": declared["gross_slot_fill_fraction"]
            <= limits["maximum_winding_slot_fill_fraction"],
            "required_dc_link": maximum_dc_link
            <= limits["maximum_required_dc_link_v"],
            "dc_link_margin": dc_margin
            >= limits["minimum_margin_on_48v_link_fraction"],
            "reference_source_energy": reference["maximum_source_energy_j"]
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
        bands = {name: bool(value) for name, value in bands.items()}
        records.append(
            {
                "corner": corner,
                "cage_sheet_conductance_s": conductance,
                "phase_resistance_ohm": design["phase_resistance_ohm"],
                "reference": compact_case(reference),
                "qualification": compact_case(qualification),
                "maximum_required_dc_link_v": maximum_dc_link,
                "dc_link_margin_fraction": dc_margin,
                "unbalanced_normal_force_n": normal_residual,
                "bands": bands,
                "band_pass_count": sum(bands.values()),
                "band_count": len(bands),
                "failed_bands": [name for name, passed in bands.items() if not passed],
                "pass": all(bands.values()),
            }
        )

    failed_union = sorted(
        {name for record in records for name in record["failed_bands"]}
    )
    preferences = control["preferences"]
    preference_results = {
        "target_interface_mass": declared["interface_increment_kg"]
        <= preferences["target_interface_mass_kg"],
        "preferred_interface_mass": declared["interface_increment_kg"]
        <= preferences["preferred_interface_mass_kg"],
    }
    return {
        "evidence": "A7a POST-FIELD HOMOGENIZED CAGE + LUMPED CIRCUIT/CENTRE-OF-GRAVITY SHOT MODEL",
        "input_file": str(INPUT.relative_to(ROOT)),
        "source_files": control["source_files"],
        "field_trace": {
            "minimum_three_mesh_tooth_field_rms_t": tooth_field,
            "equivalent_sheet_field_rms_t": equivalent_field,
            "maximum_three_mesh_magnetic_material_field_t": magnetic_peak,
            "maximum_three_mesh_phase_inductance_h": phase_inductance,
        },
        "design": selected,
        "rated": {
            "phase_current_rms_a": declared["rated_phase_current_rms_a"],
            "ampere_turn_rms": declared["rated_mmf_a_turn"],
            "primary_current_density_a_m2": declared[
                "rated_primary_current_density_a_m2"
            ],
            "nominal_cage_sheet_conductance_s": nominal_conductance,
        },
        "interface": {
            "total_increment_kg": declared["interface_increment_kg"],
            "cage_copper_kg": declared["cage_copper_mass_kg"],
            "magnetic_matrix_kg": declared["magnetic_matrix_mass_kg"],
            "target_mass_kg": preferences["target_interface_mass_kg"],
            "preferred_mass_kg": preferences["preferred_interface_mass_kg"],
            "absolute_limit_kg": limits["maximum_interface_mass_kg"],
            "preference_results": preference_results,
        },
        "cg_points_per_case": len(cg_grid) ** 2,
        "corner_count": len(records),
        "corners": records,
        "corner_band_order": sorted(records[0]["bands"]),
        "failed_band_union": failed_union,
        "screen_pass": all(record["pass"] for record in records),
        "disposition": (
            "PROMOTE_GEN25_TO_DISCRETE_CAD_AND_TRANSIENT_FORCE_MODEL"
            if all(record["pass"] for record in records)
            else "DO_NOT_PROMOTE_GEN25_CAGE_CIRCUIT_POINT"
        ),
        "limits": [
            "The cage remains an equivalent sheet; discrete rungs, end buses and current crowding are absent.",
            "The shot model is quasi-steady and assumes prebias; switching, end effects and six-degree-of-freedom motion are absent.",
            "A6f field and inductance enter by worst-mesh selection; axial bar/backstrap geometry is still homogenized.",
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
            raise SystemExit("stale A7a CG-point artifact")
        compare_json(OUTPUT, result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
