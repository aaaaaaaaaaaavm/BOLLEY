"""Render A8b design-space, margin and axial-package evidence."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "analysis" / "results" / "gen27_codesign.json"
FIGURE_DIR = ROOT / "analysis" / "figures" / "a8b"
MANIFEST = FIGURE_DIR / "FIGURES.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_candidates(result: dict) -> list[dict]:
    path = ROOT / result["candidate_artifact"]["path"]
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def draw_package(axis, design: dict, interface: dict, start: float, title: str) -> int:
    import matplotlib.patches as patches

    pitch = design["cell_pitch_m"]
    count = design["total_cells_per_channel"]
    stator_length = design["active_stator_length_m"]
    cage_length = interface["active_cage_length_m"]
    cage_end = start + cage_length
    intersected = 0
    for index in range(count):
        x0 = index * pitch
        x1 = x0 + pitch
        active = min(x1, cage_end) - max(x0, start) > 1e-12
        if active:
            intersected += 1
        axis.add_patch(
            patches.Rectangle(
                (x0, 0.0),
                pitch,
                0.35,
                facecolor="#0f766e" if active else "#cbd5e1",
                edgecolor="#ffffff",
                linewidth=0.5,
            )
        )
    axis.add_patch(
        patches.Rectangle(
            (start, 0.55),
            cage_length,
            0.22,
            facecolor="#f59e0b",
            edgecolor="#92400e",
            linewidth=1.2,
        )
    )
    axis.text(start + cage_length / 2.0, 0.66, "318.6 mm passive cage", ha="center", va="center")
    axis.text(stator_length / 2.0, 0.175, f"{intersected} endpoint cells intersected", ha="center", va="center")
    axis.set_xlim(-0.015, stator_length + 0.015)
    axis.set_ylim(-0.1, 0.92)
    axis.set_yticks([])
    axis.set_title(title, loc="left")
    axis.spines[["left", "right", "top"]].set_visible(False)
    return intersected


def render() -> None:
    import matplotlib.pyplot as plt

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    candidates = load_candidates(result)
    selected = result["selected_candidate"]
    selected_id = result["selected_candidate_id"]
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    figures = []

    evaluated = [candidate for candidate in candidates if candidate["fully_evaluated"]]
    currents = sorted({candidate["rated"]["phase_current_rms_a"] for candidate in candidates})
    path = FIGURE_DIR / "A8b_feasible_island.png"
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9), dpi=160, sharex=True, sharey=True)
    scatter = None
    for axis, current in zip(axes.flat, currents):
        subset = [candidate for candidate in evaluated if candidate["rated"]["phase_current_rms_a"] == current]
        if not subset:
            axis.text(
                0.5,
                0.54,
                "No precheck survivor\ncurrent-scaled stationary peak >1.55 T",
                ha="center",
                va="center",
                transform=axis.transAxes,
                fontsize=11,
            )
            axis.set_title(f"{current:.0f} A | rejected before corner evaluation")
            axis.set_xlim(39.5, 50.5)
            axis.set_ylim(9.4, 12.1)
            axis.set_xlabel("Cell pitch [mm]")
            axis.set_ylabel("Conductor area / turn [mm2]")
            axis.grid(alpha=0.2)
            continue
        pitch = np.asarray([1e3 * candidate["design"]["cell_pitch_m"] for candidate in subset])
        area = np.asarray([1e6 * candidate["design"]["conductor_area_per_turn_m2"] for candidate in subset])
        demand = np.asarray([candidate["worst_continuous_demand"] for candidate in subset])
        scatter = axis.scatter(
            pitch,
            area,
            c=demand,
            cmap="RdYlGn_r",
            vmin=0.96,
            vmax=1.08,
            s=38,
            alpha=0.9,
            linewidths=0.0,
        )
        feasible = [candidate for candidate in subset if candidate["feasible"]]
        axis.scatter(
            [1e3 * candidate["design"]["cell_pitch_m"] for candidate in feasible],
            [1e6 * candidate["design"]["conductor_area_per_turn_m2"] for candidate in feasible],
            facecolors="none",
            edgecolors="#0891b2",
            linewidths=1.2,
            s=62,
        )
        chosen = [candidate for candidate in subset if candidate["candidate_id"] == selected_id]
        if chosen:
            axis.scatter(
                [1e3 * chosen[0]["design"]["cell_pitch_m"]],
                [1e6 * chosen[0]["design"]["conductor_area_per_turn_m2"]],
                marker="*",
                s=240,
                c="#111827",
                edgecolors="white",
                linewidths=0.8,
                zorder=5,
            )
        axis.axvline(45.3, color="#475569", linestyle=":", linewidth=0.8, alpha=0.5)
        axis.set_title(f"{current:.0f} A | cyan ring passes all bands")
        axis.grid(alpha=0.2)
        axis.set_xlabel("Cell pitch [mm]")
        axis.set_ylabel("Conductor area / turn [mm2]")
    if scatter is not None:
        color_axis = fig.add_axes([0.89, 0.16, 0.018, 0.68])
        colorbar = fig.colorbar(scatter, cax=color_axis)
        colorbar.set_label("Worst normalized hard-band demand | <=1 passes")
    fig.suptitle("A8b precheck-survivor design island | 27-cell candidates")
    fig.subplots_adjust(left=0.08, right=0.86, bottom=0.08, top=0.91, hspace=0.22, wspace=0.16)
    fig.savefig(path, metadata={"Software": "Bolley deterministic A8b renderer"})
    plt.close(fig)
    figures.append((path, "A8b feasible axial/electrical design island", "MODEL OUTPUT"))

    path = FIGURE_DIR / "A8b_selected_margins.png"
    demands = sorted(
        selected["continuous_demand_by_band"].items(), key=lambda item: item[1]
    )
    labels = [name.replace("_", " ") for name, _ in demands]
    values = [value for _, value in demands]
    colors = ["#dc2626" if value > 1.0 else "#0891b2" for value in values]
    fig, axis = plt.subplots(figsize=(11.5, 10), dpi=160)
    axis.barh(labels, values, color=colors)
    axis.axvline(1.0, color="#111827", linestyle="--", linewidth=1.3)
    axis.set_xlim(0.0, max(1.04, max(values) * 1.02))
    axis.set_xlabel("Normalized demand | <=1 passes")
    axis.set_title(f"A8b selected minimax margins | {selected_id}")
    axis.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A8b renderer"})
    plt.close(fig)
    figures.append((path, "Selected Fluxrelay normalized hard-band margins", "MODEL OUTPUT"))

    design = selected["design"]
    interface = selected["interface"]
    path = FIGURE_DIR / "A8b_axial_package.png"
    fig, axes = plt.subplots(2, 1, figsize=(14, 5.8), dpi=160, sharex=True)
    draw_package(
        axes[0],
        design,
        interface,
        interface["active_cage_start_x_m"],
        "Initial engagement | 2.25 mm aft guard",
    )
    draw_package(
        axes[1],
        design,
        interface,
        interface["active_cage_start_x_m"] + 0.9,
        "After 900 mm powered travel | 2.25 mm forward guard",
    )
    axes[1].set_xlabel("Axial station [m]")
    fig.suptitle(
        "A8b selected 1.2231 m / 27-cell primary | conservative moving window = 9 cells"
    )
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": "Bolley deterministic A8b renderer"})
    plt.close(fig)
    figures.append((path, "Selected Fluxrelay axial engagement package", "MODEL OUTPUT"))

    records = [
        {
            "path": str(figure_path.relative_to(ROOT)),
            "title": title,
            "evidence": evidence,
            "bytes": figure_path.stat().st_size,
            "sha256": sha256(figure_path),
            "source": "tools/render_gen27_codesign.py",
        }
        for figure_path, title, evidence in figures
    ]
    MANIFEST.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "gate": "A8b",
                "figure_count": len(records),
                "figures": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def check() -> None:
    if not MANIFEST.exists():
        raise SystemExit("missing A8b figure manifest")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for record in manifest["figures"]:
        path = ROOT / record["path"]
        if (
            not path.exists()
            or path.stat().st_size != record["bytes"]
            or sha256(path) != record["sha256"]
        ):
            raise SystemExit(f"stale A8b figure: {path.relative_to(ROOT)}")
    print("OK: A8b figure hashes are current")


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
