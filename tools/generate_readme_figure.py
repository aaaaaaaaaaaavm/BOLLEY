"""Generate the README visual set from committed Bolley results."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis" / "results"
BG, PANEL, INK, MUTED = "#07111b", "#0c1d2a", "#e8f0f7", "#8fa7ba"
CYAN, VIOLET, AMBER, RED, GREEN = "#38d6e8", "#9b8cff", "#ffb454", "#ff6b6b", "#61d6a3"


def txt(x: float, y: float, value: str, size: int, colour: str = INK, weight: int = 400,
        anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{colour}" font-family="Inter,Segoe UI,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def box(x: float, y: float, w: float, h: float, stroke: str = "#17384b", fill: str = PANEL,
        radius: int = 18) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def load(name: str) -> dict:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def render() -> str:
    fit = load("gen3_cad_fit.json")
    screen = load("gen456_architecture_screen.json")
    frame = load("fluxframe_mass.json")
    pressure = screen["fluxpiston"]["pressure_cases"]["reference"]["mean_pressure_pa"] / 1000.0
    fit_pass = int(fit["band_pass_count"])
    fit_total = int(fit["band_count"])
    counts = screen["status_counts"]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">',
        f'<rect width="1600" height="900" fill="{BG}"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#3f718c"/></marker></defs>',
        txt(72, 78, "BOLLEY · ONE PREMISE, THREE DIRECTIONS", 24, CYAN, 700),
        txt(72, 124, "Let the spacecraft carry passive hardware. Then price what that concession buys.", 29, INK, 600),
        txt(72, 162, "Phase 0 design study · model and nominal CAD output · no hardware evidence", 19, MUTED),
        box(72, 218, 380, 430, stroke=CYAN),
        txt(104, 264, "GEN3 FLUXRELAY", 17, CYAN, 700),
        txt(104, 306, "Selected analytical point", 24, INK, 650),
        txt(104, 346, "built as parametric CAD", 20, MUTED),
        txt(104, 420, f"{fit_pass}/{fit_total}", 58, INK, 750),
        txt(104, 452, "frozen nominal-fit bands pass", 15, MUTED),
        txt(104, 524, "0", 46, GREEN, 750),
        txt(104, 554, "nominal payload / core / coil intersections", 14, MUTED),
        txt(104, 610, "TOLERANCE · STRUCTURE · COOLING OPEN", 12, AMBER, 700),
    ]
    out.append('<line x1="452" y1="430" x2="520" y2="430" stroke="#3f718c" stroke-width="3" marker-end="url(#arrow)"/>')
    branches = [
        ("GEN4 · CLOSE THE MACHINE", "Keep Fluxrelay", "sectional switching · failed cells · packaged mass", "A9 and packaged closure remain open", CYAN),
        ("GEN5 · FLUXFRAME", "Make interface do bus work", f"needs {frame['required_displaced_mass_kg']:.5f} kg displaced mass", "credit withheld until a selected-bus ledger", VIOLET),
        ("GEN6 · FLUXPISTON", "Move the pulse into gas", f"{pressure:.2f} kPa ideal reference mean pressure", "seal leakage, friction and transients open", AMBER),
    ]
    for i, (title, premise, metric, boundary, colour) in enumerate(branches):
        x, y = 548, 218 + i * 180
        out += [
            box(x, y, 976, 148, stroke=colour),
            txt(x + 28, y + 40, title, 16, colour, 700),
            txt(x + 28, y + 80, premise, 23, INK, 650),
            txt(x + 386, y + 80, metric, 18, INK, 550),
            txt(x + 28, y + 118, boundary.upper(), 13, MUTED, 650),
        ]

    out += [
        box(72, 700, 1452, 118, fill="#091720", stroke="#21465b"),
        txt(104, 744, "A10 ARCHITECTURE SCREEN", 14, CYAN, 700),
        txt(104, 784, f"{counts['PASS']} pass   ·   {counts['FAIL']} fail   ·   {counts['OPEN']} open   ·   {counts['REPORT']} report-only", 27, INK, 650),
        txt(1494, 862, "ALL NUMBERS ARE MODEL OR NOMINAL-CAD OUTPUT", 15, RED, 650, "end"),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def gate_scorecard() -> str:
    architecture = load("gen456_architecture_screen.json")
    flow = load("fluxpiston_flow.json")
    frame = load("fluxframe_mass.json")
    rows = [
        ("A10 · ARCHITECTURE", architecture["status_counts"], 12),
        ("A11 · FLUXPISTON", {"PASS": flow["pass_count"], "FAIL": 0, "OPEN": flow["check_count"] - flow["pass_count"], "REPORT": 0}, flow["check_count"]),
        ("A12 · FLUXFRAME", {"PASS": sum(c["status"] == "PASS" for c in frame["checks"]), "FAIL": sum(c["status"] == "FAIL" for c in frame["checks"]), "OPEN": sum(c["status"] == "OPEN" for c in frame["checks"]), "REPORT": 0}, len(frame["checks"])),
    ]
    colours = {"PASS": GREEN, "FAIL": RED, "OPEN": AMBER, "REPORT": VIOLET}
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="720" viewBox="0 0 1600 720">',
        f'<rect width="1600" height="720" fill="{BG}"/>',
        txt(72, 78, "PROMOTION-GATE SCORECARD", 24, CYAN, 700),
        txt(72, 124, "Passing a screen promotes the question—not the hardware.", 34, INK, 600),
        txt(72, 162, "Three committed result ledgers, kept separate because their gates are different.", 19, MUTED),
        box(72, 220, 1452, 348, stroke="#21465b"),
    ]
    for row_index, (label, counts, total) in enumerate(rows):
        y = 276 + row_index * 92
        out.append(txt(104, y + 20, label, 16, INK, 650))
        x = 430
        for status in ("PASS", "FAIL", "OPEN", "REPORT"):
            value = int(counts.get(status, 0))
            if not value:
                continue
            width = 850 * value / total
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="34" fill="{colours[status]}"/>')
            if width > 60:
                out.append(txt(x + width / 2, y + 23, str(value), 14, BG, 800, "middle"))
            x += width
        out.append(txt(1460, y + 23, f"{total} checks", 14, MUTED, 600, "end"))
    legend_x = 430
    for status in ("PASS", "FAIL", "OPEN", "REPORT"):
        out += [f'<rect x="{legend_x}" y="522" width="18" height="18" rx="4" fill="{colours[status]}"/>', txt(legend_x + 28, 537, status, 13, MUTED, 650)]
        legend_x += 190
    out += [
        box(72, 602, 1452, 58, fill="#1b1116", stroke=RED, radius=12),
        txt(100, 638, "OPEN means evidence still required. REPORT means the screen records a comparison without selecting hardware.", 17, INK, 550),
        "</svg>",
    ]
    return "\n".join(out) + "\n"


def fluxpiston_envelope() -> str:
    result = load("fluxpiston_flow.json")
    grid = result["grid"]
    temperatures = sorted({int(row["temperature_k"]) for row in grid})
    clearances = sorted({row["clearance_m"] for row in grid})
    palette = {temperatures[0]: AMBER, temperatures[1]: CYAN, temperatures[2]: VIOLET}
    ymax = max(row["total_gas_mass_kg"] for row in grid) * 1000.0 * 1.12
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="800" viewBox="0 0 1600 800">',
        f'<rect width="1600" height="800" fill="{BG}"/>',
        txt(72, 78, "FLUXPISTON CLEARANCE ENVELOPE", 24, CYAN, 700),
        txt(72, 124, "Leakage prices clearance directly into gas mass per shot.", 34, INK, 600),
        txt(72, 162, "Ideal-gas and continuum choked-flow screen; seal contact and rarefaction remain open.", 19, MUTED),
    ]
    for panel_index, case_name in enumerate(("reference", "qualification")):
        x, y, w, h = 72 + panel_index * 744, 218, 704, 450
        left, top, plot_w, plot_h = x + 86, y + 72, 570, 286
        out += [box(x, y, w, h), txt(x + 28, y + 42, case_name.upper(), 16, CYAN, 700)]
        for tick in range(5):
            yy = top + plot_h * tick / 4
            value = ymax * (1 - tick / 4)
            out += [f'<line x1="{left}" y1="{yy:.1f}" x2="{left + plot_w}" y2="{yy:.1f}" stroke="#17384b"/>', txt(left - 12, yy + 5, f"{value:.1f}", 12, MUTED, 400, "end")]
        min_c, max_c = min(clearances), max(clearances)
        for clearance in clearances:
            xx = left + plot_w * (clearance - min_c) / (max_c - min_c)
            out.append(txt(xx, top + plot_h + 26, f"{clearance * 1000:.2f}", 11, MUTED, 400, "middle"))
        for temperature in temperatures:
            rows = sorted((row for row in grid if row["case"] == case_name and int(row["temperature_k"]) == temperature), key=lambda row: row["clearance_m"])
            points = []
            for row in rows:
                xx = left + plot_w * (row["clearance_m"] - min_c) / (max_c - min_c)
                yy = top + plot_h * (1 - row["total_gas_mass_kg"] * 1000.0 / ymax)
                points.append(f"{xx:.1f},{yy:.1f}")
            out.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{palette[temperature]}" stroke-width="4"/>')
        out += [txt(left, top - 14, "total gas mass [g]", 13, MUTED), txt(left + plot_w, top + plot_h + 54, "radial clearance [mm]", 13, MUTED, 500, "end")]
    legend_x = 538
    for temperature in temperatures:
        out += [f'<line x1="{legend_x}" y1="716" x2="{legend_x + 38}" y2="716" stroke="{palette[temperature]}" stroke-width="4"/>', txt(legend_x + 50, 722, f"{temperature} K", 14, INK, 600)]
        legend_x += 190
    out += [txt(1494, 766, "MODEL OUTPUT · CONTACT, FRICTION AND PLUME NOT SOLVED", 15, RED, 650, "end"), "</svg>"]
    return "\n".join(out) + "\n"


def main() -> None:
    outputs = {
        ROOT / "figures" / "architecture-roadmap.svg": render(),
        ROOT / "figures" / "gate-scorecard.svg": gate_scorecard(),
        ROOT / "figures" / "fluxpiston-envelope.svg": fluxpiston_envelope(),
    }
    for output, body in outputs.items():
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(body, encoding="utf-8")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
