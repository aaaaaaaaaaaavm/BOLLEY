"""Bolley A5g: restore A5e mean turn length for the A9f 12-turn winding."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from gen3_12turn_winding_fit import bare_area, solve_thickness


INPUT = ROOT / "cad" / "gen3_12turn_path_parameters.json"
A9F = RESULTS / "turn_current_exchange.json"
OUTPUT = RESULTS / "gen3_12turn_path_fit.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def record(width_mm: float, p: dict) -> dict | None:
    electrical = p["electrical"]
    search = p["winding_search"]
    wire = p["rectangular_wire_screen"]
    geometry = p["gen3_geometry"]
    bands = p["bands"]
    target_area = electrical["target_bare_copper_area_per_turn_mm2"]
    thickness = solve_thickness(width_mm, target_area)
    if thickness is None or thickness > width_mm:
        return None

    area = bare_area(width_mm, thickness)
    insulation = wire["maximum_increase_in_width_or_thickness_due_to_insulation_mm"]
    overall_width = width_mm + insulation
    overall_thickness = thickness + insulation
    in_plane_layers = search["in_plane_layers"]
    radial_layers = search["radial_layers"]
    fixed_transverse = search["fixed_inner_transverse_span_mm"]
    target_mean = electrical["target_mean_turn_length_mm"]

    # For four nested in-plane loops the average (2*j+1) coefficient is four.
    # mean = 2 * (inner_axial + inner_transverse + 8*T).
    inner_axial = 0.5 * target_mean - fixed_transverse - 8.0 * overall_thickness
    ring_wall = in_plane_layers * overall_thickness
    radial_height = radial_layers * overall_width
    outer_axial = inner_axial + 2.0 * ring_wall
    outer_transverse = fixed_transverse + 2.0 * ring_wall

    available_radial = (
        geometry["back_yoke_radial_start_above_face_mm"]
        - geometry["fluxrelay_projection_mm"]
        - search["minimum_coil_to_fluxrelay_radial_clearance_mm"]
    )
    remaining_radial = available_radial - 2.0 * radial_height
    interlayer = 0.5 * remaining_radial
    upper_yoke = 0.5 * remaining_radial
    same_cell_core = 0.5 * (inner_axial - geometry["tooth_axial_width_mm"])
    neighbouring_core = (
        geometry["cell_pitch_mm"]
        - 0.5 * geometry["tooth_axial_width_mm"]
        - 0.5 * outer_axial
    )
    same_layer = 2.0 * geometry["cell_pitch_mm"] - outer_axial

    lengths = [
        2.0
        * (
            inner_axial
            + (2 * index + 1) * overall_thickness
            + fixed_transverse
            + (2 * index + 1) * overall_thickness
        )
        for index in range(in_plane_layers)
    ]
    mean_turn = sum(lengths) / len(lengths)
    copper_volume = radial_layers * sum(lengths) * target_area
    total_cross_section = electrical["turns_per_cell"] * area
    cross_error = total_cross_section / electrical["target_total_bare_copper_area_per_coil_side_mm2"] - 1.0
    volume_error = copper_volume / electrical["target_copper_volume_per_cell_mm3"] - 1.0
    mean_error = mean_turn / target_mean - 1.0
    current_density = electrical["phase_current_rms_a"] / area
    gross_fill = (
        2.0
        * electrical["turns_per_cell"]
        * overall_width
        * overall_thickness
        / geometry["available_slot_area_mm2"]
    )
    gross_envelope_area = electrical["turns_per_cell"] * overall_width * overall_thickness

    checks = {
        "turns": electrical["turns_per_cell"] == bands["required_turns_per_cell"],
        "excitation": math.isclose(
            electrical["turns_per_cell"] * electrical["phase_current_rms_a"],
            bands["required_ampere_turn_rms"], rel_tol=0.0, abs_tol=1e-12
        ),
        "current_density": current_density <= bands["maximum_current_density_a_mm2"],
        "bare_cross_section_identity": abs(cross_error) <= bands["maximum_bare_cross_section_relative_error"],
        "detailed_copper_volume": abs(volume_error) <= bands["maximum_copper_volume_relative_error"],
        "mean_turn_length": abs(mean_error) <= bands["maximum_mean_turn_length_relative_error"],
        "gross_slot_fill": gross_fill <= bands["maximum_gross_slot_fill_fraction"],
        "coil_to_fluxrelay": search["minimum_coil_to_fluxrelay_radial_clearance_mm"] >= bands["minimum_coil_to_fluxrelay_radial_clearance_mm"],
        "same_cell_core_axial_separation": same_cell_core >= bands["minimum_inner_axial_core_clearance_mm"],
        "neighbouring_core_axial_separation": neighbouring_core >= bands["minimum_neighbouring_core_axial_clearance_mm"],
        "interlayer_radial_clearance": interlayer >= bands["minimum_interlayer_radial_clearance_mm"],
        "upper_coil_to_back_yoke_clearance": upper_yoke >= bands["minimum_upper_coil_to_back_yoke_clearance_mm"],
        "same_layer_axial_clearance": same_layer >= bands["minimum_same_layer_axial_clearance_mm"],
    }
    return {
        "bare_width_mm": width_mm,
        "bare_thickness_mm": thickness,
        "bare_area_per_turn_mm2": area,
        "insulated_overall_width_mm": overall_width,
        "insulated_overall_thickness_mm": overall_thickness,
        "solved_inner_axial_span_mm": inner_axial,
        "fixed_inner_transverse_span_mm": fixed_transverse,
        "gross_ring_wall_mm": ring_wall,
        "coil_radial_height_mm": radial_height,
        "outer_axial_span_mm": outer_axial,
        "outer_transverse_span_mm": outer_transverse,
        "interlayer_radial_clearance_mm": interlayer,
        "upper_coil_to_back_yoke_clearance_mm": upper_yoke,
        "same_cell_core_axial_clearance_mm": same_cell_core,
        "neighbouring_core_axial_clearance_mm": neighbouring_core,
        "same_layer_axial_clearance_mm": same_layer,
        "turn_centreline_lengths_mm": lengths,
        "mean_turn_length_mm": mean_turn,
        "mean_turn_length_relative_error": mean_error,
        "detailed_copper_volume_per_cell_mm3": copper_volume,
        "copper_volume_relative_error": volume_error,
        "total_bare_cross_section_per_coil_side_mm2": total_cross_section,
        "bare_cross_section_relative_error": cross_error,
        "current_density_a_mm2": current_density,
        "gross_insulated_slot_fill_fraction": gross_fill,
        "gross_insulated_conductor_envelope_area_per_coil_side_mm2": gross_envelope_area,
        "minimum_core_axial_separation_mm": min(same_cell_core, neighbouring_core),
        "minimum_radial_clearance_mm": min(interlayer, upper_yoke),
        "checks": checks,
        "pass": all(checks.values()),
        "failed_bands": [name for name, passed in checks.items() if not passed],
    }


def selection_key(item: dict) -> tuple:
    return (
        item["gross_insulated_conductor_envelope_area_per_coil_side_mm2"],
        -item["minimum_radial_clearance_mm"],
        -item["minimum_core_axial_separation_mm"],
        item["bare_width_mm"],
    )


def calculate() -> dict:
    p = load(INPUT)
    a9f = load(A9F)
    selected_a9f = a9f["selected_candidate"]
    if selected_a9f["turns_per_cell"] != p["electrical"]["turns_per_cell"]:
        raise SystemExit("A5g no longer matches A9f turn count")
    if not math.isclose(
        selected_a9f["rated_phase_current_a"], p["electrical"]["phase_current_rms_a"], rel_tol=0.0, abs_tol=1e-12
    ):
        raise SystemExit("A5g no longer matches A9f current")

    search = p["winding_search"]
    steps = round((search["bare_width_max_mm"] - search["bare_width_min_mm"]) / search["bare_width_step_mm"])
    candidates = []
    for index in range(steps + 1):
        width = round(search["bare_width_min_mm"] + index * search["bare_width_step_mm"], 10)
        item = record(width, p)
        if item is not None:
            candidates.append(item)
    passing = [item for item in candidates if item["pass"]]
    selected = min(passing, key=selection_key) if passing else None
    return {
        "evidence": "A5g PATH-CORRECTED 12-TURN RECTANGULAR-WIRE ENVELOPE SCREEN",
        "input_file": str(INPUT.relative_to(ROOT)),
        "source_result_file": str(A9F.relative_to(ROOT)),
        "candidate_count": len(candidates),
        "candidate_width_range_mm": [candidates[0]["bare_width_mm"], candidates[-1]["bare_width_mm"]],
        "candidate_width_step_mm": search["bare_width_step_mm"],
        "full_band_pass_count": len(passing),
        "screen_pass": bool(passing),
        "selected_candidate": selected,
        "disposition": (
            "A5G_PASS_PROMOTE_SELECTED_12TURN_WINDING_TO_DETAILED_CAD"
            if passing else "A5G_FAIL_REJECT_12TURN_PATH_REDESIGN"
        ),
        "limits": [
            "A5g solves one in-plane opening dimension analytically; it is not detailed conductor CAD.",
            "Axis-aligned clearances are nominal and do not include manufacturing tolerance or thermal growth.",
            "Supplier wire size, bend strain, terminals, lead exits, bridge placement, insulation life and vibration remain open.",
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
