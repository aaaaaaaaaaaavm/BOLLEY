"""Render A7b cage/circuit corner and CG evidence."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis" / "results" / "gen26_cage_circuit.json"
FIGURE_DIR = ROOT / "analysis" / "figures" / "a7b"
MANIFEST = FIGURE_DIR / "FIGURES.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render() -> None:
    import matplotlib.pyplot as plt

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    points_path = ROOT / result["cg_point_artifact"]["path"]
    with gzip.open(points_path, "rt", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    figures = []

    worst_rows = [
        row
        for row in rows
        if row["corner_index"] == "2" and row["payload_case"] == "qualification"
    ]
    y_values = sorted({float(row["y_cg_m"]) for row in worst_rows})
    z_values = sorted({float(row["z_cg_m"]) for row in worst_rows})
    y_index = {value: index for index, value in enumerate(y_values)}
    z_index = {value: index for index, value in enumerate(z_values)}
    cage_rise = np.empty((len(z_values), len(y_values)))
    for row in worst_rows:
        cage_rise[z_index[float(row["z_cg_m"])]][y_index[float(row["y_cg_m"])]] = float(
            row["maximum_cage_copper_rise_k"]
        )
    path = FIGURE_DIR / "A7b_qualification_cage_rise_map.png"
    fig, ax = plt.subplots(figsize=(8.5, 7), dpi=160)
    image = ax.imshow(
        cage_rise,
        origin="lower",
        extent=[min(y_values) * 1e3, max(y_values) * 1e3, min(z_values) * 1e3, max(z_values) * 1e3],
        aspect="equal",
        cmap="viridis",
        vmin=0.0,
        vmax=20.0,
    )
    ax.set_xlabel("Declared y CG offset [mm]")
    ax.set_ylabel("Declared z CG offset [mm]")
    ax.set_title("A7b qualification cage rise | 90% conductance | 20 K scale")
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.set_label("Maximum channel cage rise [K]")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A7b renderer"})
    plt.close(fig)
    figures.append((path, "Worst-corner qualification cage-temperature CG map", "MODEL OUTPUT"))

    corner_labels = []
    energy_ratios, rise_ratios, current_ratios, efficiency_ratios = [], [], [], []
    for corner in result["corners"]:
        sigma = int(100 * corner["corner"]["cage_sheet_conductance_multiplier"])
        resistance = int(100 * corner["corner"]["phase_resistance_multiplier"])
        corner_labels.append(f"sigma{sigma}/R{resistance}")
        energy_ratios.append(corner["reference"]["maximum_source_energy_j"] / 900.0)
        rise_ratios.append(
            max(
                corner["reference"]["maximum_cage_copper_rise_k"],
                corner["qualification"]["maximum_cage_copper_rise_k"],
            )
            / 20.0
        )
        current_ratios.append(
            max(
                corner["reference"]["maximum_cage_current_density_a_m2"],
                corner["qualification"]["maximum_cage_current_density_a_m2"],
            )
            / 180e6
        )
        efficiency_ratios.append(
            0.5
            / min(
                corner["reference"]["minimum_secondary_only_efficiency"],
                corner["qualification"]["minimum_secondary_only_efficiency"],
            )
        )
    path = FIGURE_DIR / "A7b_controlling_margins.png"
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), dpi=160, sharex=True)
    panels = (
        (axes[0, 0], energy_ratios, "Reference energy / 900 J"),
        (axes[0, 1], rise_ratios, "Cage rise / 20 K"),
        (axes[1, 0], current_ratios, "Cage current density / 180 A/mm2"),
        (axes[1, 1], efficiency_ratios, "Required / secondary efficiency"),
    )
    for axis, values, title in panels:
        colors = ["#dc2626" if value > 1.0 else "#0891b2" for value in values]
        axis.bar(corner_labels, values, color=colors)
        axis.axhline(1.0, color="#111827", linestyle="--", linewidth=1.2)
        axis.set_title(title)
        axis.set_ylabel("Normalized demand")
        axis.grid(axis="y", alpha=0.25)
        axis.tick_params(axis="x", rotation=20)
    fig.suptitle("A7b controlling corner margins | <=1 passes")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A7b renderer"})
    plt.close(fig)
    figures.append((path, "A7b controlling normalized corner margins", "MODEL OUTPUT"))

    records = [
        {
            "path": str(path.relative_to(ROOT)),
            "title": title,
            "evidence": evidence,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "source": "tools/render_gen26_cage.py",
        }
        for path, title, evidence in figures
    ]
    MANIFEST.write_text(
        json.dumps(
            {"schema_version": 1, "gate": "A7b", "figure_count": len(records), "figures": records},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("missing A7b figure manifest")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for record in manifest["figures"]:
        path = ROOT / record["path"]
        if (
            not path.exists()
            or path.stat().st_size != record["bytes"]
            or sha256(path) != record["sha256"]
        ):
            raise SystemExit(f"stale A7b figure: {path.relative_to(ROOT)}")
    print("OK: A7b figure hashes are current")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")
    if args.write:
        render()
    else:
        check()


if __name__ == "__main__":
    main()
