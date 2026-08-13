"""Bolley A5d: evaluate the Gen2 CAD, packaging and nominal-fit bands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


PARAMETERS = ROOT / "cad" / "gen2_parameters.json"
BUILD = ROOT / "cad" / "BUILD_GEN2.json"
RENDERS = ROOT / "cad" / "renders" / "gen2" / "RENDERS.json"
PACKAGE = ROOT / "cad" / "exports" / "gen2" / "PACKAGE.json"
A3G = RESULTS / "fluxbridge_optimization.json"
OUTPUT = RESULTS / "gen2_cad_fit.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load(PARAMETERS)
    build = load(BUILD)
    renders = load(RENDERS)
    package = load(PACKAGE)
    a3g = load(A3G)
    payload = p["payload"]
    bridge = p["fluxbridge"]
    stator = p["stator"]
    track = p["track"]
    coupon = p["coupon"]
    limits = p["bands"]
    fit = build["fit_checks"]
    selected = a3g["selected_candidate"]["design"]
    records = build["artifacts"]
    complete_records = all(
        all(key in parent for key in ("solid_count", "volume_mm3", "bounding_box_mm"))
        and all(
            key in parent[kind] for key in ("path", "bytes", "sha256")
        )
        for parent in records.values()
        for kind in ("step", "stl")
    )
    package_counts = {
        kind: data["member_count"] for kind, data in package["packages"].items()
    }
    alignment = bridge["fin_centres_across_face_mm"] == stator[
        "slot_centres_across_face_mm"
    ]
    intersection_limit = limits["maximum_nominal_solid_intersection_mm3"]
    bands = {
        "payload_envelope_and_rails": (
            payload["envelope_length_x_mm"] == 340.5
            and payload["envelope_y_mm"] == 100.0
            and payload["envelope_z_mm"] == 100.0
            and payload["corner_rail_width_mm"] == 8.5
        ),
        "fluxbridge_projection": bridge["encapsulated_total_projection_mm"]
        <= limits["maximum_side_projection_mm"],
        "fin_slot_alignment_and_clearance": (
            alignment
            and bridge["fin_gross_thickness_mm"] == 1.0
            and stator["foil_slot_width_mm"] == 1.4
            and fit["nominal_fin_clearance_per_side_mm"]
            + 1e-12
            >= limits["minimum_nominal_fin_clearance_per_side_mm"]
        ),
        "stator_footprint_length_pitch_count": (
            stator["core_face_footprint_mm"]
            <= limits["maximum_core_face_footprint_mm"]
            and stator["active_length_x_mm"]
            == limits["required_active_stator_length_mm"]
            and stator["cell_pitch_x_mm"] == limits["required_cell_pitch_mm"]
            and stator["cell_count_per_face"]
            == limits["required_cell_count_per_face"]
        ),
        "winding_slot_fill": selected["gross_slot_fill_fraction"]
        <= limits["maximum_coil_slot_fill_fraction"] + 1e-12,
        "alternating_coil_route": (
            fit["minimum_coil_to_fluxbridge_radial_clearance_mm"]
            >= limits["minimum_coil_to_fluxbridge_radial_clearance_mm"]
            and fit["adjacent_coil_overlap_per_face_mm3"] <= intersection_limit
            and fit["coil_core_intersection_per_face_mm3"] <= intersection_limit
        ),
        "payload_stator_non_interference": fit[
            "payload_stator_intersection_all_faces_mm3"
        ]
        <= intersection_limit,
        "muzzle_and_frame_envelope": (
            fit["muzzle_opening_yz_mm"] >= limits["minimum_muzzle_opening_yz_mm"]
            and track["enclosure_outer_yz_mm"]
            <= limits["maximum_assembly_envelope_yz_mm"]
        ),
        "four_faces_and_positive_x_departure": (
            fit["stator_face_count"] == 4 and fit["departure_axis"] == "+x"
        ),
        "discrete_coupon_content": (
            fit["discrete_coupon_bar_period_count"]
            == coupon["cage_bar_period_count"]
            == 30
            and fit["discrete_coupon_stator_cell_count"]
            == coupon["stator_cell_count"]
            == 2
        ),
        "artifact_and_render_set": (
            package_counts["step"] >= limits["minimum_step_artifact_count"]
            and package_counts["stl"] >= limits["minimum_stl_artifact_count"]
            and renders["render_count"] >= limits["minimum_render_count"]
        ),
        "artifact_traceability": complete_records,
        "copper_volume_consistency": abs(fit["coil_volume_relative_error"])
        <= 0.005,
    }
    failed = [name for name, passed in bands.items() if not passed]
    return {
        "evidence": "A5d PARAMETRIC CAD + EXACT NOMINAL SOLID INTERSECTION + ARCHIVE MANIFEST",
        "input_files": [
            str(PARAMETERS.relative_to(ROOT)),
            str(BUILD.relative_to(ROOT)),
            str(RENDERS.relative_to(ROOT)),
            str(PACKAGE.relative_to(ROOT)),
            str(A3G.relative_to(ROOT)),
        ],
        "selected_a3g_candidate_id": a3g["selected_candidate_id"],
        "geometry": {
            "payload_envelope_mm": [
                payload["envelope_length_x_mm"],
                payload["envelope_y_mm"],
                payload["envelope_z_mm"],
            ],
            "fluxbridge_projection_mm": bridge["encapsulated_total_projection_mm"],
            "nominal_fin_clearance_per_side_mm": fit[
                "nominal_fin_clearance_per_side_mm"
            ],
            "core_face_footprint_mm": stator["core_face_footprint_mm"],
            "active_stator_length_mm": stator["active_length_x_mm"],
            "cell_pitch_mm": stator["cell_pitch_x_mm"],
            "cell_count_per_face": stator["cell_count_per_face"],
            "gross_winding_slot_fill_fraction": selected[
                "gross_slot_fill_fraction"
            ],
            "coil_to_fluxbridge_radial_clearance_mm": fit[
                "minimum_coil_to_fluxbridge_radial_clearance_mm"
            ],
            "payload_stator_intersection_all_faces_mm3": fit[
                "payload_stator_intersection_all_faces_mm3"
            ],
            "coil_core_intersection_per_face_mm3": fit[
                "coil_core_intersection_per_face_mm3"
            ],
            "adjacent_coil_overlap_per_face_mm3": fit[
                "adjacent_coil_overlap_per_face_mm3"
            ],
            "muzzle_opening_yz_mm": fit["muzzle_opening_yz_mm"],
            "assembly_frame_yz_mm": track["enclosure_outer_yz_mm"],
            "cad_coil_volume_mm3": fit[
                "coil_envelope_volume_all_four_faces_mm3"
            ],
            "analytical_copper_volume_mm3": fit[
                "a3g_analytical_copper_volume_all_four_faces_mm3"
            ],
            "coil_volume_relative_error": fit["coil_volume_relative_error"],
        },
        "artifacts": {
            "step_count": package_counts["step"],
            "stl_count": package_counts["stl"],
            "render_count": renders["render_count"],
            "step_archive": package["packages"]["step"]["path"],
            "stl_archive": package["packages"]["stl"]["path"],
        },
        "bands": bands,
        "band_count": len(bands),
        "band_pass_count": sum(bands.values()),
        "failed_bands": failed,
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_GEN2_GEOMETRY_TO_FIELD_STRUCTURE_AND_TOLERANCE_ANALYSIS"
            if all(bands.values())
            else "REJECT_GEN2_CAD"
        ),
        "limits": [
            "No tolerance stack, individual turns, insulation, leads, cooling, fasteners or lamination detail is present.",
            "Full-length Fluxbridge blades are homogenized; the coupon alone resolves cage bars.",
            "CAD geometry is not launch-provider approval or a manufacturing release.",
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
