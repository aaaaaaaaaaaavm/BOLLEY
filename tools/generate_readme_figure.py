"""Generate the README architecture roadmap from committed Bolley results."""

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


def main() -> None:
    output = ROOT / "figures" / "architecture-roadmap.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(), encoding="utf-8")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
