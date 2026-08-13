"""Build Bolley Gen1 native CAD and a reproducible artifact manifest.

STEP is the master exchange geometry. STL is a derived browser/preview mesh. Analysis scripts,
not CAD volume, remain authoritative for mass and performance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / "cad"
PARAMETERS = CAD / "gen1_parameters.json"
STEP_DIR = CAD / "step" / "gen1"
STL_DIR = CAD / "stl" / "gen1"
MANIFEST = CAD / "BUILD.json"
PART_NAMES = (
    "Bolley_Fluxfoil_Interface_Gen1",
    "Bolley_Payload_Proxy_Gen1",
    "Bolley_Stator_Cassette_Gen1",
    "Bolley_Track_Gen1",
    "Bolley_Retention_Gate_Gen1",
    "Bolley_A3_Coupon_Gen1",
    "Bolley_Assembly_Gen1",
)


def load_parameters() -> dict:
    with PARAMETERS.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def box_at(cq, x: float, y: float, z: float, dx: float, dy: float, dz: float):
    return cq.Workplane("XY").box(dx, dy, dz).translate((x + dx / 2, y + dy / 2, z + dz / 2)).val()


def compound(cq, shapes):
    solids = []
    for shape in shapes:
        solids.extend(shape.Solids())
    return cq.Compound.makeCompound(solids)


def rotate_face(shape, face: str):
    if face == "z+":
        return shape
    if face == "z-":
        return shape.rotate((0, 0, 0), (1, 0, 0), 180)
    if face == "y+":
        return shape.rotate((0, 0, 0), (1, 0, 0), -90)
    if face == "y-":
        return shape.rotate((0, 0, 0), (1, 0, 0), 90)
    raise ValueError(face)


def fluxfoil_interface(cq, p: dict, x_offset: float = 0.0):
    payload = p["payload"]
    foil = p["fluxfoil"]
    x0 = x_offset + foil["active_length_start_x_mm"]
    length = foil["active_length_x_mm"]
    projection = foil["total_projection_mm"]
    thickness = foil["fin_thickness_mm"]
    centres = foil["fin_centres_across_face_mm"]
    root_width = foil["root_strip_width_mm"]
    root_depth = foil["root_strip_depth_mm"]
    face = payload["envelope_y_mm"] / 2
    shapes = []

    shapes.append(box_at(cq, x0, -root_width / 2, face - root_depth, length, root_width, root_depth))
    shapes.append(box_at(cq, x0, -root_width / 2, -face, length, root_width, root_depth))
    shapes.append(box_at(cq, x0, face - root_depth, -root_width / 2, length, root_depth, root_width))
    shapes.append(box_at(cq, x0, -face, -root_width / 2, length, root_depth, root_width))

    for centre in centres:
        shapes.append(box_at(cq, x0, centre - thickness / 2, face, length, thickness, projection))
        shapes.append(box_at(cq, x0, centre - thickness / 2, -face - projection, length, thickness, projection))
        shapes.append(box_at(cq, x0, face, centre - thickness / 2, length, projection, thickness))
        shapes.append(box_at(cq, x0, -face - projection, centre - thickness / 2, length, projection, thickness))
    return compound(cq, shapes)


def payload_proxy(cq, p: dict, x_offset: float = 0.0, include_interface: bool = True):
    payload = p["payload"]
    length = payload["envelope_length_x_mm"]
    body = payload["proxy_body_yz_mm"]
    rail = payload["corner_rail_width_mm"]
    outer = payload["envelope_y_mm"]
    shapes = [box_at(cq, x_offset, -body / 2, -body / 2, length, body, body)]
    for sy in (-1, 1):
        for sz in (-1, 1):
            y0 = -outer / 2 if sy < 0 else outer / 2 - rail
            z0 = -outer / 2 if sz < 0 else outer / 2 - rail
            shapes.append(box_at(cq, x_offset, y0, z0, length, rail, rail))
    if include_interface:
        shapes.append(fluxfoil_interface(cq, p, x_offset))
    return compound(cq, shapes)


def stator_cell_parts(cq, p: dict, index: int):
    payload = p["payload"]
    stator = p["stator"]
    x = stator["active_start_x_mm"] + index * stator["phase_cell_pitch_x_mm"]
    dx = stator["phase_cell_core_length_x_mm"]
    face = payload["envelope_z_mm"] / 2
    projection = p["fluxfoil"]["total_projection_mm"]
    z0 = face
    y_min = -stator["face_footprint_mm"] / 2
    core_shapes = []
    core_shapes.append(box_at(cq, x, y_min, z0, dx, stator["outer_return_leg_width_mm"], stator["core_radial_height_mm"]))
    core_shapes.append(box_at(cq, x, -y_min - stator["outer_return_leg_width_mm"], z0, dx, stator["outer_return_leg_width_mm"], stator["core_radial_height_mm"]))
    separator_starts = (-5.0, -1.0, 3.0)
    for y in separator_starts:
        core_shapes.append(box_at(cq, x, y, z0, dx, stator["interior_separator_width_mm"], projection))
    core_shapes.append(box_at(cq, x, y_min, z0 + projection, dx, stator["face_footprint_mm"], stator["back_yoke_thickness_mm"]))

    coil_y = y_min - 3.0
    coil_z = z0 - 1.0
    coil_outer = box_at(cq, x, coil_y, coil_z, dx, stator["coil_pack_outer_width_mm"], stator["coil_pack_outer_height_mm"])
    inner_y = coil_y + (stator["coil_pack_outer_width_mm"] - stator["coil_pack_inner_width_mm"]) / 2
    inner_z = coil_z + (stator["coil_pack_outer_height_mm"] - stator["coil_pack_inner_height_mm"]) / 2
    coil_inner = box_at(cq, x - 0.1, inner_y, inner_z, dx + 0.2, stator["coil_pack_inner_width_mm"], stator["coil_pack_inner_height_mm"])
    coil = coil_outer.cut(coil_inner)
    return compound(cq, core_shapes), coil


def stator_cassette(cq, p: dict, face: str = "z+", cell_count: int | None = None):
    count = cell_count if cell_count is not None else p["stator"]["cell_count_per_face"]
    core, phases = [], [[], [], []]
    for index in range(count):
        cell_core, coil = stator_cell_parts(cq, p, index)
        core.append(cell_core)
        phases[index % 3].append(coil)
    core_shape = rotate_face(compound(cq, core), face)
    phase_shapes = [rotate_face(compound(cq, group), face) for group in phases]
    return core_shape, phase_shapes


def track(cq, p: dict):
    track_p = p["track"]
    x0 = track_p["start_x_mm"]
    length = track_p["length_x_mm"]
    guide = track_p["guide_bar_size_mm"]
    offset = track_p["guide_bar_centre_offset_yz_mm"]
    bar = track_p["enclosure_frame_bar_mm"]
    enclosure = track_p["enclosure_outer_yz_mm"]
    corner = track_p["enclosure_longeron_offset_yz_mm"]
    shapes = []
    for sy in (-1, 1):
        for sz in (-1, 1):
            shapes.append(box_at(cq, x0, sy * offset - guide / 2, sz * offset - guide / 2, length, guide, guide))
            shapes.append(box_at(cq, x0, sy * corner - bar / 2, sz * corner - bar / 2, length, bar, bar))
    for x in track_p["hoop_x_positions_mm"]:
        shapes.extend(
            [
                box_at(cq, x, -enclosure / 2, -enclosure / 2, bar, enclosure, bar),
                box_at(cq, x, -enclosure / 2, enclosure / 2 - bar, bar, enclosure, bar),
                box_at(cq, x, -enclosure / 2, -enclosure / 2 + bar, bar, bar, enclosure - 2 * bar),
                box_at(cq, x, enclosure / 2 - bar, -enclosure / 2 + bar, bar, bar, enclosure - 2 * bar),
            ]
        )
    return compound(cq, shapes)


def retention_gate(cq, p: dict):
    gate = p["gate"]
    x = gate["station_x_mm"]
    dx = gate["axial_thickness_mm"]
    outer = gate["frame_outer_yz_mm"]
    inner = gate["frame_inner_yz_mm"]
    frame = box_at(cq, x, -outer / 2, -outer / 2, dx, outer, outer).cut(
        box_at(cq, x - 0.1, -inner / 2, -inner / 2, dx + 0.2, inner, inner)
    )
    pin = gate["retractable_pin_size_mm"]
    pads = [
        box_at(cq, x, -inner / 2, -pin / 2, dx, 12.0, pin),
        box_at(cq, x, inner / 2 - 12.0, -pin / 2, dx, 12.0, pin),
        box_at(cq, x, -pin / 2, -inner / 2, dx, pin, 12.0),
        box_at(cq, x, -pin / 2, inner / 2 - 12.0, dx, pin, 12.0),
    ]
    return compound(cq, [frame, *pads])


def coupon(cq, p: dict):
    coupon_p = p["coupon"]
    short = json.loads(json.dumps(p))
    short["payload"]["envelope_length_x_mm"] = coupon_p["active_length_x_mm"]
    short["payload"]["corner_rail_length_mm"] = coupon_p["active_length_x_mm"]
    short["fluxfoil"]["active_length_x_mm"] = coupon_p["active_length_x_mm"]
    short["fluxfoil"]["active_length_start_x_mm"] = 0.0
    interface = fluxfoil_interface(cq, short)
    top_core, top_phases = stator_cassette(cq, short, "z+", coupon_p["phase_cell_count"])
    support = box_at(
        cq,
        -10.0,
        -coupon_p["support_plate_width_mm"] / 2,
        -70.0,
        coupon_p["support_plate_length_x_mm"],
        coupon_p["support_plate_width_mm"],
        coupon_p["support_plate_thickness_mm"],
    )
    body_wall = box_at(cq, 0.0, -20.0, 45.0, coupon_p["active_length_x_mm"], 40.0, 5.0)
    return compound(cq, [interface, top_core, *top_phases, support, body_wall])


def build_shapes(cq, p: dict):
    interface = fluxfoil_interface(cq, p)
    payload = payload_proxy(cq, p)
    top_core, top_phases = stator_cassette(cq, p)
    cassette = compound(cq, [top_core, *top_phases])
    track_shape = track(cq, p)
    gate_shape = retention_gate(cq, p)
    coupon_shape = coupon(cq, p)
    assembly_parts = [track_shape, gate_shape, payload]
    for face in ("z+", "z-", "y+", "y-"):
        core, phases = stator_cassette(cq, p, face)
        assembly_parts.extend([core, *phases])
    assembly = compound(cq, assembly_parts)
    return {
        PART_NAMES[0]: interface,
        PART_NAMES[1]: payload,
        PART_NAMES[2]: cassette,
        PART_NAMES[3]: track_shape,
        PART_NAMES[4]: gate_shape,
        PART_NAMES[5]: coupon_shape,
        PART_NAMES[6]: assembly,
    }


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


def build() -> None:
    try:
        import cadquery as cq
    except ImportError as error:
        raise SystemExit("CadQuery is required; install requirements-cad.txt") from error
    p = load_parameters()
    STEP_DIR.mkdir(parents=True, exist_ok=True)
    STL_DIR.mkdir(parents=True, exist_ok=True)
    shapes = build_shapes(cq, p)
    payload = shapes[PART_NAMES[1]]
    top_core, top_phases = stator_cassette(cq, p, "z+")
    nominal_intersection_mm3 = payload.intersect(top_core).Volume() + sum(
        payload.intersect(phase).Volume() for phase in top_phases
    )
    records = {}
    for name, shape in shapes.items():
        step_path = STEP_DIR / f"{name}.step"
        stl_path = STL_DIR / f"{name}.stl"
        cq.exporters.export(shape, str(step_path))
        cq.exporters.export(shape, str(stl_path), tolerance=0.15, angularTolerance=0.2)
        record = shape_record(shape)
        record["step"] = {
            "path": str(step_path.relative_to(ROOT)),
            "bytes": step_path.stat().st_size,
            "sha256": sha256(step_path),
        }
        record["stl"] = {
            "path": str(stl_path.relative_to(ROOT)),
            "bytes": stl_path.stat().st_size,
            "sha256": sha256(stl_path),
        }
        records[name] = record
    manifest = {
        "schema_version": 1,
        "generation": p["generation"],
        "evidence": "PARAMETRIC CAD OUTPUT from ASSUMPTION geometry; no manufacturing release",
        "parameter_file": str(PARAMETERS.relative_to(ROOT)),
        "parameter_sha256": sha256(PARAMETERS),
        "master_format": "STEP",
        "derived_format": "STL",
        "coordinate_frame": p["coordinate_frame"],
        "fit_checks": {
            "departure_axis": "+x",
            "nominal_payload_stator_intersection_per_face_mm3": nominal_intersection_mm3,
            "nominal_payload_stator_intersection_all_four_faces_mm3": 4.0
            * nominal_intersection_mm3,
            "nominal_slot_clearance_per_side_mm": (
                p["stator"]["slot_width_mm"] - p["fluxfoil"]["fin_thickness_mm"]
            )
            / 2.0,
            "muzzle_opening_yz_mm": p["track"]["enclosure_outer_yz_mm"]
            - 2.0 * p["track"]["enclosure_frame_bar_mm"],
            "stator_face_count": 4,
        },
        "artifacts": records,
        "limits": [
            "Geometry and fit only; analysis scripts remain authoritative for mass and performance.",
            "Coils are solid envelopes, not individual turns or insulation stacks.",
            "Fasteners, laminations, cooling, sensors, cabling and gate actuation are absent.",
            "The payload is an envelope proxy, not a spacecraft design.",
            "The Gen1 coil envelope intersects the first foil channel; A5c records this as a rejected packaging result.",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("cad/BUILD.json does not exist; run cad/build_gen1.py --write")
    with MANIFEST.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest["parameter_sha256"] != sha256(PARAMETERS):
        raise SystemExit("cad/BUILD.json is stale relative to cad/gen1_parameters.json")
    expected = set(PART_NAMES)
    found = set(manifest["artifacts"])
    if found != expected:
        raise SystemExit(f"CAD artifact set mismatch: expected {sorted(expected)}, found {sorted(found)}")
    artifact_paths = [
        ROOT / record[kind]["path"]
        for record in manifest["artifacts"].values()
        for kind in ("step", "stl")
    ]
    present_count = sum(path.exists() for path in artifact_paths)
    if present_count == 0:
        print(
            "OK: Gen1 manifest is current; rejected exports are not tracked "
            "(run cad/build_gen1.py --write to regenerate them)"
        )
        return
    if present_count != len(artifact_paths):
        missing = [str(path.relative_to(ROOT)) for path in artifact_paths if not path.exists()]
        raise SystemExit(f"partial Gen1 CAD export set; missing {missing}")
    for record in manifest["artifacts"].values():
        for kind in ("step", "stl"):
            path = ROOT / record[kind]["path"]
            if not path.exists():
                raise SystemExit(f"missing CAD artifact: {path.relative_to(ROOT)}")
            if path.stat().st_size != record[kind]["bytes"] or sha256(path) != record[kind]["sha256"]:
                raise SystemExit(f"modified CAD artifact: {path.relative_to(ROOT)}")
    print("OK: Gen1 STEP/STL files match cad/BUILD.json")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")
    build() if args.write else check()


if __name__ == "__main__":
    main()
