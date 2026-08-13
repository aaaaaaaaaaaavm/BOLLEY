"""Render indexed Gen2 CAD evidence views from the native source model."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import build_gen2


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cad" / "renders" / "gen2"
MANIFEST = OUTPUT / "RENDERS.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def triangles(shape, tolerance: float = 0.8):
    vertices, faces = shape.tessellate(tolerance)
    points = [(vertex.x, vertex.y, vertex.z) for vertex in vertices]
    return [[points[index] for index in face] for face in faces]


def render_scene(items, bounds, view, title: str, note: str, path: Path) -> None:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure(figsize=(16, 10), dpi=100, facecolor="#f8fafc")
    ax = fig.add_subplot(111, projection="3d", facecolor="#f8fafc")
    for shape, color, alpha in items:
        mesh = Poly3DCollection(
            triangles(shape),
            facecolors=color,
            edgecolors="#0f172a" if alpha >= 0.9 else "none",
            linewidths=0.08,
            alpha=alpha,
        )
        ax.add_collection3d(mesh)
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)
    ax.set_box_aspect((xmax - xmin, ymax - ymin, zmax - zmin))
    ax.view_init(elev=view[0], azim=view[1], roll=0)
    ax.set_axis_off()
    fig.text(0.055, 0.94, title, fontsize=22, weight="bold", color="#0f172a")
    fig.text(0.056, 0.905, note, fontsize=11, color="#475569")
    fig.text(
        0.945,
        0.04,
        "PARAMETRIC CAD — NOT A MANUFACTURING RELEASE",
        ha="right",
        fontsize=9,
        color="#64748b",
    )
    fig.savefig(path, bbox_inches="tight", pad_inches=0.25, facecolor=fig.get_facecolor())
    plt.close(fig)


def discrete_top_fin_materials(cq, p: dict, centre: float = -4.8):
    payload = p["payload"]
    b = p["fluxbridge"]
    q = p["coupon"]
    x0 = 0.0
    y0 = centre - b["fin_gross_thickness_mm"] / 2.0
    z0 = payload["envelope_z_mm"] / 2.0
    length = q["active_length_x_mm"]
    copper = [
        build_gen2.box_at(cq, x0, y0, z0, length, b["fin_gross_thickness_mm"], b["root_bus_height_mm"]),
        build_gen2.box_at(
            cq,
            x0,
            y0,
            z0 + b["root_bus_height_mm"] + b["active_bar_height_mm"],
            length,
            b["fin_gross_thickness_mm"],
            b["tip_bus_height_mm"],
        ),
    ]
    magnetic = []
    for index in range(q["cage_bar_period_count"]):
        bx = x0 + index * b["bar_pitch_x_mm"]
        copper.append(
            build_gen2.box_at(
                cq,
                bx,
                y0,
                z0 + b["root_bus_height_mm"],
                b["bar_axial_width_mm"],
                b["fin_gross_thickness_mm"],
                b["active_bar_height_mm"],
            )
        )
        magnetic.append(
            build_gen2.box_at(
                cq,
                bx + b["bar_axial_width_mm"],
                y0,
                z0 + b["root_bus_height_mm"],
                b["magnetic_ligament_axial_width_mm"],
                b["fin_gross_thickness_mm"],
                b["active_bar_height_mm"],
            )
        )
    return build_gen2.compound(cq, magnetic), build_gen2.compound(cq, copper)


def generate() -> None:
    import cadquery as cq

    p = build_gen2.load()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    silver = "#94a3b8"
    bridge = "#0891b2"
    magnetic = "#334155"
    copper = "#d97706"
    core = "#172554"
    phase = ("#f59e0b", "#ef4444", "#2563eb")
    frame = "#475569"
    gate = "#7c3aed"
    records = []

    def make(filename, items, bounds, view, title, note, evidence="nominal geometry"):
        path = OUTPUT / filename
        render_scene(items, bounds, view, title, note, path)
        records.append(
            {
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "evidence": evidence,
                "source": "cad/build_gen2.py + cad/gen2_parameters.json",
            }
        )

    body = build_gen2.payload_proxy(cq, p, include_interface=False)
    interface = build_gen2.fluxbridge_interface(cq, p)
    payload = build_gen2.payload_proxy(cq, p)
    track = build_gen2.track(cq, p)
    retained_gate = build_gen2.retention_gate(cq, p)

    hero_items = [(track, frame, 0.15), (retained_gate, gate, 0.72), (body, silver, 0.55), (interface, bridge, 1.0)]
    for face_name in ("z+", "z-", "y+", "y-"):
        face_core, face_phases = build_gen2.stator_cassette(cq, p, face_name, 5)
        hero_items.append((face_core, core, 0.92))
        hero_items.extend((item, phase[index], 0.88) for index, item in enumerate(face_phases))
    make(
        "01_gen2_hero.png",
        hero_items,
        ((-55, 355), (-85, 85), (-85, 85)),
        (22, -58),
        "Bolley Gen2 — Fluxbridge launcher",
        "Passive cage payload, alternating-layer stator, independent retained-state gate.",
        "arrangement view; five master cells per face shown for legibility",
    )

    make(
        "02_fluxbridge_payload.png",
        [(body, silver, 0.62), (interface, bridge, 1.0)],
        ((-10, 350), (-70, 70), (-70, 70)),
        (23, -62),
        "Gen2 cooperative payload interface",
        "Full-length blades use the A3g homogenized magnetic/copper representation.",
    )

    short = json.loads(json.dumps(p))
    short["payload"]["envelope_length_x_mm"] = p["coupon"]["active_length_x_mm"]
    bar_matrix, bar_copper = discrete_top_fin_materials(cq, p)
    make(
        "03_discrete_fluxbridge_bar.png",
        [(bar_matrix, magnetic, 1.0), (bar_copper, copper, 1.0)],
        ((-2, 62), (-8, -1.5), (48, 58)),
        (14, -58),
        "Discrete Fluxbridge coupon blade",
        "Thirty copper rungs over 60 mm; dark ligaments carry transverse magnetic flux.",
        "bar-resolved coupon geometry",
    )

    two_core, two_phases = build_gen2.stator_cassette(cq, p, "z+", 2)
    short_bridge = json.loads(json.dumps(p))
    short_bridge["payload"]["envelope_length_x_mm"] = 60.0
    short_bridge["fluxbridge"]["active_length_x_mm"] = 60.0
    short_bridge["fluxbridge"]["active_length_start_x_mm"] = 0.0
    one_face_bridge = build_gen2.fluxbridge_interface(cq, short_bridge, faces=("z+",))
    make(
        "04_alternating_coil_layers.png",
        [(one_face_bridge, bridge, 0.38), (two_core, core, 0.82), *[(item, phase[index], 0.96) for index, item in enumerate(two_phases)]],
        ((-14, 63), (-22, 12), (47, 81)),
        (18, -55),
        "Two-cell alternating-layer winding",
        "Adjacent 39 × 23 × 9 mm pack envelopes overlap axially but occupy separate radial layers.",
    )

    full_core, full_phases = build_gen2.stator_cassette(cq, p)
    make(
        "05_full_stator_cassette.png",
        [(full_core, core, 1.0), *[(item, phase[index], 0.92) for index, item in enumerate(full_phases)]],
        ((-20, 915), (-23, 13), (48, 80)),
        (22, -66),
        "Complete 30-cell Gen2 stator cassette",
        "Thirty cells, ten per phase, 30 mm pitch and 0.900 m active length.",
    )

    coupon_wall = build_gen2.box_at(cq, 0.0, -20.0, 45.0, 60.0, 40.0, 5.0)
    coupon_support = build_gen2.box_at(
        cq,
        -10.0,
        -32.5,
        p["coupon"]["support_plate_z_mm"],
        80.0,
        65.0,
        8.0,
    )
    make(
        "06_two_cell_coupon.png",
        [
            (coupon_wall, silver, 0.38),
            (bar_matrix, magnetic, 1.0),
            (bar_copper, copper, 1.0),
            (two_core, core, 0.9),
            *[(item, phase[index], 0.94) for index, item in enumerate(two_phases)],
            (coupon_support, frame, 0.68),
        ],
        ((-14, 70), (-52, 52), (34, 82)),
        (17, -57),
        "A3 Fluxbridge two-cell coupon",
        "One bar-resolved face, both winding layers, payload-face surrogate and support plate.",
        "test-article arrangement geometry",
    )

    retained_items = [(track, frame, 0.18), (retained_gate, gate, 0.68), (body, silver, 0.52), (interface, bridge, 0.95)]
    for face_name in ("z+", "z-", "y+", "y-"):
        face_core, face_phases = build_gen2.stator_cassette(cq, p, face_name, 4)
        retained_items.append((face_core, core, 0.9))
        retained_items.extend((item, phase[index], 0.8) for index, item in enumerate(face_phases))
    make(
        "07_retained_assembly.png",
        retained_items,
        ((-55, 360), (-85, 85), (-85, 85)),
        (20, -58),
        "Retained Gen2 assembly — breech end",
        "Four independently driven faces surround the passive interface without solid overlap.",
        "arrangement view; four master cells per face shown for legibility",
    )

    departing = build_gen2.payload_proxy(cq, p, x_offset=850.0)
    make(
        "08_positive_x_departure.png",
        [(track, frame, 0.22), (retained_gate, gate, 0.50), (departing, bridge, 0.92)],
        ((-55, 1220), (-90, 90), (-90, 90)),
        (12, -74),
        "Positive-x departure through the open muzzle",
        "The payload translates toward the 1000 mm muzzle station; the gate remains with the host.",
        "kinematic arrangement view",
    )

    make(
        "09_axial_fit_section.png",
        [(one_face_bridge, bridge, 0.78), (two_core, core, 0.38), *[(item, phase[index], 0.55) for index, item in enumerate(two_phases)]],
        ((-13, 26), (-22, 13), (47, 80)),
        (0, 0),
        "Gen2 axial fit section",
        "Four 1.0 mm blades sit in 1.4 mm slots; the lower coil layer starts 0.75 mm above the tips.",
        "nominal fit geometry",
    )

    MANIFEST.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generation": "Gen2",
                "evidence": "RENDERED PARAMETRIC CAD; not measurement or manufacturing release",
                "render_count": len(records),
                "renders": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("missing cad/renders/gen2/RENDERS.json")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["render_count"] < 7:
        raise SystemExit("Gen2 render set has fewer than seven views")
    for record in manifest["renders"]:
        path = ROOT / record["path"]
        if not path.exists() or path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise SystemExit(f"stale Gen2 render: {path.relative_to(ROOT)}")
    print("OK: Gen2 renders match RENDERS.json")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")
    generate() if args.write else check()


if __name__ == "__main__":
    main()
