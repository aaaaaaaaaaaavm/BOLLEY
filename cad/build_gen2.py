"""Build Bolley Gen2 parametric CAD and its reproducible evidence manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / "cad"
PARAMETERS = CAD / "gen2_parameters.json"
A3G_RESULT = ROOT / "analysis" / "results" / "fluxbridge_optimization.json"
STEP_DIR = CAD / "step" / "gen2"
STL_DIR = CAD / "stl" / "gen2"
MANIFEST = CAD / "BUILD_GEN2.json"
PART_NAMES = (
    "Bolley_Fluxbridge_Interface_Gen2",
    "Bolley_Payload_Proxy_Gen2",
    "Bolley_Stator_Cassette_Gen2",
    "Bolley_Track_Gen2",
    "Bolley_Retention_Gate_Gen2",
    "Bolley_A3_Fluxbridge_Coupon_Gen2",
    "Bolley_Assembly_Gen2",
)


def load(path: Path = PARAMETERS) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def box_at(cq, x: float, y: float, z: float, dx: float, dy: float, dz: float):
    return (
        cq.Workplane("XY")
        .box(dx, dy, dz)
        .translate((x + dx / 2, y + dy / 2, z + dz / 2))
        .val()
    )


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


def rectangular_ring_x(cq, x0, y0, z0, dx_outer, dy_outer, dz, wall):
    outer = box_at(cq, x0, y0, z0, dx_outer, dy_outer, dz)
    inner = box_at(
        cq,
        x0 + wall,
        y0 + wall,
        z0 - 0.1,
        dx_outer - 2.0 * wall,
        dy_outer - 2.0 * wall,
        dz + 0.2,
    )
    return outer.cut(inner)


def fluxbridge_interface(
    cq,
    p: dict,
    x_offset: float = 0.0,
    discrete: bool = False,
    faces: tuple[str, ...] = ("z+", "z-", "y+", "y-"),
):
    payload = p["payload"]
    bridge = p["fluxbridge"]
    x0 = x_offset + bridge["active_length_start_x_mm"]
    length = bridge["active_length_x_mm"]
    face = payload["envelope_y_mm"] / 2.0
    centres = bridge["fin_centres_across_face_mm"]
    thickness = bridge["fin_gross_thickness_mm"]
    root_width = bridge["root_capture_strip_width_mm"]
    root_depth = bridge["root_capture_strip_depth_mm"]
    total_projection = bridge["encapsulated_total_projection_mm"]
    active_height = bridge["active_bar_height_mm"]
    root_bus = bridge["root_bus_height_mm"]
    tip_bus = bridge["tip_bus_height_mm"]
    magnetic_thickness = bridge["homogenized_magnetic_layer_mm"]
    copper_thickness = bridge["homogenized_copper_layer_mm"]
    shapes = []

    for face_name in faces:
        if face_name == "z+":
            shapes.append(box_at(cq, x0, -root_width / 2, face - root_depth, length, root_width, root_depth))
        elif face_name == "z-":
            shapes.append(box_at(cq, x0, -root_width / 2, -face, length, root_width, root_depth))
        elif face_name == "y+":
            shapes.append(box_at(cq, x0, face - root_depth, -root_width / 2, length, root_depth, root_width))
        else:
            shapes.append(box_at(cq, x0, -face, -root_width / 2, length, root_depth, root_width))

    def top_fin_components(centre: float):
        y0 = centre - thickness / 2.0
        z0 = face
        local = []
        if not discrete:
            local.append(box_at(cq, x0, y0, z0, length, magnetic_thickness, total_projection))
            local.append(box_at(cq, x0, y0 + magnetic_thickness, z0, length, copper_thickness, total_projection))
            return local
        local.append(box_at(cq, x0, y0, z0, length, thickness, root_bus))
        local.append(box_at(cq, x0, y0, z0 + root_bus + active_height, length, thickness, tip_bus))
        periods = int(round(length / bridge["bar_pitch_x_mm"]))
        for index in range(periods):
            bx = x0 + index * bridge["bar_pitch_x_mm"]
            local.append(box_at(cq, bx, y0, z0 + root_bus, bridge["bar_axial_width_mm"], thickness, active_height))
            ligament_x = bx + bridge["bar_axial_width_mm"]
            local.append(box_at(cq, ligament_x, y0, z0 + root_bus, bridge["magnetic_ligament_axial_width_mm"], thickness, active_height))
        return local

    for centre in centres:
        top_components = top_fin_components(centre)
        top_shape = compound(cq, top_components)
        if "z+" in faces:
            shapes.append(top_shape)
        if "z-" in faces:
            shapes.append(top_shape.rotate((0, 0, 0), (1, 0, 0), 180))
        if "y+" in faces:
            shapes.append(top_shape.rotate((0, 0, 0), (1, 0, 0), -90))
        if "y-" in faces:
            shapes.append(top_shape.rotate((0, 0, 0), (1, 0, 0), 90))
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
        shapes.append(fluxbridge_interface(cq, p, x_offset=x_offset))
    return compound(cq, shapes)


def stator_core_cell(cq, p: dict, index: int):
    payload = p["payload"]
    s = p["stator"]
    x0 = s["active_start_x_mm"] + index * s["cell_pitch_x_mm"]
    dx = s["tooth_axial_width_mm"]
    y_min = -s["core_face_footprint_mm"] / 2.0
    face = payload["envelope_z_mm"] / 2.0
    shapes = [
        box_at(cq, x0, y_min, face, dx, s["outer_return_leg_width_mm"], s["outer_leg_radial_height_mm"]),
        box_at(cq, x0, -y_min - s["outer_return_leg_width_mm"], face, dx, s["outer_return_leg_width_mm"], s["outer_leg_radial_height_mm"]),
    ]
    for centre in s["slot_centres_across_face_mm"][:-1]:
        separator_y = centre + s["foil_slot_width_mm"] / 2.0
        shapes.append(
            box_at(cq, x0, separator_y, face, dx, s["interior_separator_width_mm"], s["separator_radial_height_mm"])
        )
    shapes.append(
        box_at(cq, x0, y_min, face + s["back_yoke_radial_start_mm"], dx, s["core_face_footprint_mm"], s["back_yoke_thickness_mm"])
    )
    return compound(cq, shapes)


def coil_pack(cq, p: dict, index: int):
    payload = p["payload"]
    s = p["stator"]
    centre_x = (
        s["active_start_x_mm"]
        + index * s["cell_pitch_x_mm"]
        + s["tooth_axial_width_mm"] / 2.0
    )
    centre_y = -s["core_face_footprint_mm"] / 2.0 + s["outer_return_leg_width_mm"] / 2.0
    layer = index % 2
    z0 = payload["envelope_z_mm"] / 2.0 + s["coil_lower_radial_start_mm"] + layer * s["coil_layer_radial_height_mm"]
    x0 = centre_x - s["coil_outer_axial_span_mm"] / 2.0
    y0 = centre_y - s["coil_outer_transverse_span_mm"] / 2.0
    return rectangular_ring_x(
        cq,
        x0,
        y0,
        z0,
        s["coil_outer_axial_span_mm"],
        s["coil_outer_transverse_span_mm"],
        s["coil_layer_radial_height_mm"],
        s["coil_pack_width_mm"],
    )


def stator_cassette(cq, p: dict, face: str = "z+", cell_count: int | None = None):
    count = cell_count if cell_count is not None else p["stator"]["cell_count_per_face"]
    cores, phases = [], [[], [], []]
    for index in range(count):
        cores.append(stator_core_cell(cq, p, index))
        phases[index % 3].append(coil_pack(cq, p, index))
    return (
        rotate_face(compound(cq, cores), face),
        [rotate_face(compound(cq, group), face) for group in phases],
    )


def track(cq, p: dict):
    q = p["track"]
    x0, length = q["start_x_mm"], q["length_x_mm"]
    guide, guide_offset = q["guide_bar_size_mm"], q["guide_bar_centre_offset_yz_mm"]
    bar, enclosure = q["enclosure_frame_bar_mm"], q["enclosure_outer_yz_mm"]
    corner = q["enclosure_longeron_offset_yz_mm"]
    shapes = []
    for sy in (-1, 1):
        for sz in (-1, 1):
            shapes.append(box_at(cq, x0, sy * guide_offset - guide / 2, sz * guide_offset - guide / 2, length, guide, guide))
            shapes.append(box_at(cq, x0, sy * corner - bar / 2, sz * corner - bar / 2, length, bar, bar))
    for x in q["hoop_x_positions_mm"]:
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
    q = p["gate"]
    x, dx = q["station_x_mm"], q["axial_thickness_mm"]
    outer, inner = q["frame_outer_yz_mm"], q["frame_inner_yz_mm"]
    frame = box_at(cq, x, -outer / 2, -outer / 2, dx, outer, outer).cut(
        box_at(cq, x - 0.1, -inner / 2, -inner / 2, dx + 0.2, inner, inner)
    )
    pin = q["retractable_pin_size_mm"]
    pads = [
        box_at(cq, x, -inner / 2, -pin / 2, dx, 12.0, pin),
        box_at(cq, x, inner / 2 - 12.0, -pin / 2, dx, 12.0, pin),
        box_at(cq, x, -pin / 2, -inner / 2, dx, pin, 12.0),
        box_at(cq, x, -pin / 2, inner / 2 - 12.0, dx, pin, 12.0),
    ]
    return compound(cq, [frame, *pads])


def coupon(cq, p: dict):
    q = p["coupon"]
    short = json.loads(json.dumps(p))
    short["payload"]["envelope_length_x_mm"] = q["active_length_x_mm"]
    short["fluxbridge"]["active_length_x_mm"] = q["active_length_x_mm"]
    short["fluxbridge"]["active_length_start_x_mm"] = 0.0
    discrete_bridge = fluxbridge_interface(cq, short, discrete=True, faces=("z+",))
    body_wall = box_at(
        cq,
        0.0,
        -20.0,
        short["payload"]["envelope_z_mm"] / 2.0 - 5.0,
        q["active_length_x_mm"],
        40.0,
        5.0,
    )
    core, phases = stator_cassette(cq, short, "z+", q["stator_cell_count"])
    support = box_at(
        cq,
        -10.0,
        -q["support_plate_width_mm"] / 2.0,
        q["support_plate_z_mm"],
        q["support_plate_length_x_mm"],
        q["support_plate_width_mm"],
        q["support_plate_thickness_mm"],
    )
    return compound(cq, [body_wall, discrete_bridge, core, *phases, support])


def build_shapes(cq, p: dict):
    interface = fluxbridge_interface(cq, p)
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
    return {
        PART_NAMES[0]: interface,
        PART_NAMES[1]: payload,
        PART_NAMES[2]: cassette,
        PART_NAMES[3]: track_shape,
        PART_NAMES[4]: gate_shape,
        PART_NAMES[5]: coupon_shape,
        PART_NAMES[6]: compound(cq, assembly_parts),
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
    p = load()
    a3g = load(A3G_RESULT)
    STEP_DIR.mkdir(parents=True, exist_ok=True)
    STL_DIR.mkdir(parents=True, exist_ok=True)
    shapes = build_shapes(cq, p)
    records = {}
    for name, shape in shapes.items():
        step_path = STEP_DIR / f"{name}.step"
        stl_path = STL_DIR / f"{name}.stl"
        cq.exporters.export(shape, str(step_path))
        cq.exporters.export(shape, str(stl_path), tolerance=0.15, angularTolerance=0.2)
        record = shape_record(shape)
        for kind, path in (("step", step_path), ("stl", stl_path)):
            record[kind] = {
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        records[name] = record

    payload = shapes[PART_NAMES[1]]
    core, phases = stator_cassette(cq, p, "z+")
    core_intersection = payload.intersect(core).Volume()
    coil_intersection = sum(payload.intersect(phase).Volume() for phase in phases)
    coil_shapes = [coil_pack(cq, p, index) for index in range(p["stator"]["cell_count_per_face"])]
    adjacent_coil_overlap = sum(
        coil_shapes[index].intersect(coil_shapes[index + 1]).Volume()
        for index in range(len(coil_shapes) - 1)
    )
    coil_core_overlap = sum(shape.intersect(core).Volume() for shape in coil_shapes)
    expected_copper_volume = (
        a3g["selected_candidate"]["design"]["primary_copper_mass_kg"]
        / 8960.0
        * 1e9
    )
    cad_coil_volume = sum(shape.Volume() for shape in coil_shapes) * 4.0
    volume_error = cad_coil_volume / expected_copper_volume - 1.0
    fit = {
        "departure_axis": "+x",
        "stator_face_count": 4,
        "payload_core_intersection_per_face_mm3": core_intersection,
        "payload_coil_intersection_per_face_mm3": coil_intersection,
        "payload_stator_intersection_all_faces_mm3": 4.0 * (core_intersection + coil_intersection),
        "adjacent_coil_overlap_per_face_mm3": adjacent_coil_overlap,
        "coil_core_intersection_per_face_mm3": coil_core_overlap,
        "nominal_fin_clearance_per_side_mm": (
            p["stator"]["foil_slot_width_mm"] - p["fluxbridge"]["fin_gross_thickness_mm"]
        ) / 2.0,
        "minimum_coil_to_fluxbridge_radial_clearance_mm": (
            p["stator"]["coil_lower_radial_start_mm"]
            - p["fluxbridge"]["encapsulated_total_projection_mm"]
        ),
        "muzzle_opening_yz_mm": p["track"]["enclosure_outer_yz_mm"] - 2.0 * p["track"]["enclosure_frame_bar_mm"],
        "coil_envelope_volume_all_four_faces_mm3": cad_coil_volume,
        "a3g_analytical_copper_volume_all_four_faces_mm3": expected_copper_volume,
        "coil_volume_relative_error": volume_error,
        "discrete_coupon_bar_period_count": p["coupon"]["cage_bar_period_count"],
        "discrete_coupon_stator_cell_count": p["coupon"]["stator_cell_count"],
    }
    manifest = {
        "schema_version": 1,
        "generation": p["generation"],
        "evidence": "PARAMETRIC CAD OUTPUT from A3g-controlled ASSUMPTION geometry; no manufacturing release",
        "parameter_file": str(PARAMETERS.relative_to(ROOT)),
        "parameter_sha256": sha256(PARAMETERS),
        "a3g_result_file": str(A3G_RESULT.relative_to(ROOT)),
        "a3g_result_sha256": sha256(A3G_RESULT),
        "master_format": "STEP",
        "derived_format": "STL",
        "coordinate_frame": p["coordinate_frame"],
        "fit_checks": fit,
        "artifacts": records,
        "limits": [
            "Full-length Fluxbridge blades are homogenized magnetic/copper layers; the coupon resolves discrete bars.",
            "Coils are pack envelopes, not individual turns, insulation, impregnation or terminals.",
            "Fasteners, laminations, cooling, sensors, cabling and gate actuation are absent.",
            "The payload is an envelope proxy, not a spacecraft design.",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("cad/BUILD_GEN2.json does not exist; run cad/build_gen2.py --write")
    manifest = load(MANIFEST)
    if manifest["parameter_sha256"] != sha256(PARAMETERS):
        raise SystemExit("cad/BUILD_GEN2.json is stale relative to cad/gen2_parameters.json")
    if manifest["a3g_result_sha256"] != sha256(A3G_RESULT):
        raise SystemExit("cad/BUILD_GEN2.json is stale relative to the A3g result")
    if set(manifest["artifacts"]) != set(PART_NAMES):
        raise SystemExit("Gen2 CAD artifact set mismatch")
    step_paths = [ROOT / record["step"]["path"] for record in manifest["artifacts"].values()]
    stl_paths = [ROOT / record["stl"]["path"] for record in manifest["artifacts"].values()]
    step_present = sum(path.exists() for path in step_paths)
    stl_present = sum(path.exists() for path in stl_paths)
    if step_present == 0 and stl_present == 0:
        print("OK: Gen2 manifest is current; exports can be regenerated with cad/build_gen2.py --write")
        return
    if step_present not in (0, len(step_paths)) or stl_present not in (0, len(stl_paths)):
        raise SystemExit("partial Gen2 STEP/STL export set")
    for record in manifest["artifacts"].values():
        for kind in ("step", "stl"):
            path = ROOT / record[kind]["path"]
            if not path.exists():
                continue
            if path.stat().st_size != record[kind]["bytes"] or sha256(path) != record[kind]["sha256"]:
                raise SystemExit(f"modified Gen2 CAD artifact: {path.relative_to(ROOT)}")
    if step_present == 0:
        print("OK: Gen2 tracked STL preview set matches manifest; regenerate STEP masters from source")
    else:
        print("OK: Gen2 STEP/STL files match cad/BUILD_GEN2.json")


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
