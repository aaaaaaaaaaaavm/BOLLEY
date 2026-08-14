"""Bolley A2: sweep the declared transverse CG envelope."""

from __future__ import annotations

import argparse

from common import (
    RESULTS,
    compare_json,
    snap_residual,
    dump_json,
    force_centroid,
    load_parameters,
    rail_forces,
)
from baseline import calculate as calculate_baseline


OUTPUT = RESULTS / "force_allocation.json"


def calculate() -> dict:
    p = load_parameters()
    baseline = calculate_baseline()
    limit = p["payload"]["transverse_cg_limit_m"]
    radius = p["rail"]["force_line_radius_m"]
    total_force = baseline["qualification_case"]["total_force_n"]
    channel_band = p["screens"]["channel_force_band_n"]

    count = 21
    coordinates = [-limit + 2.0 * limit * index / (count - 1) for index in range(count)]
    min_force = float("inf")
    max_force = float("-inf")
    max_sum_error = 0.0
    max_centroid_error = 0.0
    worst_point = None

    for y_cg in coordinates:
        for z_cg in coordinates:
            forces = rail_forces(total_force, y_cg, z_cg, radius)
            reconstructed_total, y_reconstructed, z_reconstructed = force_centroid(forces, radius)
            local_min = min(forces.values())
            local_max = max(forces.values())
            min_force = min(min_force, local_min)
            if local_max > max_force:
                max_force = local_max
                worst_point = {"y_cg_m": y_cg, "z_cg_m": z_cg, "forces_n": forces}
            max_sum_error = max(max_sum_error, abs(reconstructed_total - total_force))
            max_centroid_error = max(
                max_centroid_error,
                abs(y_reconstructed - y_cg),
                abs(z_reconstructed - z_cg),
            )

    max_fraction = max_force / total_force
    bands = {
        "all_forces_nonnegative": min_force >= 0.0,
        "channel_force": max_force <= channel_band,
        "force_sum_error": max_sum_error <= 1e-9,
        "centroid_error": max_centroid_error <= 1e-9,
        "single_channel_fraction": max_fraction <= 0.52,
    }
    return {
        "evidence": "MODEL OUTPUT; algebraic allocation only",
        "grid": {"points_per_axis": count, "limit_m": limit, "total_points": count**2},
        "qualification_total_force_n": total_force,
        "minimum_channel_force_n": min_force,
        "maximum_channel_force_n": max_force,
        "maximum_channel_fraction": max_fraction,
        "maximum_force_sum_error_n": snap_residual(max_sum_error),
        "maximum_centroid_error_m": snap_residual(max_centroid_error),
        "worst_point": worst_point,
        "bands": bands,
        "overall_pass": all(bands.values()),
        "limits": [
            "CG knowledge, force calibration, structural compliance and control bandwidth are excluded.",
            "Positive algebraic commands do not establish electromagnetic independence between channels.",
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
        import json

        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

