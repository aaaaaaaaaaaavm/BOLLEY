"""Build my A5h detailed 12-turn Gen3 winding CAD and evidence manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / "cad"
sys.path.insert(0, str(CAD))
import build_gen2 as geometry  # noqa: E402


PARAMETERS = CAD / "gen3_12turn_detailed_parameters.json"
GEN3 = CAD / "gen3_parameters.json"
A5G = ROOT / "analysis" / "results" / "gen3_12turn_path_fit.json"
STEP_DIR = CAD / "step" / "gen3_12turn"
STL_DIR = CAD / "stl" / "gen3_12turn"
MANIFEST = CAD / "BUILD_GEN3_12TURN.json"
PART_NAMES = (
    "Bolley_12Turn_Cell_Gen3",
    "Bolley_12Turn_ABC_Module_Gen3",
    "Bolley_12Turn_FullFace_Winding_Gen3",
    "Bolley_12Turn_FullFace_CoreAndWinding_Gen3",
)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def winding_cell(cq, gen3: dict, selected: dict, index: int):
    stator = gen3["stator"]
    payload = gen3["payload"]
    turns = selected["in_plane_turns_per_radial_layer"]
    radial_layers = selected["radial_layers"]
    conductor_width = selected["insulated_overall_width_mm"]
    conductor_thickness = selected["insulated_overall_thickness_mm"]
    inner_x = selected["inner_axial_span_mm"]
    inner_y = selected["inner_transverse_span_mm"]
    radial_height = radial_layers * conductor_width
    centre_x = (
        stator["active_start_x_mm"]
        + index * stator["cell_pitch_x_mm"]
        + stator["tooth_axial_width_mm"] / 2.0
    )
    centre_y = (
        -stator["core_face_footprint_mm"] / 2.0
        + stator["outer_return_leg_width_mm"] / 2.0
    )
    lower_z = payload["envelope_z_mm"] / 2.0 + selected["lower_coil_start_above_payload_face_mm"]
    layer_offset = radial_height + selected["interlayer_radial_clearance_mm"]
    z_base = lower_z + (index % 2) * layer_offset

    solids = []
    for radial_index in range(radial_layers):
        z0 = z_base + radial_index * conductor_width
        for in_plane_index in range(turns):
            outer_x = inner_x + 2.0 * (in_plane_index + 1) * conductor_thickness
            outer_y = inner_y + 2.0 * (in_plane_index + 1) * conductor_thickness
            x0 = centre_x - outer_x / 2.0
            y0 = centre_y - outer_y / 2.0
            solids.append(
                geometry.rectangular_ring_x(
                    cq,
                    x0,
                    y0,
                    z0,
                    outer_x,
                    outer_y,
                    conductor_width,
                    conductor_thickness,
                )
            )
    return geometry.compound(cq, solids)


def winding_set(cq, gen3: dict, selected: dict, count: int):
    return geometry.compound(
        cq, [winding_cell(cq, gen3, selected, index) for index in range(count)]
    )


def core_set(cq, gen3: dict, count: int):
    return geometry.compound(
        cq, [geometry.stator_core_cell(cq, gen3, index) for index in range(count)]
    )


def shape_record(shape) -> dict:
    bounds = shape.BoundingBox()
    return {
        "solid_count": len(shape.Solids()),
        "volume_mm3": shape.Volume(),
        "bounding_box_mm": {
            "x": [bounds.xmin, bounds.xmax],
            "y": [bounds.ymin, bounds.ymax],
            "z": [bounds.zmin, bounds.zmax],
            "size": [bounds.xlen, bounds.ylen, bounds.zlen],
        },
    }


def build() -> dict:
    try:
        import cadquery as cq
    except ImportError as error:
        raise SystemExit("CadQuery is required; install requirements-cad.txt") from error

    controlled = load(PARAMETERS)
    gen3 = load(GEN3)
    a5g = load(A5G)
    if not a5g["screen_pass"]:
        raise SystemExit("A5h requires the passing A5g point")
    a5g_selected = a5g["selected_candidate"]
    frozen = controlled["selected_winding"]
    for key, source_key in (
        ("bare_width_mm", "bare_width_mm"),
        ("bare_thickness_mm", "bare_thickness_mm"),
        ("insulated_overall_width_mm", "insulated_overall_width_mm"),
        ("insulated_overall_thickness_mm", "insulated_overall_thickness_mm"),
        ("inner_axial_span_mm", "solved_inner_axial_span_mm"),
        ("inner_transverse_span_mm", "fixed_inner_transverse_span_mm"),
    ):
        if abs(frozen[key] - a5g_selected[source_key]) > 1e-12:
            raise SystemExit(f"A5h frozen {key} no longer matches A5g")

    one = winding_cell(cq, gen3, frozen, 0)
    abc = winding_set(cq, gen3, frozen, controlled["cad_scope"]["abc_module_cell_count"])
    full = winding_set(cq, gen3, frozen, controlled["cad_scope"]["full_face_cell_count"])
    cores = core_set(cq, gen3, controlled["cad_scope"]["full_face_cell_count"])
    combined = geometry.compound(cq, [cores, full])
    shapes = {
        PART_NAMES[0]: one,
        PART_NAMES[1]: abc,
        PART_NAMES[2]: full,
        PART_NAMES[3]: combined,
    }

    STEP_DIR.mkdir(parents=True, exist_ok=True)
    STL_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = {}
    for name, shape in shapes.items():
        step_path = STEP_DIR / f"{name}.step"
        stl_path = STL_DIR / f"{name}.stl"
        cq.exporters.export(shape, str(step_path))
        cq.exporters.export(shape, str(stl_path), tolerance=0.12, angularTolerance=0.2)
        item = shape_record(shape)
        item["step"] = {
            "path": str(step_path.relative_to(ROOT)),
            "bytes": step_path.stat().st_size,
            "sha256": sha256(step_path),
        }
        item["stl"] = {
            "path": str(stl_path.relative_to(ROOT)),
            "bytes": stl_path.stat().st_size,
            "sha256": sha256(stl_path),
        }
        artifacts[name] = item

    coil_core_intersection = full.intersect(cores).Volume()
    consecutive_intersection = 0.0
    same_layer_intersection = 0.0
    cells = [
        winding_cell(cq, gen3, frozen, index)
        for index in range(controlled["cad_scope"]["full_face_cell_count"])
    ]
    for index in range(len(cells) - 1):
        consecutive_intersection += cells[index].intersect(cells[index + 1]).Volume()
    for index in range(len(cells) - 2):
        same_layer_intersection += cells[index].intersect(cells[index + 2]).Volume()

    payload_face = gen3["payload"]["envelope_z_mm"] / 2.0
    coil_to_fluxrelay = (
        frozen["lower_coil_start_above_payload_face_mm"]
        - gen3["fluxbridge"]["encapsulated_total_projection_mm"]
    )
    radial_height = (
        frozen["radial_layers"] * frozen["insulated_overall_width_mm"]
    )
    upper_end_above_face = (
        frozen["lower_coil_start_above_payload_face_mm"]
        + 2.0 * radial_height
        + frozen["interlayer_radial_clearance_mm"]
    )
    upper_to_yoke = gen3["stator"]["back_yoke_radial_start_mm"] - upper_end_above_face

    result = {
        "schema_version": 1,
        "evidence": "A5h DETAILED MAXIMUM-INSULATION CONDUCTOR-ENVELOPE CAD; nominal only",
        "parameter_file": str(PARAMETERS.relative_to(ROOT)),
        "parameter_sha256": sha256(PARAMETERS),
        "source_a5g": str(A5G.relative_to(ROOT)),
        "artifacts": artifacts,
        "fit_checks": {
            "turn_solid_count_per_cell": artifacts[PART_NAMES[0]]["solid_count"],
            "full_face_turn_solid_count": artifacts[PART_NAMES[2]]["solid_count"],
            "coil_core_intersection_mm3": coil_core_intersection,
            "consecutive_cell_coil_intersection_mm3": consecutive_intersection,
            "same_layer_coil_intersection_mm3": same_layer_intersection,
            "coil_to_fluxrelay_radial_clearance_mm": coil_to_fluxrelay,
            "interlayer_radial_clearance_mm": frozen["interlayer_radial_clearance_mm"],
            "upper_coil_to_back_yoke_clearance_mm": upper_to_yoke,
            "analytical_copper_volume_per_cell_mm3": a5g_selected["detailed_copper_volume_per_cell_mm3"],
            "analytical_copper_volume_relative_error": a5g_selected["copper_volume_relative_error"],
            "mean_turn_length_mm": a5g_selected["mean_turn_length_mm"],
            "mean_turn_length_relative_error": a5g_selected["mean_turn_length_relative_error"],
            "payload_face_z_mm": payload_face,
        },
    }
    MANIFEST.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build()
        print(json.dumps(result["fit_checks"], indent=2, sort_keys=True))
    else:
        raise SystemExit("use --build")


if __name__ == "__main__":
    main()
