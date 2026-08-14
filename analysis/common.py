"""Shared deterministic calculations for the Bolley Phase 0 screens."""

from __future__ import annotations

import json
import math
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


# A residual that exists only to show a constraint closes is judged against a declared
# tolerance, and below that tolerance it carries no information beyond "closes". Its exact
# value does not survive a change of platform: the force-sum residual is 5.7e-14 on one
# machine and 1.1e-13 on another, both of them zero to every purpose this project has, and
# an exact comparison reports the second as a stale result. Snapping below the floor makes
# the reported number reproducible without hiding a residual that ever becomes real.
#
# The floor is the same 1e-9 the bands in force_allocation.py already test against, so this
# introduces no tolerance that was not already declared.
RESIDUAL_FLOOR = 1e-9


def snap_residual(value: float, floor: float = RESIDUAL_FLOOR) -> float:
    """Report a should-be-zero residual as exactly zero when it is below `floor`."""

    return 0.0 if abs(value) < floor else value


# Two floats that differ in the last bit of the mantissa are the same number as far as this
# project is concerned, and they are what a different libm or BLAS returns for an identical
# calculation. `induction_screen.py` emits 8,000 time-series values; on a second machine 117
# of them moved by one unit in the last place, and exact equality reported the whole result
# as stale. The tolerance below is ~1e-12 relative, four orders of magnitude tighter than any
# change to the design could be and four orders looser than the noise.
#
# It does NOT cover a residual that should be zero: 5.7e-14 against 1.1e-13 is a factor of
# two in relative terms and no relative tolerance can accept it. That is what snap_residual
# is for, and the two fixes are for different failures.
RELATIVE_TOLERANCE = 1e-12


def _same(committed, computed) -> bool:
    if isinstance(committed, bool) or isinstance(computed, bool):
        return committed is computed
    if isinstance(committed, (int, float)) and isinstance(computed, (int, float)):
        return math.isclose(committed, computed, rel_tol=RELATIVE_TOLERANCE, abs_tol=0.0)
    return committed == computed


def _differences(committed, computed, path=""):
    """Every leaf that disagrees by more than RELATIVE_TOLERANCE, as (path, was, now)."""

    if isinstance(committed, dict) and isinstance(computed, dict):
        out = []
        for key in sorted(set(committed) | set(computed)):
            here = f"{path}.{key}" if path else str(key)
            if key not in committed:
                out.append((here, "<absent>", computed[key]))
            elif key not in computed:
                out.append((here, committed[key], "<absent>"))
            else:
                out.extend(_differences(committed[key], computed[key], here))
        return out
    if isinstance(committed, list) and isinstance(computed, list):
        if len(committed) != len(computed):
            return [(path, f"{len(committed)} items", f"{len(computed)} items")]
        out = []
        for index, (a, b) in enumerate(zip(committed, computed)):
            out.extend(_differences(a, b, f"{path}[{index}]"))
        return out
    return [] if _same(committed, computed) else [(path, committed, computed)]


def compare_json(path: Path, payload: dict) -> None:
    if not path.exists():
        raise SystemExit(f"missing generated result: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as handle:
        committed = json.load(handle)
    diffs = _differences(committed, payload)
    if diffs:
        # Naming the field is the whole point. "stale generated result" on its own sends the
        # reader to diff two thousand-line JSON files to find out whether the design moved or
        # the last bit of a float did.
        lines = [f"stale generated result: {path.relative_to(ROOT)}"]
        for where, was, now in diffs[:20]:
            lines.append(f"  {where}: committed {was!r}, computed {now!r}")
        if len(diffs) > 20:
            lines.append(f"  ... and {len(diffs) - 20} more")
        raise SystemExit("\n".join(lines))


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

