"""Render indexed Gen3 Fluxrelay CAD evidence from my native source model."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import build_gen2 as geometry
import build_gen3


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cad" / "renders" / "gen3"
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


def discrete_top_fin_materials(cq, p: dict, centre: float = -8.0):
    payload = p["payload"]
    blade = p["fluxbridge"]
    coupon = p["coupon"]
    y0 = centre - blade["fin_gross_thickness_mm"] / 2.0
    material_y = y0 + blade["encapsulant_per_side_mm"]
    z0 = payload["envelope_z_mm"] / 2.0
    length = coupon["active_length_x_mm"]
    root = blade["root_bus_height_mm"]
    active = blade["active_bar_height_mm"]
    copper = [
        geometry.box_at(cq, 0.0, material_y, z0, length, blade["magnetic_active_width_mm"], root),
        geometry.box_at(
            cq,
            0.0,
            material_y,
            z0 + root + active,
            length,
            blade["magnetic_active_width_mm"],
            blade["tip_bus_height_mm"],
        ),
    ]
    magnetic = []
    for index in range(coupon["cage_bar_period_count"]):
        bx = index * blade["bar_pitch_x_mm"]
        magnetic.append(
            geometry.box_at(
                cq,
                bx,
                material_y,
                z0 + root,
                blade["bar_axial_width_mm"],
                blade["magnetic_backstrap_width_mm"],
                active,
            )
        )
        copper.append(
            geometry.box_at(
                cq,
                bx,
                material_y + blade["magnetic_backstrap_width_mm"],
                z0 + root,
                blade["bar_axial_width_mm"],
                blade["copper_rung_width_mm"],
                active,
            )
        )
        magnetic.append(
            geometry.box_at(
                cq,
                bx + blade["bar_axial_width_mm"],
                material_y,
                z0 + root,
                blade["magnetic_ligament_axial_width_mm"],
                blade["magnetic_active_width_mm"],
                active,
            )
        )
    skins = [
        geometry.box_at(
            cq,
            0.0,
            y0,
            z0,
            length,
            blade["encapsulant_per_side_mm"],
            blade["encapsulated_total_projection_mm"],
        ),
        geometry.box_at(
            cq,
            0.0,
            y0 + blade["fin_gross_thickness_mm"] - blade["encapsulant_per_side_mm"],
            z0,
            length,
            blade["encapsulant_per_side_mm"],
            blade["encapsulated_total_projection_mm"],
        ),
    ]
    return (
        geometry.compound(cq, magnetic),
        geometry.compound(cq, copper),
        geometry.compound(cq, skins),
    )


def generate() -> None:
    import cadquery as cq

    p = build_gen3.load()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    silver = "#94a3b8"
    relay = "#0891b2"
    magnetic = "#334155"
    copper = "#d97706"
    dielectric = "#67e8f9"
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
                "source": "cad/build_gen3.py + cad/gen3_parameters.json",
            }
        )

    body = build_gen3.payload_proxy(cq, p, include_interface=False)
    interface = build_gen3.fluxrelay_interface(cq, p)
    track = geometry.track(cq, p)
    retained_gate = geometry.retention_gate(cq, p)

    hero_items = [(track, frame, 0.13), (retained_gate, gate, 0.72), (body, silver, 0.55), (interface, relay, 1.0)]
    for face_name in ("z+", "z-", "y+", "y-"):
        face_core, face_phases = build_gen3.stator_cassette(cq, p, face_name, 4)
        hero_items.append((face_core, core, 0.92))
        hero_items.extend((item, phase[index], 0.88) for index, item in enumerate(face_phases))
    make(
        "01_gen3_hero.png",
        hero_items,
        ((-55, 360), (-85, 85), (-85, 85)),
        (22, -58),
        "Bolley Gen3 — Fluxrelay launcher",
        "Exact selected payload cage, sectional primary cells and independent retained-state gate.",
        "arrangement view; four master cells per face shown for legibility",
    )

    make(
        "02_fluxrelay_payload.png",
        [(body, silver, 0.62), (interface, relay, 1.0)],
        ((-10, 350), (-70, 70), (-70, 70)),
        (23, -62),
        "Gen3 cooperative payload interface",
        "Twenty finished lanes span 318.6 mm and begin 2.25 mm from the aft face.",
    )

    bar_matrix, bar_copper, bar_skins = discrete_top_fin_materials(cq, p)
    make(
        "03_discrete_fluxrelay_lane.png",
        [(bar_matrix, magnetic, 1.0), (bar_copper, copper, 1.0), (bar_skins, dielectric, 0.48)],
        ((-2, 102), (-10, -5.5), (49, 58)),
        (14, -58),
        "Discrete Fluxrelay coupon lane",
        "Fifty periods resolve copper rungs, magnetic backstraps/ligaments and 0.03 mm side skins.",
        "bar-resolved coupon geometry",
    )

    two_core, two_phases = build_gen3.stator_cassette(cq, p, "z+", 2)
    short = json.loads(json.dumps(p))
    short["payload"]["envelope_length_x_mm"] = 100.0
    short["fluxbridge"]["active_length_x_mm"] = 100.0
    short["fluxbridge"]["active_length_start_x_mm"] = 0.0
    one_face = build_gen3.fluxrelay_interface(cq, short, faces=("z+",))
    make(
        "04_alternating_coil_layers.png",
        [(one_face, relay, 0.35), (two_core, core, 0.82), *[(item, phase[index], 0.96) for index, item in enumerate(two_phases)]],
        ((-8, 100), (-27, 15), (47, 83)),
        (18, -55),
        "Two-cell Gen3 winding route",
        "Volume-matched 5.2 × 8.0 mm copper packs alternate radial layers without solid overlap.",
    )

    full_core, full_phases = build_gen3.stator_cassette(cq, p)
    make(
        "05_full_stator_cassette.png",
        [(full_core, core, 1.0), *[(item, phase[index], 0.92) for index, item in enumerate(full_phases)]],
        ((-20, 1240), (-30, 18), (48, 82)),
        (22, -66),
        "Complete 27-cell Fluxrelay cassette",
        "Twenty-seven cells, nine per phase, 45.3 mm pitch and 1.2231 m installed active length.",
    )

    window_core, window_phases = build_gen3.stator_cassette(cq, p, cell_count=9)
    make(
        "06_sectional_active_window.png",
        [(window_core, core, 1.0), *[(item, phase[index], 0.94) for index, item in enumerate(window_phases)]],
        ((-10, 420), (-30, 18), (48, 82)),
        (20, -62),
        "Nine-cell sectional active window",
        "The conservative window contains three cells per phase; the other installed cells remain cold.",
        "sectional-drive arrangement geometry",
    )

    coupon_wall = geometry.box_at(cq, 0.0, -24.0, 45.0, 100.0, 48.0, 5.0)
    coupon_support = geometry.box_at(cq, -10.0, -37.5, p["coupon"]["support_plate_z_mm"], 120.0, 75.0, 8.0)
    make(
        "07_two_cell_coupon.png",
        [
            (coupon_wall, silver, 0.36),
            (bar_matrix, magnetic, 1.0),
            (bar_copper, copper, 1.0),
            (bar_skins, dielectric, 0.32),
            (two_core, core, 0.9),
            *[(item, phase[index], 0.94) for index, item in enumerate(two_phases)],
            (coupon_support, frame, 0.68),
        ],
        ((-14, 112), (-58, 58), (34, 84)),
        (17, -57),
        "A3 Fluxrelay two-cell coupon",
        "One bar-resolved face, both winding layers, a payload-face surrogate and support plate.",
        "test-article arrangement geometry",
    )

    retained_items = [(track, frame, 0.15), (retained_gate, gate, 0.68), (body, silver, 0.52), (interface, relay, 0.95)]
    for face_name in ("z+", "z-", "y+", "y-"):
        face_core, face_phases = build_gen3.stator_cassette(cq, p, face_name, 4)
        retained_items.append((face_core, core, 0.9))
        retained_items.extend((item, phase[index], 0.8) for index, item in enumerate(face_phases))
    make(
        "08_retained_assembly.png",
        retained_items,
        ((-55, 360), (-85, 85), (-85, 85)),
        (20, -58),
        "Retained Gen3 assembly — breech end",
        "Four independently driven faces surround the passive interface without nominal overlap.",
        "arrangement view; four master cells per face shown for legibility",
    )

    endpoint_payload = build_gen3.payload_proxy(cq, p, x_offset=900.0)
    make(
        "09_endpoint_engagement.png",
        [(full_core, core, 0.22), *[(item, phase[index], 0.20) for index, item in enumerate(full_phases)], (endpoint_payload, relay, 0.92)],
        ((-20, 1250), (-72, 72), (45, 84)),
        (10, -72),
        "Powered-travel endpoint",
        "After 900 mm travel, the 318.6 mm cage retains the frozen 2.25 mm overlap guard.",
        "kinematic arrangement view; one stator face",
    )

    make(
        "10_axial_fit_section.png",
        [(one_face, relay, 0.72), (two_core, core, 0.34), *[(item, phase[index], 0.54) for index, item in enumerate(two_phases)]],
        ((-8, 54), (-27, 16), (47, 82)),
        (0, 0),
        "Gen3 nominal fit section",
        "Five 1.18 mm lanes sit in 1.58 mm slots; the lower coil layer clears the tips by 0.75 mm.",
        "nominal fit geometry",
    )

    MANIFEST.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generation": "Gen3",
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
        raise SystemExit("missing cad/renders/gen3/RENDERS.json")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["render_count"] < 10:
        raise SystemExit("Gen3 render set has fewer than ten views")
    for record in manifest["renders"]:
        path = ROOT / record["path"]
        if not path.exists() or path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise SystemExit(f"stale Gen3 render: {path.relative_to(ROOT)}")
    print("OK: Gen3 renders match RENDERS.json")


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
