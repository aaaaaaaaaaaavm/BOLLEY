"""Index every repository figure by source, evidence class and disposition."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GEN1 = ROOT / "cad" / "renders" / "gen1" / "RENDERS.json"
GEN2 = ROOT / "cad" / "renders" / "gen2" / "RENDERS.json"
A6 = ROOT / "analysis" / "figures" / "a6" / "FIGURES.json"
A6B = ROOT / "analysis" / "figures" / "a6b" / "FIGURES.json"
A6C = ROOT / "analysis" / "figures" / "a6c" / "FIGURES.json"
A6D = ROOT / "analysis" / "figures" / "a6d" / "FIGURES.json"
A6E = ROOT / "analysis" / "figures" / "a6e" / "FIGURES.json"
A6F = ROOT / "analysis" / "figures" / "a6f" / "FIGURES.json"
A7A = ROOT / "analysis" / "figures" / "a7a" / "FIGURES.json"
A6G = ROOT / "analysis" / "figures" / "a6g" / "FIGURES.json"
A7B = ROOT / "analysis" / "figures" / "a7b" / "FIGURES.json"
A8A = ROOT / "analysis" / "figures" / "a8a" / "FIGURES.json"
A8B = ROOT / "analysis" / "figures" / "a8b" / "FIGURES.json"
OUTPUT = ROOT / "docs" / "FIGURE_INDEX.md"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def render() -> str:
    rows = [
        ("F01", "A3a unit-cell candidates", "cad/a3a_unit_cells.svg", "Hand-authored parametric schematic", "Historical topology screen"),
        ("F02", "A5a comb-fin cross-section", "cad/a5a_comb_fin_cross_section.svg", "Hand-authored dimensional schematic", "Rejected architecture evidence"),
    ]
    for prefix, manifest_path, disposition in (
        ("G1", GEN1, "Rejected Gen1 package evidence"),
        ("G2", GEN2, "A5d nominal geometry; A6 operating point rejected"),
    ):
        for index, record in enumerate(load(manifest_path)["renders"], start=1):
            name = Path(record["path"]).stem.replace("_", " ").title()
            rows.append(
                (
                    f"{prefix}-{index:02d}",
                    name,
                    record["path"],
                    f"Rendered parametric CAD — {record['evidence']}",
                    disposition,
                )
            )
    for gate, manifest_path, evidence_prefix, disposition in (
        ("A6", A6, "2D nonlinear field-model output", "Rejected Gen2 operating-point evidence"),
        ("A6b", A6B, "2D nonlinear field-model output", "Rejected exact Gen2.1 geometry evidence"),
        ("A6c", A6C, "2D nonlinear field-model output", "Rejected Gen2.2 ligament evidence"),
        ("A6d", A6D, "2D nonlinear field-model output", "Rejected Gen2.3 rib evidence"),
        ("A6e", A6E, "2D nonlinear field-model output", "Rejected Gen2.4 local-peak evidence"),
        ("A6f", A6F, "2D nonlinear field-model output", "Passing Gen2.5 transverse-field screen; downstream gates open"),
        ("A7a", A7A, "Post-field cage/circuit model output", "Rejected exact Gen2.5 cage/circuit evidence"),
        ("A6g", A6G, "2D nonlinear field-model output", "Passing Gen2.6 Quintweb transverse-field screen"),
        ("A7b", A7B, "Post-field cage/circuit model output", "Rejected exact Gen2.6 hot-resistance circuit evidence"),
        ("A8a", A8A, "Axial engagement model output", "Rejected exact Gen2.6 axial-package evidence"),
        ("A8b", A8B, "Coupled design-space model output", "Selected Gen2.7 analytical point; field reclosure open"),
    ):
        if not manifest_path.exists():
            continue
        for index, record in enumerate(load(manifest_path)["figures"], start=1):
            rows.append(
                (
                    f"{gate}-{index:02d}",
                    record["title"],
                    record["path"],
                    f"{evidence_prefix} — {record['evidence']}",
                    disposition,
                )
            )
    lines = [
        "# Figure index",
        "",
        "> I index every figure by its generating source and evidence class. I do not present any",
        "> figure in this repository as test observation or flight evidence.",
        "",
        "| ID | Figure | Source | Evidence class | Disposition |",
        "|---|---|---|---|---|",
    ]
    for identifier, name, path, evidence, disposition in rows:
        relative = Path(path)
        target = "../" + relative.as_posix()
        lines.append(
            f"| {identifier} | [{name}]({target}) | `{path}` | {evidence} | {disposition} |"
        )
    lines.extend(
        [
            "",
            "## Evidence count",
            "",
            f"- Indexed figures: **{len(rows)}**.",
            f"- Parametric/model/schematic figures: **{len(rows)}**.",
            "- Physically observed figures: **0**.",
            "",
            "I use a render to explain topology or nominal fit. I do not use it to close force, field,",
            "thermal, structural, tolerance, wear, vacuum or release evidence without the corresponding result.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.write:
        OUTPUT.write_text(content, encoding="utf-8")
    elif args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("stale generated file: docs/FIGURE_INDEX.md")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
