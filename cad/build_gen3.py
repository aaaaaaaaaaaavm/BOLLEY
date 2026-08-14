"""Build my Bolley Gen3 Fluxrelay CAD and reproducible evidence manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import build_gen2 as geometry


ROOT = Path(__file__).resolve().parents[1]
CAD = ROOT / "cad"
PARAMETERS = CAD / "gen3_parameters.json"
A8B_RESULT = ROOT / "analysis" / "results" / "gen27_codesign.json"
A6H_RESULT = ROOT / "analysis" / "results" / "gen27_field.json"
A7C_RESULT = ROOT / "analysis" / "results" / "gen27_cage_circuit.json"
STEP_DIR = CAD / "step" / "gen3"
STL_DIR = CAD / "stl" / "gen3"
MANIFEST = CAD / "BUILD_GEN3.json"
PART_NAMES = (
    "Bolley_Fluxrelay_Interface_Gen3",
    "Bolley_Payload_Proxy_Gen3",
    "Bolley_Stator_Cassette_Gen3",
    "Bolley_Sectional_Window_Gen3",
    "Bolley_Track_Gen3",
    "Bolley_Retention_Gate_Gen3",
    "Bolley_A3_Fluxrelay_Coupon_Gen3",
    "Bolley_Assembly_Gen3",
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


def top_blade_components(cq, p: dict, centre: float, x0: float, length: float, discrete: bool):
    payload = p["payload"]
    blade = p["fluxbridge"]
    thickness = blade["fin_gross_thickness_mm"]
    skin = blade["encapsulant_per_side_mm"]
    active_width = blade["magnetic_active_width_mm"]
    y0 = centre - thickness / 2.0
    z0 = payload["envelope_z_mm"] / 2.0
    total_projection = blade["encapsulated_total_projection_mm"]
    root_bus = blade["root_bus_height_mm"]
    active_height = blade["active_bar_height_mm"]
    tip_bus = blade["tip_bus_height_mm"]
    shapes = [
        geometry.box_at(cq, x0, y0, z0, length, skin, total_projection),
        geometry.box_at(
            cq,
            x0,
            y0 + thickness - skin,
            z0,
            length,
            skin,
            total_projection,
        ),
    ]
    if not discrete:
        material_y = y0 + skin
        shapes.extend(
            [
                geometry.box_at(
                    cq,
                    x0,
                    material_y,
                    z0,
                    length,
                    blade["homogenized_magnetic_layer_mm"],
                    total_projection,
                ),
                geometry.box_at(
                    cq,
                    x0,
                    material_y + blade["homogenized_magnetic_layer_mm"],
                    z0,
                    length,
                    blade["homogenized_copper_layer_mm"],
                    total_projection,
                ),
            ]
        )
        return shapes

    material_y = y0 + skin
    shapes.extend(
        [
            geometry.box_at(cq, x0, material_y, z0, length, active_width, root_bus),
            geometry.box_at(
                cq,
                x0,
                material_y,
                z0 + root_bus + active_height,
                length,
                active_width,
                tip_bus,
            ),
        ]
    )
    periods = int(round(length / blade["bar_pitch_x_mm"]))
    for index in range(periods):
        bx = x0 + index * blade["bar_pitch_x_mm"]
        shapes.extend(
            [
                geometry.box_at(
                    cq,
                    bx,
                    material_y,
                    z0 + root_bus,
                    blade["bar_axial_width_mm"],
                    blade["magnetic_backstrap_width_mm"],
                    active_height,
                ),
                geometry.box_at(
                    cq,
                    bx,
                    material_y + blade["magnetic_backstrap_width_mm"],
                    z0 + root_bus,
                    blade["bar_axial_width_mm"],
                    blade["copper_rung_width_mm"],
                    active_height,
                ),
                geometry.box_at(
                    cq,
                    bx + blade["bar_axial_width_mm"],
                    material_y,
                    z0 + root_bus,
                    blade["magnetic_ligament_axial_width_mm"],
                    active_width,
                    active_height,
                ),
            ]
        )
    return shapes


def fluxrelay_interface(
    cq,
    p: dict,
    x_offset: float = 0.0,
    discrete: bool = False,
    faces: tuple[str, ...] = ("z+", "z-", "y+", "y-"),
):
    payload = p["payload"]
    blade = p["fluxbridge"]
    x0 = x_offset + blade["active_length_start_x_mm"]
    length = blade["active_length_x_mm"]
    face = payload["envelope_y_mm"] / 2.0
    root_width = blade["root_capture_strip_width_mm"]
    root_depth = blade["root_capture_strip_depth_mm"]
    shapes = []
    for face_name in faces:
        if face_name == "z+":
            shapes.append(geometry.box_at(cq, x0, -root_width / 2, face - root_depth, length, root_width, root_depth))
        elif face_name == "z-":
            shapes.append(geometry.box_at(cq, x0, -root_width / 2, -face, length, root_width, root_depth))
        elif face_name == "y+":
            shapes.append(geometry.box_at(cq, x0, face - root_depth, -root_width / 2, length, root_depth, root_width))
        else:
            shapes.append(geometry.box_at(cq, x0, -face, -root_width / 2, length, root_depth, root_width))
    for centre in blade["fin_centres_across_face_mm"]:
        top = geometry.compound(cq, top_blade_components(cq, p, centre, x0, length, discrete))
        if "z+" in faces:
            shapes.append(top)
        if "z-" in faces:
            shapes.append(top.rotate((0, 0, 0), (1, 0, 0), 180))
        if "y+" in faces:
            shapes.append(top.rotate((0, 0, 0), (1, 0, 0), -90))
        if "y-" in faces:
            shapes.append(top.rotate((0, 0, 0), (1, 0, 0), 90))
    return geometry.compound(cq, shapes)


def payload_proxy(cq, p: dict, x_offset: float = 0.0, include_interface: bool = True):
    payload = p["payload"]
    length = payload["envelope_length_x_mm"]
    body = payload["proxy_body_yz_mm"]
    rail = payload["corner_rail_width_mm"]
    outer = payload["envelope_y_mm"]
    shapes = [geometry.box_at(cq, x_offset, -body / 2, -body / 2, length, body, body)]
    for sy in (-1, 1):
        for sz in (-1, 1):
            y0 = -outer / 2 if sy < 0 else outer / 2 - rail
            z0 = -outer / 2 if sz < 0 else outer / 2 - rail
            shapes.append(geometry.box_at(cq, x_offset, y0, z0, length, rail, rail))
    if include_interface:
        shapes.append(fluxrelay_interface(cq, p, x_offset=x_offset))
    return geometry.compound(cq, shapes)


def stator_cassette(cq, p: dict, face: str = "z+", cell_count: int | None = None):
    return geometry.stator_cassette(cq, p, face, cell_count)


def coupon(cq, p: dict):
    q = p["coupon"]
    short = json.loads(json.dumps(p))
    short["payload"]["envelope_length_x_mm"] = q["active_length_x_mm"]
    short["fluxbridge"]["active_length_x_mm"] = q["active_length_x_mm"]
    short["fluxbridge"]["active_length_start_x_mm"] = 0.0
    discrete = fluxrelay_interface(cq, short, discrete=True, faces=("z+",))
    wall = geometry.box_at(
        cq,
        0.0,
        -24.0,
        short["payload"]["envelope_z_mm"] / 2.0 - 5.0,
        q["active_length_x_mm"],
        48.0,
        5.0,
    )
    core, phases = stator_cassette(cq, short, "z+", q["stator_cell_count"])
    support = geometry.box_at(
        cq,
        -10.0,
        -q["support_plate_width_mm"] / 2.0,
        q["support_plate_z_mm"],
        q["support_plate_length_x_mm"],
        q["support_plate_width_mm"],
        q["support_plate_thickness_mm"],
    )
    return geometry.compound(cq, [wall, discrete, core, *phases, support])


def build_shapes(cq, p: dict):
    interface = fluxrelay_interface(cq, p)
    payload = payload_proxy(cq, p)
    top_core, top_phases = stator_cassette(cq, p)
    cassette = geometry.compound(cq, [top_core, *top_phases])
    window_core, window_phases = stator_cassette(
        cq, p, cell_count=p["sectional_drive"]["active_window_cell_count"]
    )
    window = geometry.compound(cq, [window_core, *window_phases])
    track_shape = geometry.track(cq, p)
    gate_shape = geometry.retention_gate(cq, p)
    coupon_shape = coupon(cq, p)
    assembly_parts = [track_shape, gate_shape, payload]
    for face in ("z+", "z-", "y+", "y-"):
        core, phases = stator_cassette(cq, p, face)
        assembly_parts.extend([core, *phases])
    return {
        PART_NAMES[0]: interface,
        PART_NAMES[1]: payload,
        PART_NAMES[2]: cassette,
        PART_NAMES[3]: window,
        PART_NAMES[4]: track_shape,
        PART_NAMES[5]: gate_shape,
        PART_NAMES[6]: coupon_shape,
        PART_NAMES[7]: geometry.compound(cq, assembly_parts),
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
    a8b = load(A8B_RESULT)
    selected = a8b["selected_candidate"]
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
    coil_shapes = [
        geometry.coil_pack(cq, p, index)
        for index in range(p["stator"]["cell_count_per_face"])
    ]
    adjacent_coil_overlap = sum(
        coil_shapes[index].intersect(coil_shapes[index + 1]).Volume()
        for index in range(len(coil_shapes) - 1)
    )
    coil_core_overlap = sum(shape.intersect(core).Volume() for shape in coil_shapes)
    expected_copper_volume = (
        selected["design"]["installed_primary_copper_mass_kg"] / 8960.0 * 1e9
    )
    cad_coil_volume = sum(shape.Volume() for shape in coil_shapes) * 4.0
    endpoint_guard = (
        p["stator"]["active_length_x_mm"]
        - p["sectional_drive"]["powered_travel_mm"]
        - p["fluxbridge"]["active_length_start_x_mm"]
        - p["fluxbridge"]["active_length_x_mm"]
    )
    fit = {
        "departure_axis": "+x",
        "stator_face_count": 4,
        "payload_core_intersection_per_face_mm3": core_intersection,
        "payload_coil_intersection_per_face_mm3": coil_intersection,
        "payload_stator_intersection_all_faces_mm3": 4.0 * (core_intersection + coil_intersection),
        "adjacent_coil_overlap_per_face_mm3": adjacent_coil_overlap,
        "coil_core_intersection_per_face_mm3": coil_core_overlap,
        "nominal_fin_clearance_per_side_mm": (
            p["stator"]["foil_slot_width_mm"]
            - p["fluxbridge"]["fin_gross_thickness_mm"]
        )
        / 2.0,
        "minimum_coil_to_fluxbridge_radial_clearance_mm": (
            p["stator"]["coil_lower_radial_start_mm"]
            - p["fluxbridge"]["encapsulated_total_projection_mm"]
        ),
        "muzzle_opening_yz_mm": p["track"]["enclosure_outer_yz_mm"]
        - 2.0 * p["track"]["enclosure_frame_bar_mm"],
        "endpoint_overlap_guard_mm": endpoint_guard,
        "active_window_cell_count": p["sectional_drive"]["active_window_cell_count"],
        "active_window_cells_per_phase": p["sectional_drive"]["active_window_cells_per_phase"],
        "coil_envelope_volume_all_four_faces_mm3": cad_coil_volume,
        "a8b_installed_copper_volume_all_four_faces_mm3": expected_copper_volume,
        "coil_volume_relative_error": cad_coil_volume / expected_copper_volume - 1.0,
        "discrete_coupon_bar_period_count": p["coupon"]["cage_bar_period_count"],
        "discrete_coupon_stator_cell_count": p["coupon"]["stator_cell_count"],
    }
    manifest = {
        "schema_version": 1,
        "generation": p["generation"],
        "evidence": "PARAMETRIC CAD OUTPUT from the A6h/A7c-passing selected point; no manufacturing release",
        "parameter_file": str(PARAMETERS.relative_to(ROOT)),
        "parameter_sha256": sha256(PARAMETERS),
        "source_results": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (A8B_RESULT, A6H_RESULT, A7C_RESULT)
        },
        "selected_candidate_id": selected["candidate_id"],
        "master_format": "STEP",
        "derived_format": "STL",
        "coordinate_frame": p["coordinate_frame"],
        "fit_checks": fit,
        "artifacts": records,
        "limits": [
            "Full-length Fluxrelay blades remain homogenized; the coupon resolves magnetic webs, copper rungs and side encapsulant.",
            "Coils are volume-matched copper solids, not individual turns, insulation, impregnation, leads or terminals.",
            "Fasteners, lamination plies, cooling, sensors, cabling and gate actuation are absent.",
            "The 16 kg active-material band is not a packaged launcher-mass allowance.",
            "The payload is an envelope proxy, not a spacecraft design.",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("cad/BUILD_GEN3.json does not exist; run cad/build_gen3.py --write")
    manifest = load(MANIFEST)
    if manifest["parameter_sha256"] != sha256(PARAMETERS):
        raise SystemExit("cad/BUILD_GEN3.json is stale relative to cad/gen3_parameters.json")
    for path in (A8B_RESULT, A6H_RESULT, A7C_RESULT):
        key = str(path.relative_to(ROOT))
        if manifest["source_results"].get(key) != sha256(path):
            raise SystemExit(f"cad/BUILD_GEN3.json is stale relative to {key}")
    if set(manifest["artifacts"]) != set(PART_NAMES):
        raise SystemExit("Gen3 CAD artifact set mismatch")
    step_paths = [ROOT / record["step"]["path"] for record in manifest["artifacts"].values()]
    stl_paths = [ROOT / record["stl"]["path"] for record in manifest["artifacts"].values()]
    step_present = sum(path.exists() for path in step_paths)
    stl_present = sum(path.exists() for path in stl_paths)
    if step_present == 0 and stl_present == 0:
        print("OK: Gen3 manifest is current; exports can be regenerated with cad/build_gen3.py --write")
        return
    if step_present not in (0, len(step_paths)) or stl_present not in (0, len(stl_paths)):
        raise SystemExit("partial Gen3 STEP/STL export set")
    for record in manifest["artifacts"].values():
        for kind in ("step", "stl"):
            path = ROOT / record[kind]["path"]
            if not path.exists():
                continue
            if path.stat().st_size != record[kind]["bytes"] or sha256(path) != record[kind]["sha256"]:
                raise SystemExit(f"modified Gen3 CAD artifact: {path.relative_to(ROOT)}")
    if step_present == 0:
        print("OK: Gen3 tracked STL previews match the manifest; regenerate STEP masters from source")
    else:
        print("OK: Gen3 STEP/STL files match cad/BUILD_GEN3.json")


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
