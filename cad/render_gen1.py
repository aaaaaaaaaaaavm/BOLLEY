"""Render reproducible Gen1 CAD evidence views from the CadQuery source model."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import build_gen1


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cad" / "renders" / "gen1"
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

    fig = plt.figure(figsize=(16, 10), dpi=100, facecolor="#f7f9fc")
    ax = fig.add_subplot(111, projection="3d", facecolor="#f7f9fc")
    for shape, color, alpha in items:
        mesh = Poly3DCollection(
            triangles(shape),
            facecolors=color,
            edgecolors="#0f172a" if alpha >= 0.95 else "none",
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


def generate() -> None:
    import cadquery as cq

    p = build_gen1.load_parameters()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    aluminium = "#94a3b8"
    fluxfoil = "#0891b2"
    core = "#263238"
    phase = ("#f59e0b", "#ef4444", "#3b82f6")
    frame = "#334155"
    gate = "#7c3aed"
    collision = "#dc2626"

    body = build_gen1.payload_proxy(cq, p, include_interface=False)
    interface = build_gen1.fluxfoil_interface(cq, p)
    payload = build_gen1.payload_proxy(cq, p)
    top_core, top_phases = build_gen1.stator_cassette(cq, p, "z+")
    track = build_gen1.track(cq, p)
    retained_gate = build_gen1.retention_gate(cq, p)

    records = []

    def make(filename, items, bounds, view, title, note, evidence):
        path = OUTPUT / filename
        render_scene(items, bounds, view, title, note, path)
        records.append(
            {
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "evidence": evidence,
                "source": "cad/build_gen1.py + cad/gen1_parameters.json",
            }
        )

    make(
        "01_fluxfoil_payload.png",
        [(body, aluminium, 0.78), (interface, fluxfoil, 1.0)],
        ((-12, 353), (-72, 72), (-72, 72)),
        (22, -62),
        "Bolley Gen1 cooperative payload interface",
        "Four passive aluminium Fluxfoil blades per face; +x is the departure axis.",
        "nominal geometry",
    )

    make(
        "02_stator_cassette.png",
        [(top_core, core, 1.0), *[(item, phase[i], 0.95) for i, item in enumerate(top_phases)]],
        ((-12, 924), (-20, 20), (43, 68)),
        (24, -66),
        "Gen1 57-cell serpentine stator cassette",
        "Dark: magnetic circuit. Orange/red/blue: phase winding envelopes.",
        "nominal geometry",
    )

    coupon_p = json.loads(json.dumps(p))
    coupon_p["payload"]["envelope_length_x_mm"] = 96.0
    coupon_p["fluxfoil"]["active_length_x_mm"] = 96.0
    coupon_p["fluxfoil"]["active_length_start_x_mm"] = 0.0
    coupon_body = build_gen1.payload_proxy(cq, coupon_p, include_interface=False)
    coupon_interface = build_gen1.fluxfoil_interface(cq, coupon_p)
    coupon_core, coupon_phases = build_gen1.stator_cassette(cq, coupon_p, "z+", 6)
    make(
        "03_six_cell_coupon.png",
        [
            (coupon_body, aluminium, 0.28),
            (coupon_interface, fluxfoil, 1.0),
            (coupon_core, core, 1.0),
            *[(item, phase[i], 0.95) for i, item in enumerate(coupon_phases)],
        ],
        ((-8, 104), (-22, 22), (38, 69)),
        (28, -58),
        "A3 six-cell one-face coupon",
        "The coupon resolves the repeating cell and makes the Gen1 collision inspectable.",
        "nominal geometry",
    )

    interference_p = json.loads(json.dumps(p))
    interference_p["payload"]["envelope_length_x_mm"] = 15.5
    interference_p["fluxfoil"]["active_length_x_mm"] = 15.5
    interference_p["fluxfoil"]["active_length_start_x_mm"] = 0.0
    interference_body = build_gen1.payload_proxy(cq, interference_p, include_interface=False)
    interference_interface = build_gen1.fluxfoil_interface(cq, interference_p)
    interference_payload = build_gen1.payload_proxy(cq, interference_p)
    interference_core, interference_phases = build_gen1.stator_cassette(
        cq, interference_p, "z+", 1
    )
    interference = build_gen1.compound(
        cq, [interference_payload.intersect(item) for item in interference_phases]
    )
    make(
        "04_winding_interference.png",
        [
            (interference_interface, fluxfoil, 0.38),
            (interference_core, core, 0.25),
            *[(item, phase[i], 0.18) for i, item in enumerate(interference_phases)],
            (interference, collision, 1.0),
        ],
        ((-1, 17), (-18, 18), (42, 67)),
        (0, 0),
        "A5c winding interference — axial cross-section",
        "Red is the first-slot winding overlap. The nominal core/foil clearance itself is valid.",
        "rejected nominal fit",
    )

    assembly_items = [(track, frame, 0.18), (retained_gate, gate, 0.7), (payload, aluminium, 0.65)]
    for face in ("z+", "z-", "y+", "y-"):
        face_core, face_phases = build_gen1.stator_cassette(cq, p, face, 6)
        assembly_items.append((face_core, core, 0.9))
        assembly_items.extend((item, phase[i], 0.72) for i, item in enumerate(face_phases))
    make(
        "05_retained_assembly.png",
        assembly_items,
        ((-55, 380), (-85, 85), (-85, 85)),
        (23, -58),
        "Gen1 retained assembly — breech end",
        "Six cells per face are resolved here for legibility; the master cassette contains 57.",
        "arrangement view",
    )

    departing = build_gen1.payload_proxy(cq, p, x_offset=p["render"]["departing_payload_position_x_mm"])
    make(
        "06_departure_axis.png",
        [(track, frame, 0.22), (retained_gate, gate, 0.55), (departing, fluxfoil, 0.9)],
        ((-55, 1220), (-90, 90), (-90, 90)),
        (12, -74),
        "Positive-x departure and open muzzle",
        "The payload translates toward the 1000 mm muzzle station; no negative-x ejection.",
        "kinematic arrangement view",
    )

    MANIFEST.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generation": "Gen1",
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
        raise SystemExit("missing cad/renders/gen1/RENDERS.json")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["render_count"] < 5:
        raise SystemExit("Gen1 render set has fewer than five views")
    for record in manifest["renders"]:
        path = ROOT / record["path"]
        if not path.exists() or path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise SystemExit(f"stale Gen1 render: {path.relative_to(ROOT)}")
    print("OK: Gen1 renders match RENDERS.json")


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
