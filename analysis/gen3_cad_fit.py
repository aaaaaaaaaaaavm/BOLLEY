"""Bolley A5e: evaluate my exact Gen3 Fluxrelay CAD and nominal-fit bands."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


PARAMETERS = ROOT / "cad" / "gen3_parameters.json"
BUILD = ROOT / "cad" / "BUILD_GEN3.json"
RENDERS = ROOT / "cad" / "renders" / "gen3" / "RENDERS.json"
PACKAGE = ROOT / "cad" / "exports" / "gen3" / "PACKAGE.json"
A8B = RESULTS / "gen27_codesign.json"
A6H = RESULTS / "gen27_field.json"
A7C = RESULTS / "gen27_cage_circuit.json"
OUTPUT = RESULTS / "gen3_cad_fit.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def close(a: float, b: float, tolerance: float = 1e-9) -> bool:
    return math.isclose(a, b, rel_tol=tolerance, abs_tol=tolerance)


def calculate() -> dict:
    p = load(PARAMETERS)
    build = load(BUILD)
    renders = load(RENDERS)
    package = load(PACKAGE)
    a8b = load(A8B)
    a6h = load(A6H)
    a7c = load(A7C)
    selected = a8b["selected_candidate"]
    payload = p["payload"]
    relay = p["fluxbridge"]
    stator = p["stator"]
    sectional = p["sectional_drive"]
    track = p["track"]
    coupon = p["coupon"]
    limits = p["bands"]
    fit = build["fit_checks"]
    records = build["artifacts"]
    complete_records = all(
        all(key in parent for key in ("solid_count", "volume_mm3", "bounding_box_mm"))
        and all(key in parent[kind] for key in ("path", "bytes", "sha256"))
        for parent in records.values()
        for kind in ("step", "stl")
    )
    package_counts = {kind: data["member_count"] for kind, data in package["packages"].items()}
    alignment = relay["fin_centres_across_face_mm"] == stator["slot_centres_across_face_mm"]
    intersection_limit = limits["maximum_nominal_solid_intersection_mm3"]
    selected_design = selected["design"]
    selected_interface = selected["interface"]
    bands = {
        "upstream_a6h_a7c_pass": a6h["screen_pass"] and a7c["screen_pass"],
        "payload_envelope_and_rails": (
            close(payload["envelope_length_x_mm"], 340.5)
            and close(payload["envelope_y_mm"], 100.0)
            and close(payload["envelope_z_mm"], 100.0)
            and close(payload["corner_rail_width_mm"], 8.5)
        ),
        "fluxrelay_projection": relay["encapsulated_total_projection_mm"]
        <= limits["maximum_side_projection_mm"],
        "five_lane_slot_alignment_and_clearance": (
            alignment
            and len(relay["fin_centres_across_face_mm"]) == 5
            and close(relay["fin_gross_thickness_mm"], 1.18)
            and close(stator["foil_slot_width_mm"], 1.58)
            and fit["nominal_fin_clearance_per_side_mm"] + 1e-12
            >= limits["minimum_nominal_fin_clearance_per_side_mm"]
        ),
        "stator_length_pitch_count": (
            stator["core_face_footprint_mm"] <= limits["maximum_core_face_footprint_mm"]
            and close(stator["active_length_x_mm"], limits["required_active_stator_length_mm"])
            and close(stator["cell_pitch_x_mm"], limits["required_cell_pitch_mm"])
            and stator["cell_count_per_face"] == limits["required_cell_count_per_face"]
        ),
        "cage_length_start_and_endpoint_guard": (
            close(relay["active_length_x_mm"], limits["required_active_cage_length_mm"])
            and close(relay["active_length_start_x_mm"], limits["required_active_cage_start_mm"])
            and fit["endpoint_overlap_guard_mm"] + 1e-12 >= limits["minimum_endpoint_guard_mm"]
            and relay["active_length_start_x_mm"] + relay["active_length_x_mm"]
            <= payload["envelope_length_x_mm"]
        ),
        "sectional_active_window": (
            fit["active_window_cell_count"] == limits["required_active_window_cell_count"]
            and fit["active_window_cells_per_phase"]
            == limits["required_active_window_cells_per_phase"]
            and sectional["maximum_intersected_cell_count"]
            == limits["required_active_window_cell_count"]
        ),
        "winding_slot_fill": selected_design["gross_slot_fill_fraction"]
        <= limits["maximum_coil_slot_fill_fraction"],
        "alternating_coil_route": (
            fit["minimum_coil_to_fluxbridge_radial_clearance_mm"]
            >= limits["minimum_coil_to_fluxbridge_radial_clearance_mm"]
            and fit["adjacent_coil_overlap_per_face_mm3"] <= intersection_limit
            and fit["coil_core_intersection_per_face_mm3"] <= intersection_limit
        ),
        "payload_stator_non_interference": fit["payload_stator_intersection_all_faces_mm3"]
        <= intersection_limit,
        "muzzle_and_frame_envelope": (
            fit["muzzle_opening_yz_mm"] >= limits["minimum_muzzle_opening_yz_mm"]
            and track["enclosure_outer_yz_mm"] <= limits["maximum_assembly_envelope_yz_mm"]
        ),
        "four_faces_and_positive_x_departure": fit["stator_face_count"] == 4
        and fit["departure_axis"] == "+x",
        "discrete_coupon_content": (
            fit["discrete_coupon_bar_period_count"]
            == coupon["cage_bar_period_count"]
            == 50
            and fit["discrete_coupon_stator_cell_count"]
            == coupon["stator_cell_count"]
            == 2
        ),
        "active_material_mass": (
            selected_interface["total_increment_kg"] <= limits["maximum_interface_mass_kg"]
            and selected_design["installed_active_primary_mass_kg"]
            <= limits["maximum_installed_active_primary_mass_kg"]
        ),
        "artifact_and_render_set": (
            package_counts["step"] >= limits["minimum_step_artifact_count"]
            and package_counts["stl"] >= limits["minimum_stl_artifact_count"]
            and renders["render_count"] >= limits["minimum_render_count"]
        ),
        "artifact_traceability": complete_records,
        "installed_copper_volume_consistency": abs(fit["coil_volume_relative_error"])
        <= limits["maximum_copper_volume_relative_error"],
    }
    bands = {name: bool(value) for name, value in bands.items()}
    failed = [name for name, passed in bands.items() if not passed]
    return {
        "evidence": "A5e PARAMETRIC GEN3 CAD + EXACT NOMINAL SOLID INTERSECTION + ARCHIVE MANIFEST",
        "input_files": [
            str(path.relative_to(ROOT))
            for path in (PARAMETERS, BUILD, RENDERS, PACKAGE, A8B, A6H, A7C)
        ],
        "selected_candidate_id": selected["candidate_id"],
        "geometry": {
            "payload_envelope_mm": [
                payload["envelope_length_x_mm"],
                payload["envelope_y_mm"],
                payload["envelope_z_mm"],
            ],
            "active_cage_start_mm": relay["active_length_start_x_mm"],
            "active_cage_length_mm": relay["active_length_x_mm"],
            "finished_lane_count_per_face": len(relay["fin_centres_across_face_mm"]),
            "finished_lane_width_mm": relay["fin_gross_thickness_mm"],
            "nominal_lane_clearance_per_side_mm": fit["nominal_fin_clearance_per_side_mm"],
            "core_face_footprint_mm": stator["core_face_footprint_mm"],
            "active_stator_length_mm": stator["active_length_x_mm"],
            "cell_pitch_mm": stator["cell_pitch_x_mm"],
            "cell_count_per_face": stator["cell_count_per_face"],
            "active_window_cell_count": fit["active_window_cell_count"],
            "gross_winding_slot_fill_fraction": selected_design["gross_slot_fill_fraction"],
            "coil_to_lane_radial_clearance_mm": fit["minimum_coil_to_fluxbridge_radial_clearance_mm"],
            "endpoint_overlap_guard_mm": fit["endpoint_overlap_guard_mm"],
            "payload_stator_intersection_all_faces_mm3": fit["payload_stator_intersection_all_faces_mm3"],
            "coil_core_intersection_per_face_mm3": fit["coil_core_intersection_per_face_mm3"],
            "adjacent_coil_overlap_per_face_mm3": fit["adjacent_coil_overlap_per_face_mm3"],
            "muzzle_opening_yz_mm": fit["muzzle_opening_yz_mm"],
            "assembly_frame_yz_mm": track["enclosure_outer_yz_mm"],
            "cad_coil_volume_mm3": fit["coil_envelope_volume_all_four_faces_mm3"],
            "a8b_installed_copper_volume_mm3": fit["a8b_installed_copper_volume_all_four_faces_mm3"],
            "coil_volume_relative_error": fit["coil_volume_relative_error"],
        },
        "mass_trace": {
            "interface_increment_kg": selected_interface["total_increment_kg"],
            "installed_active_primary_kg": selected_design["installed_active_primary_mass_kg"],
            "unallocated_active_material_margin_kg": limits[
                "maximum_installed_active_primary_mass_kg"
            ]
            - selected_design["installed_active_primary_mass_kg"],
            "excluded_from_active_material_band": [
                "structure",
                "containment",
                "insulation",
                "cooling",
                "wiring",
                "sensors",
                "power electronics",
            ],
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
            "PROMOTE_GEN3_NOMINAL_GEOMETRY_TO_TOLERANCE_STRUCTURE_AND_A9"
            if all(bands.values())
            else "REJECT_GEN3_NOMINAL_CAD"
        ),
        "limits": [
            "No tolerance stack, individual turns, insulation, leads, cooling, fasteners or lamination detail is present.",
            "Full-length Fluxrelay lanes are homogenized; the coupon alone resolves webs and rungs.",
            "The 92 g active-material margin is not a structure or packaged-system allocation.",
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
