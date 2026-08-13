"""Bolley A5c: evaluate the frozen Gen1 CAD package and nominal fit bands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


PARAMETERS = ROOT / "cad" / "gen1_parameters.json"
BUILD = ROOT / "cad" / "BUILD.json"
RENDERS = ROOT / "cad" / "renders" / "gen1" / "RENDERS.json"
STATOR_RESULT = RESULTS / "stator_circuit.json"
OUTPUT = RESULTS / "cad_fit.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load(PARAMETERS)
    build = load(BUILD)
    renders = load(RENDERS)
    stator = load(STATOR_RESULT)
    payload = p["payload"]
    foil = p["fluxfoil"]
    core = p["stator"]
    track = p["track"]
    limits = p["bands"]
    fit = build["fit_checks"]
    records = build["artifacts"]

    step_records = [record["step"] for record in records.values()]
    stl_records = [record["stl"] for record in records.values()]
    clearance = (core["slot_width_mm"] - foil["fin_thickness_mm"]) / 2.0
    complete_records = all(
        all(key in record for key in ("bytes", "sha256"))
        and all(key in parent for key in ("solid_count", "volume_mm3", "bounding_box_mm"))
        for parent in records.values()
        for record in (parent["step"], parent["stl"])
    )
    body_and_rail_match = (
        payload["envelope_length_x_mm"] == 340.5
        and payload["envelope_y_mm"] == 100.0
        and payload["envelope_z_mm"] == 100.0
        and payload["corner_rail_width_mm"] == 8.5
    )
    bands = {
        "payload_envelope_and_rails": body_and_rail_match,
        "fluxfoil_projection": foil["total_projection_mm"]
        <= limits["maximum_fluxfoil_projection_mm"],
        "fin_slot_alignment_and_clearance": (
            foil["fin_centres_across_face_mm"] == core["slot_centres_across_face_mm"]
            and foil["fin_thickness_mm"] == 1.0
            and core["slot_width_mm"] == 2.0
            and clearance >= limits["minimum_nominal_slot_clearance_per_side_mm"]
        ),
        "stator_footprint_and_length": (
            core["face_footprint_mm"] <= limits["maximum_stator_face_footprint_mm"]
            and core["active_length_x_mm"] == limits["required_active_stator_length_mm"]
        ),
        "muzzle_and_frame_envelope": (
            fit["muzzle_opening_yz_mm"] >= limits["minimum_muzzle_opening_yz_mm"]
            and track["enclosure_outer_yz_mm"] <= limits["maximum_assembly_envelope_yz_mm"]
        ),
        "nominal_payload_stator_non_interference": abs(
            fit["nominal_payload_stator_intersection_all_four_faces_mm3"]
        )
        <= 1e-9,
        "four_faces_and_positive_x_departure": (
            fit["stator_face_count"] == 4 and fit["departure_axis"] == "+x"
        ),
        "step_and_stl_set": (
            len(step_records) >= limits["minimum_step_artifact_count"]
            and len(stl_records) >= limits["minimum_stl_artifact_count"]
        ),
        "render_set": renders["render_count"] >= limits["minimum_render_count"],
        "artifact_traceability": complete_records,
    }

    turns = stator["winding"]["turns_per_cell"]
    conductor_area = stator["winding"]["copper_area_m2"] * 1e6
    intercell_gap = core["phase_cell_axial_gap_mm"]
    nominal_coil_height = core["coil_pack_outer_height_mm"]
    available_section = intercell_gap * nominal_coil_height
    gross_copper_section = turns * conductor_area
    failed = [name for name, passed in bands.items() if not passed]
    return {
        "evidence": "PARAMETRIC CAD MANIFEST AND EXACT NOMINAL SOLID INTERSECTION",
        "input_files": [
            str(PARAMETERS.relative_to(ROOT)),
            str(BUILD.relative_to(ROOT)),
            str(RENDERS.relative_to(ROOT)),
            str(STATOR_RESULT.relative_to(ROOT)),
        ],
        "geometry": {
            "payload_envelope_mm": [
                payload["envelope_length_x_mm"],
                payload["envelope_y_mm"],
                payload["envelope_z_mm"],
            ],
            "fluxfoil_projection_mm": foil["total_projection_mm"],
            "nominal_slot_clearance_per_side_mm": clearance,
            "stator_face_footprint_mm": core["face_footprint_mm"],
            "active_stator_length_mm": core["active_length_x_mm"],
            "muzzle_opening_yz_mm": fit["muzzle_opening_yz_mm"],
            "assembly_frame_yz_mm": track["enclosure_outer_yz_mm"],
            "payload_stator_intersection_per_face_mm3": fit[
                "nominal_payload_stator_intersection_per_face_mm3"
            ],
            "payload_stator_intersection_all_faces_mm3": fit[
                "nominal_payload_stator_intersection_all_four_faces_mm3"
            ],
        },
        "artifact_counts": {
            "step": len(step_records),
            "stl": len(stl_records),
            "render": renders["render_count"],
        },
        "winding_pack_discovery": {
            "turns_per_cell": turns,
            "conductor_area_per_turn_mm2": conductor_area,
            "gross_copper_section_required_mm2": gross_copper_section,
            "intercell_axial_gap_mm": intercell_gap,
            "modelled_coil_height_mm": nominal_coil_height,
            "available_intercell_section_before_fill_factor_mm2": available_section,
            "required_to_available_section_ratio": gross_copper_section / available_section,
            "note": "This is a packaging finding, not an added A5c band. Insulation and fill factor make the deficit larger.",
        },
        "bands": bands,
        "band_count": len(bands),
        "band_pass_count": sum(bands.values()),
        "failed_bands": failed,
        "screen_pass": all(bands.values()),
        "disposition": "REJECT_GEN1_WINDING_PACKAGE_AND_REVISE_MAGNETIC_INTERFACE",
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
