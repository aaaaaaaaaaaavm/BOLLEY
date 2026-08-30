"""Bolley A9b: apply the existing residual floor to my A9 force-sign checks."""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

from common import RESIDUAL_FLOOR, RESULTS, ROOT, compare_json, dump_json, snap_residual
import sectional_drive as a9


OUTPUT = RESULTS / "sectional_drive_a9b.json"
A9_FAILURE = RESULTS / "sectional_drive_a9_failure.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def corrected_resolution(resolution: dict, limits: dict) -> tuple[dict, list[dict]]:
    corrected = copy.deepcopy(resolution)
    residuals = []
    for corner in corrected["corners"]:
        for case_name in ("reference", "qualification"):
            case = corner[case_name]
            raw = case["healthy_minimum_axial_force_n"]
            snapped = snap_residual(raw)
            residuals.append(
                {
                    "corner": corner["corner"],
                    "case": case_name,
                    "raw_minimum_force_n": raw,
                    "snapped_minimum_force_n": snapped,
                }
            )
            case["healthy_minimum_axial_force_n"] = snapped
            case["selector"]["minimum_channel_force_n"] = snapped
            case["selector"]["healthy_minimum_axial_force_n"] = snapped

    bands = a9.evaluate_bands(corrected["corners"], limits)
    corrected["bands"] = bands
    corrected["band_pass_count"] = sum(bands.values())
    corrected["band_count"] = len(bands)
    corrected["failed_bands"] = [name for name, passed in bands.items() if not passed]
    corrected["pass"] = all(bands.values())
    return corrected, residuals


def same_controlling(a: dict, b: dict) -> bool:
    if set(a) != set(b):
        return False
    return all(
        math.isclose(float(a[key]), float(b[key]), rel_tol=1e-12, abs_tol=0.0)
        for key in a
    )


def calculate() -> dict:
    parameters = a9.load(a9.INPUT)
    base = a9.load(a9.BASE_INPUT)
    a7c = a9.load(a9.A7C_RESULT)
    preserved = load(A9_FAILURE)

    coarse_raw = a9.calculate_resolution(parameters, base, a7c, 100)
    fine_raw = a9.calculate_resolution(parameters, base, a7c, 200)
    coarse, coarse_residuals = corrected_resolution(coarse_raw, parameters["bands"])
    fine, fine_residuals = corrected_resolution(fine_raw, parameters["bands"])

    controlling = a9.maxima(fine)
    raw_minimum = min(item["raw_minimum_force_n"] for item in fine_residuals)
    snapped_minimum = min(item["snapped_minimum_force_n"] for item in fine_residuals)
    all_subfloor = all(
        abs(item["raw_minimum_force_n"]) < RESIDUAL_FLOOR
        for item in fine_residuals
        if item["raw_minimum_force_n"] < 0.0
    )
    controlling_matches_a9 = same_controlling(controlling, preserved["controlling"])
    band_outcomes_match = coarse["bands"] == fine["bands"]
    all_bands_pass = fine["pass"] and coarse["pass"]

    checks = {
        "negative_residuals_below_existing_floor": all_subfloor,
        "snapped_minimum_force_nonnegative": snapped_minimum >= 0.0,
        "coarse_fine_band_outcomes_match": band_outcomes_match,
        "all_unchanged_physical_bands_pass": all_bands_pass,
        "controlling_nonforce_outputs_match_preserved_a9": controlling_matches_a9,
    }

    return {
        "evidence": "A9b NUMERICAL RECLOSURE OF COMMITTED A9 USING THE EXISTING RESIDUAL FLOOR",
        "source_solver": "analysis/sectional_drive.py",
        "source_failure_record": str(A9_FAILURE.relative_to(ROOT)),
        "residual_floor_n": RESIDUAL_FLOOR,
        "fine_raw_minimum_force_n": raw_minimum,
        "fine_snapped_minimum_force_n": snapped_minimum,
        "coarse_band_pass_count": coarse["band_pass_count"],
        "fine_band_pass_count": fine["band_pass_count"],
        "band_count": fine["band_count"],
        "fine_failed_bands": fine["failed_bands"],
        "fine_bands": fine["bands"],
        "controlling": controlling,
        "checks": checks,
        "check_pass_count": sum(checks.values()),
        "check_count": len(checks),
        "screen_pass": all(checks.values()),
        "disposition": (
            "A9B_PASS_RETAIN_FLUXRELAY_FOR_SUPPLIER_AND_PACKAGING_CLOSURE"
            if all(checks.values())
            else "A9B_FAIL_KEEP_P38_OPEN"
        ),
        "limits": [
            "A9 remains a preserved 11/13 execution; A9b does not rewrite it.",
            "The 1e-9 residual floor predates A9 and is not a new acceptance tolerance.",
            "Supplier switching loss, hot resistance, cables, 3D end fields, packaged mass and hardware force evidence remain outside this reclosure."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = calculate()
    if args.write:
        dump_json(OUTPUT, result)
    elif args.check:
        compare_json(OUTPUT, result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
