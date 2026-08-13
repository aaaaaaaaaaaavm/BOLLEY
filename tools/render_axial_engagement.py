"""Render A8a axial-overlap and correction-trade evidence."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis" / "results" / "axial_engagement.json"
FIGURE_DIR = ROOT / "analysis" / "figures" / "a8a"
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
    points_path = ROOT / result["profile_artifact"]["path"]
    with gzip.open(points_path, "rt", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    figures = []

    travel = np.asarray([float(row["travel_m"]) for row in rows])
    names = {
        "as_drawn_rated": ("As drawn | 375 A", "#475569"),
        "as_drawn_limited_boost": ("As drawn | <=400 A", "#dc2626"),
        "best_placement_limited_boost": ("Best placement | <=400 A", "#0891b2"),
    }
    path = FIGURE_DIR / "A8a_engagement_profile.png"
    fig, axes = plt.subplots(3, 1, figsize=(11.5, 10), dpi=160, sharex=True)
    for key, (label, color) in names.items():
        overlap = np.asarray([float(row[f"{key}_overlap_fraction"]) for row in rows])
        force = np.asarray([float(row[f"{key}_force_ratio_to_nominal"]) for row in rows])
        velocity = np.asarray([float(row[f"{key}_velocity_m_s"]) for row in rows])
        axes[0].plot(travel * 1e3, overlap, label=label, color=color, linewidth=2)
        axes[1].plot(travel * 1e3, force, label=label, color=color, linewidth=2)
        axes[2].plot(travel * 1e3, velocity, label=label, color=color, linewidth=2)
    ideal_velocity = np.sqrt(2.0 * 8.0 * 9.81 * travel)
    axes[2].plot(travel * 1e3, ideal_velocity, label="Full-overlap 8 g", color="#111827", linestyle="--")
    axes[2].axhline(11.8, color="#7c3aed", linestyle=":", linewidth=1.6, label="11.8 m/s band")
    axes[0].set_ylabel("Overlap fraction")
    axes[1].set_ylabel("Force / nominal")
    axes[2].set_ylabel("Velocity [m/s]")
    axes[2].set_xlabel("Payload travel [mm]")
    for axis in axes:
        axis.grid(alpha=0.25)
        axis.legend(loc="best", fontsize=9)
    fig.suptitle("A8a finite cage engagement across the claimed 900 mm travel")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A8a renderer"})
    plt.close(fig)
    figures.append((path, "Axial overlap, force and velocity traces", "MODEL OUTPUT"))

    path = FIGURE_DIR / "A8a_correction_trade.png"
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.2), dpi=160)
    velocity_labels = ["As drawn\n375 A", "As drawn\n400 A", "Best place\n400 A"]
    velocity_values = [
        result["as_drawn_rated"]["exit_velocity_m_s"],
        result["as_drawn_limited_boost"]["exit_velocity_m_s"],
        result["best_placement_limited_boost"]["exit_velocity_m_s"],
    ]
    axes[0].bar(velocity_labels, velocity_values, color=["#475569", "#dc2626", "#0891b2"])
    axes[0].axhline(11.8, color="#111827", linestyle="--")
    axes[0].set_ylim(0, 12.5)
    axes[0].set_title("Exit velocity")
    axes[0].set_ylabel("m/s")

    extension = result["full_overlap_extension"]
    mass_labels = ["Current\n900 mm", "42-cell\n1,260 mm", "9-tile\n1,350 mm"]
    mass_values = [
        result["field_and_cage_inputs_unchanged"]["a7b_active_primary_mass_kg"],
        extension["cell_quantized_active_primary_mass_kg"],
        extension["tile_quantized_active_primary_mass_kg"],
    ]
    axes[1].bar(mass_labels, mass_values, color=["#0891b2", "#dc2626", "#dc2626"])
    axes[1].axhline(16.0, color="#111827", linestyle="--")
    axes[1].set_ylim(0, 26)
    axes[1].set_title("Installed active primary")
    axes[1].set_ylabel("kg")

    sectional = result["sectional_excitation"]
    resistance_labels = ["All A7b\ncells", "Whole-tile\nwindow", "Cell\nwindow"]
    resistance_values = [
        1.0,
        sectional["tile_window_phase_resistance_ratio_to_a7b"],
        sectional["cell_window_phase_resistance_ratio_to_a7b"],
    ]
    colors = [
        "#dc2626" if value > sectional["a7b_required_phase_resistance_ratio"] else "#0891b2"
        for value in resistance_values
    ]
    axes[2].bar(resistance_labels, resistance_values, color=colors)
    axes[2].axhline(
        sectional["a7b_required_phase_resistance_ratio"],
        color="#111827",
        linestyle="--",
    )
    axes[2].set_ylim(0, 1.1)
    axes[2].set_title("Phase resistance / A7b")
    axes[2].set_ylabel("ratio")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("A8a separates the stroke failure from the useful circuit correction")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A8a renderer"})
    plt.close(fig)
    figures.append((path, "Velocity, installed-mass and sectional-resistance trade", "MODEL OUTPUT"))

    records = [
        {
            "path": str(path.relative_to(ROOT)),
            "title": title,
            "evidence": evidence,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "source": "tools/render_axial_engagement.py",
        }
        for path, title, evidence in figures
    ]
    MANIFEST.write_text(
        json.dumps(
            {"schema_version": 1, "gate": "A8a", "figure_count": len(records), "figures": records},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("missing A8a figure manifest")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for record in manifest["figures"]:
        path = ROOT / record["path"]
        if (
            not path.exists()
            or path.stat().st_size != record["bytes"]
            or sha256(path) != record["sha256"]
        ):
            raise SystemExit(f"stale A8a figure: {path.relative_to(ROOT)}")
    print("OK: A8a figure hashes are current")


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
