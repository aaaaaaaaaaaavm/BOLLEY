"""Shared deterministic calculations for the Bolley Phase 0 screens."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARAMETERS = ROOT / "cad" / "parameters.json"
RESULTS = ROOT / "analysis" / "results"


def load_parameters() -> dict:
    with PARAMETERS.open(encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def compare_json(path: Path, payload: dict) -> None:
    if not path.exists():
        raise SystemExit(f"missing generated result: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as handle:
        committed = json.load(handle)
    if committed != payload:
        raise SystemExit(f"stale generated result: {path.relative_to(ROOT)}")


def rail_forces(total_force_n: float, y_cg_m: float, z_cg_m: float, radius_m: float) -> dict:
    """Return four positive-corner force commands for a requested force centroid."""

    forces = {}
    for sy in (-1, 1):
        for sz in (-1, 1):
            key = f"y{sy:+d}_z{sz:+d}"
            forces[key] = (
                total_force_n
                / 4.0
                * (1.0 + sy * y_cg_m / radius_m)
                * (1.0 + sz * z_cg_m / radius_m)
            )
    return forces


def force_centroid(forces: dict, radius_m: float) -> tuple[float, float, float]:
    total = sum(forces.values())
    y_moment = z_moment = 0.0
    for sy in (-1, 1):
        for sz in (-1, 1):
            force = forces[f"y{sy:+d}_z{sz:+d}"]
            y_moment += sy * radius_m * force
            z_moment += sz * radius_m * force
    return total, y_moment / total, z_moment / total

