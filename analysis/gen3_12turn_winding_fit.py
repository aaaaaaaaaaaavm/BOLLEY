"""Bolley A5f: screen the A9f 12-turn winding inside my retained Gen3 stator."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "cad" / "gen3_12turn_winding_parameters.json"
GEN3 = ROOT / "cad" / "gen3_parameters.json"
A9F = RESULTS / "turn_current_exchange.json"
OUTPUT = RESULTS / "gen3_12turn_winding_fit.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def corner_radius(thickness_mm: float) -> float:
    if thickness_mm <= 1.0:
        return 0.5 * thickness_mm
    if thickness_mm <= 1.6:
        return 0.5
    if thickness_mm <= 2.24:
        return 0.65
    if thickness_mm <= 3.55:
        return 0.8
    raise ValueError("A5f thickness leaves the frozen IEC screening range")


def bare_area(width_mm: float, thickness_mm: float) -> float:
    radius = corner_radius(thickness_mm)
    return width_mm * thickness_mm - (4.0 - math.pi) * radius**2


def solve_thickness(width_mm: float, target_area_mm2: float) -> float | None:
    """Solve the piecewise rounded-rectangle area relation inside the frozen IEC ranges."""

    solutions: list[float] = []
    k = 4.0 - math.pi

    # t <= 1 mm, r=t/2.
    a = 0.25 * k
    discriminant = width_mm**2 - 4.0 * a * target_area_mm2
    if discriminant >= 0.0:
        root = math.sqrt(discriminant)
        for thickness in (
            (width_mm - root) / (2.0 * a),
            (width_mm + root) / (2.0 * a),
        ):
            if 0.0 < thickness <= 1.0:
                solutions.append(thickness)

    for lower, upper, radius in (
        (1.0, 1.6, 0.5),
        (1.6, 2.24, 0.65),
        (2.24, 3.55, 0.8),
    ):
        thickness = (target_area_mm2 + k * radius**2) / width_mm
        if lower < thickness <= upper:
            solutions.append(thickness)

    if not solutions:
        return None
    return min(solutions)


def candidate(width_mm: float, p: dict) -> dict | None:
    electrical = p["electrical"]
    search = p["winding_search"]
    wire = p["rectangular_wire_screen"]
    geometry = p["a5e_geometry"]
    bands = p["bands"]

    target_area = electrical["target_bare_copper_area_per_turn_mm2"]
    thickness = solve_thickness(width_mm, target_area)
    if thickness is None or thickness > width_mm:
        return None

    radius = corner_radius(thickness)
    area = bare_area(width_mm, thickness)
    insulated_width = width_mm + wire["maximum_increase_in_width_or_thickness_due_to_insulation_mm"]
    insulated_thickness = thickness + wire["maximum_increase_in_width_or_thickness_due_to_insulation_mm"]

    in_plane_layers = search["in_plane_layers"]
    radial_layers = search["radial_layers"]
    ring_wall = in_plane_layers * insulated_thickness
    radial_height = radial_layers * insulated_width
    outer_axial = search["inner_axial_span_mm"] + 2.0 * ring_wall
    outer_transverse = search["inner_transverse_span_mm"] + 2.0 * ring_wall

    available_radial = (
        geometry["back_yoke_radial_start_above_face_mm"]
        - geometry["fluxrelay_projection_mm"]
        - search["minimum_coil_to_fluxrelay_radial_clearance_mm"]
    )
    remaining_radial = available_radial - 2.0 * radial_height
    interlayer_clearance = 0.5 * remaining_radial
    upper_back_yoke_clearance = 0.5 * remaining_radial
    same_layer_axial_clearance = 2.0 * geometry["cell_pitch_mm"] - outer_axial

    # The same-cell tooth is inside the frozen inner axial opening. The nearest neighbouring
    # tooth starts one pitch away. Positive separation proves zero axis-aligned solid overlap
    # without a BRep operation for this upstream screen.
    same_cell_core_axial_clearance = 0.5 * (
        search["inner_axial_span_mm"] - 22.65
    )
    neighbouring_core_axial_clearance = (
        geometry["cell_pitch_mm"]
        - 0.5 * 22.65
        - 0.5 * outer_axial
    )
    coil_core_intersection = 0.0 if min(
        same_cell_core_axial_clearance, neighbouring_core_axial_clearance
    ) >= 0.0 else math.inf
    adjacent_coil_intersection = 0.0 if min(
        interlayer_clearance, same_layer_axial_clearance
    ) >= 0.0 else math.inf

    turn_lengths = [
        2.0
        * (
            search["inner_axial_span_mm"]
            + (2 * index + 1) * insulated_thickness
            + search["inner_transverse_span_mm"]
            + (2 * index + 1) * insulated_thickness
        )
        for index in range(in_plane_layers)
    ]
    mean_turn_length = sum(turn_lengths) / len(turn_lengths)
    copper_volume = radial_layers * sum(turn_lengths) * target_area
    target_volume = electrical["target_a5e_copper_volume_per_cell_mm3"]
    copper_volume_relative_error = copper_volume / target_volume - 1.0
    total_cross_section = electrical["turns_per_cell"] * area
    cross_section_relative_error = (
        total_cross_section
        / electrical["target_total_bare_copper_area_per_coil_side_mm2"]
        - 1.0
    )
    current_density = electrical["phase_current_rms_a"] / area
    gross_slot_fill = (
        2.0
        * electrical["turns_per_cell"]
        * insulated_width
        * insulated_thickness
        / geometry["available_slot_area_mm2"]
    )
    gross_envelope_area = (
        electrical["turns_per_cell"] * insulated_width * insulated_thickness
    )

    checks = {
        "turns": electrical["turns_per_cell"] == bands["required_turns_per_cell"],
        "excitation": math.isclose(
            electrical["turns_per_cell"] * electrical["phase_current_rms_a"],
            bands["required_ampere_turn_rms"],
            rel_tol=0.0,
            abs_tol=1e-12,
        ),
        "current_density": current_density <= bands["maximum_current_density_a_mm2"],
        "bare_cross_section_identity": abs(cross_section_relative_error)
        <= bands["maximum_bare_cross_section_relative_error"],
        "detailed_copper_volume": abs(copper_volume_relative_error)
        <= bands["maximum_copper_volume_relative_error"],
        "gross_slot_fill": gross_slot_fill <= bands["maximum_gross_slot_fill_fraction"],
        "coil_to_fluxrelay": search["minimum_coil_to_fluxrelay_radial_clearance_mm"]
        >= bands["minimum_coil_to_fluxrelay_radial_clearance_mm"],
        "interlayer_radial_clearance": interlayer_clearance
        >= bands["minimum_interlayer_radial_clearance_mm"],
        "upper_coil_to_back_yoke_clearance": upper_back_yoke_clearance
        >= bands["minimum_upper_coil_to_back_yoke_clearance_mm"],
        "same_layer_axial_clearance": same_layer_axial_clearance
        >= bands["minimum_same_layer_axial_clearance_mm"],
        "coil_core_intersection": coil_core_intersection
        <= bands["maximum_coil_core_intersection_mm3"],
        "adjacent_coil_intersection": adjacent_coil_intersection
        <= bands["maximum_adjacent_coil_intersection_mm3"],
    }
    return {
        "bare_width_mm": width_mm,
        "bare_thickness_mm": thickness,
        "bare_corner_radius_mm": radius,
        "bare_area_per_turn_mm2": area,
        "insulated_overall_width_mm": insulated_width,
        "insulated_overall_thickness_mm": insulated_thickness,
        "gross_ring_wall_mm": ring_wall,
        "coil_radial_height_mm": radial_height,
        "outer_axial_span_mm": outer_axial,
        "outer_transverse_span_mm": outer_transverse,
        "interlayer_radial_clearance_mm": interlayer_clearance,
        "upper_coil_to_back_yoke_clearance_mm": upper_back_yoke_clearance,
        "same_layer_axial_clearance_mm": same_layer_axial_clearance,
        "same_cell_core_axial_clearance_mm": same_cell_core_axial_clearance,
        "neighbouring_core_axial_clearance_mm": neighbouring_core_axial_clearance,
        "coil_core_intersection_mm3": coil_core_intersection,
        "adjacent_coil_intersection_mm3": adjacent_coil_intersection,
        "turn_centreline_lengths_mm": turn_lengths,
        "mean_turn_length_mm": mean_turn_length,
        "detailed_copper_volume_per_cell_mm3": copper_volume,
        "copper_volume_relative_error": copper_volume_relative_error,
        "total_bare_cross_section_per_coil_side_mm2": total_cross_section,
        "bare_cross_section_relative_error": cross_section_relative_error,
        "current_density_a_mm2": current_density,
        "gross_insulated_slot_fill_fraction": gross_slot_fill,
        "gross_insulated_conductor_envelope_area_per_coil_side_mm2": gross_envelope_area,
        "checks": checks,
        "pass": all(checks.values()),
        "failed_bands": [name for name, passed in checks.items() if not passed],
    }


def calculate() -> dict:
    p = load(INPUT)
    gen3 = load(GEN3)
    a9f = load(A9F)
    selected = a9f["selected_candidate"]
    electrical = p["electrical"]
    search = p["winding_search"]

    if selected["turns_per_cell"] != electrical["turns_per_cell"]:
        raise SystemExit("A5f turn count no longer matches A9f")
    if not math.isclose(
        selected["rated_phase_current_a"],
        electrical["phase_current_rms_a"],
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise SystemExit("A5f phase current no longer matches A9f")
    if not math.isclose(
        gen3["stator"]["cell_pitch_x_mm"],
        p["a5e_geometry"]["cell_pitch_mm"],
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise SystemExit("A5f cell pitch no longer matches A5e")

    steps = round(
        (search["bare_width_max_mm"] - search["bare_width_min_mm"])
        / search["bare_width_step_mm"]
    )
    candidates = []
    for index in range(steps + 1):
        width = round(
            search["bare_width_min_mm"] + index * search["bare_width_step_mm"], 10
        )
        record = candidate(width, p)
        if record is not None:
            candidates.append(record)

    passing = [record for record in candidates if record["pass"]]
    geometry_only = [
        record
        for record in candidates
        if all(
            passed
            for name, passed in record["checks"].items()
            if name != "detailed_copper_volume"
        )
    ]
    closest_volume_geometry_candidate = min(
        geometry_only, key=lambda record: abs(record["copper_volume_relative_error"])
    )
    minimum_envelope_geometry_candidate = min(
        geometry_only,
        key=lambda record: (
            record["gross_insulated_conductor_envelope_area_per_coil_side_mm2"],
            -min(
                record["interlayer_radial_clearance_mm"],
                record["upper_coil_to_back_yoke_clearance_mm"],
            ),
            record["gross_ring_wall_mm"],
            record["bare_width_mm"],
        ),
    )
    selected_candidate = None
    if passing:
        selected_candidate = min(
            passing,
            key=lambda record: (
                record["gross_insulated_conductor_envelope_area_per_coil_side_mm2"],
                -min(
                    record["interlayer_radial_clearance_mm"],
                    record["upper_coil_to_back_yoke_clearance_mm"],
                ),
                record["gross_ring_wall_mm"],
                record["bare_width_mm"],
            ),
        )

    return {
        "evidence": "A5f NOMINAL RECTANGULAR-WIRE ENVELOPE AND COPPER-PATH SCREEN",
        "input_file": str(INPUT.relative_to(ROOT)),
        "source_files": [str(GEN3.relative_to(ROOT)), str(A9F.relative_to(ROOT))],
        "candidate_count": len(candidates),
        "geometry_only_pass_count": len(geometry_only),
        "full_band_pass_count": len(passing),
        "screen_pass": bool(passing),
        "selected_candidate": selected_candidate,
        "closest_volume_geometry_candidate": closest_volume_geometry_candidate,
        "minimum_envelope_geometry_candidate": minimum_envelope_geometry_candidate,
        "candidates": candidates,
        "disposition": (
            "A5F_PASS_PROMOTE_12TURN_POINT_TO_DETAILED_CAD_AND_PACKAGE_RECLOSURE"
            if passing
            else "A5F_FAIL_FIXED_INNER_SPANS_EXCEED_A5E_COPPER_VOLUME"
        ),
        "limits": [
            "Axis-aligned positive separations establish zero nominal overlap for this upstream envelope screen; I do not export new STEP/STL from a rejected point.",
            "A5f fixes the A5e inner axial and transverse spans. A later redesign may change them only behind a new declaration.",
            "IEC insulation dimensions are a screening envelope, not supplier qualification or a winding-process specification.",
            "Lead exits, terminals, impregnation, bend strain, bridge placement, hot resistance, switching loss, cooling and vibration remain absent.",
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
