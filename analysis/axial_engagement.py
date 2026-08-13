"""Bolley A8a: axial overlap, sectional excitation and installed-length audit."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "cad" / "axial_engagement_parameters.json"
A7B_RESULT = RESULTS / "gen26_cage_circuit.json"
OUTPUT = RESULTS / "axial_engagement.json"
POINTS_OUTPUT = RESULTS / "axial_engagement_points.csv.gz"
GRAVITY_M_S2 = 9.81


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def overlap_length(
    stator_start: float,
    stator_length: float,
    cage_start: float,
    cage_length: float,
) -> float:
    return max(
        0.0,
        min(stator_start + stator_length, cage_start + cage_length)
        - max(stator_start, cage_start),
    )


def profile(control: dict, initial_cage_start: float, boost: bool) -> list[dict]:
    geometry = control["geometry"]
    drive = control["drive"]
    count = drive["profile_point_count"]
    travel = geometry["commanded_travel_m"]
    dx = travel / (count - 1)
    acceleration = drive["nominal_acceleration_g"] * GRAVITY_M_S2
    rated_current = drive["rated_phase_current_rms_a"]
    maximum_current = drive["maximum_phase_current_rms_a"]
    exponent = drive["force_field_exponent"]
    work_distance = 0.0
    previous_force_ratio = None
    rows = []
    for index in range(count):
        travel_x = index * dx
        overlap = overlap_length(
            geometry["stator_start_x_m"],
            geometry["stator_active_length_m"],
            initial_cage_start + travel_x,
            geometry["cage_active_length_m"],
        )
        overlap_fraction = overlap / geometry["cage_active_length_m"]
        if boost and overlap_fraction > 0.0:
            required_current = rated_current / overlap_fraction ** (1.0 / exponent)
            current = min(maximum_current, required_current)
        else:
            current = rated_current if overlap_fraction > 0.0 else 0.0
        force_ratio = min(
            1.0,
            overlap_fraction * (current / rated_current) ** exponent,
        )
        if previous_force_ratio is not None:
            work_distance += 0.5 * (previous_force_ratio + force_ratio) * dx
        velocity = math.sqrt(2.0 * acceleration * work_distance)
        rows.append(
            {
                "travel_m": travel_x,
                "overlap_m": overlap,
                "overlap_fraction": overlap_fraction,
                "phase_current_rms_a": current,
                "force_ratio_to_nominal": force_ratio,
                "effective_work_distance_m": work_distance,
                "velocity_m_s": velocity,
            }
        )
        previous_force_ratio = force_ratio
    return rows


def compact_profile(rows: list[dict], initial_cage_start: float) -> dict:
    return {
        "initial_cage_start_x_m": initial_cage_start,
        "initial_overlap_fraction": rows[0]["overlap_fraction"],
        "final_overlap_fraction": rows[-1]["overlap_fraction"],
        "minimum_overlap_fraction": min(row["overlap_fraction"] for row in rows),
        "maximum_phase_current_rms_a": max(row["phase_current_rms_a"] for row in rows),
        "effective_work_distance_m": rows[-1]["effective_work_distance_m"],
        "exit_velocity_m_s": rows[-1]["velocity_m_s"],
    }


def round_up_multiple(value: int, multiple: int) -> int:
    return ((value + multiple - 1) // multiple) * multiple


def maximum_intersected_segments(active_length: float, segment_length: float) -> int:
    return math.ceil(active_length / segment_length - 1e-12) + 1


def calculate() -> tuple[dict, dict[str, list[dict]]]:
    control = load(INPUT)
    a7b = load(A7B_RESULT)
    geometry = control["geometry"]
    drive = control["drive"]
    accounting = control["accounting"]
    limits = control["bands"]

    as_drawn_rated = profile(
        control,
        geometry["cage_active_start_at_retained_position_x_m"],
        boost=False,
    )
    as_drawn_limited_boost = profile(
        control,
        geometry["cage_active_start_at_retained_position_x_m"],
        boost=True,
    )

    placement_count = drive["placement_candidate_count"]
    cage_length = geometry["cage_active_length_m"]
    placement_candidates = [
        -cage_length + cage_length * index / (placement_count - 1)
        for index in range(placement_count)
    ]
    placement_records = []
    best_rows = None
    for initial_start in placement_candidates:
        rows = profile(control, initial_start, boost=True)
        record = compact_profile(rows, initial_start)
        placement_records.append(record)
        if best_rows is None or rows[-1]["effective_work_distance_m"] > best_rows[-1][
            "effective_work_distance_m"
        ]:
            best_rows = rows
    assert best_rows is not None
    best_placement = compact_profile(best_rows, best_rows[0]["travel_m"])
    best_placement["initial_cage_start_x_m"] = next(
        record["initial_cage_start_x_m"]
        for record in placement_records
        if math.isclose(
            record["effective_work_distance_m"],
            best_rows[-1]["effective_work_distance_m"],
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    # Recompute with the retained winning start so the packaged trace has the right geometry.
    best_rows = profile(control, best_placement["initial_cage_start_x_m"], boost=True)
    best_placement = compact_profile(best_rows, best_placement["initial_cage_start_x_m"])

    required_continuous_length = (
        geometry["cage_active_start_at_retained_position_x_m"]
        + geometry["cage_active_length_m"]
        + geometry["commanded_travel_m"]
        - geometry["stator_start_x_m"]
    )
    raw_cell_count = math.ceil(
        required_continuous_length / geometry["cell_pitch_m"] - 1e-12
    )
    cell_count = round_up_multiple(raw_cell_count, geometry["phase_count"])
    cell_quantized_length = cell_count * geometry["cell_pitch_m"]
    tile_count = math.ceil(
        required_continuous_length / geometry["tile_length_m"] - 1e-12
    )
    tile_quantized_length = tile_count * geometry["tile_length_m"]
    cell_primary_mass = (
        accounting["a7b_active_primary_mass_kg"]
        * cell_quantized_length
        / geometry["stator_active_length_m"]
    )
    tile_primary_mass = (
        accounting["a7b_active_primary_mass_kg"]
        * tile_quantized_length
        / geometry["stator_active_length_m"]
    )

    active_cells = maximum_intersected_segments(
        cage_length, geometry["cell_pitch_m"]
    )
    cell_window_phase_cells = math.ceil(active_cells / geometry["phase_count"])
    active_tiles = maximum_intersected_segments(
        cage_length, geometry["tile_length_m"]
    )
    active_tile_cells = active_tiles * geometry["cells_per_tile"]
    tile_window_phase_cells = math.ceil(
        active_tile_cells / geometry["phase_count"]
    )
    cell_window_resistance_ratio = (
        cell_window_phase_cells / accounting["a7b_cells_per_phase"]
    )
    tile_window_resistance_ratio = (
        tile_window_phase_cells / accounting["a7b_cells_per_phase"]
    )

    as_drawn_rated_summary = compact_profile(
        as_drawn_rated,
        geometry["cage_active_start_at_retained_position_x_m"],
    )
    as_drawn_boost_summary = compact_profile(
        as_drawn_limited_boost,
        geometry["cage_active_start_at_retained_position_x_m"],
    )
    bands = {
        "as_drawn_reference_velocity": as_drawn_rated_summary["exit_velocity_m_s"]
        >= limits["minimum_reference_exit_velocity_m_s"],
        "as_drawn_qualification_velocity": as_drawn_rated_summary["exit_velocity_m_s"]
        >= limits["minimum_qualification_exit_velocity_m_s"],
        "best_placement_reference_velocity": best_placement["exit_velocity_m_s"]
        >= limits["minimum_reference_exit_velocity_m_s"],
        "boost_current": as_drawn_boost_summary["maximum_phase_current_rms_a"]
        <= limits["maximum_phase_current_rms_a"],
        "as_drawn_end_overlap": as_drawn_rated_summary["final_overlap_fraction"]
        >= limits["minimum_end_overlap_fraction_for_full_force"],
        "cell_quantized_primary_mass": cell_primary_mass
        <= limits["maximum_installed_active_primary_mass_kg"],
        "tile_quantized_primary_mass": tile_primary_mass
        <= limits["maximum_installed_active_primary_mass_kg"],
        "cell_sectional_resistance": cell_window_resistance_ratio
        <= limits["maximum_phase_resistance_ratio_to_a7b"],
        "tile_sectional_resistance": tile_window_resistance_ratio
        <= limits["maximum_phase_resistance_ratio_to_a7b"],
        "three_phase_cell_count": cell_count % geometry["phase_count"] == 0,
    }
    bands = {name: bool(value) for name, value in bands.items()}
    profiles = {
        "as_drawn_rated": as_drawn_rated,
        "as_drawn_limited_boost": as_drawn_limited_boost,
        "best_placement_limited_boost": best_rows,
    }
    result = {
        "evidence": "A8a AXIAL OVERLAP + CURRENT-LIMITED KINEMATIC AUDIT",
        "input_file": str(INPUT.relative_to(ROOT)),
        "source_files": control["source_files"],
        "as_drawn_rated": as_drawn_rated_summary,
        "as_drawn_limited_boost": as_drawn_boost_summary,
        "best_placement_limited_boost": best_placement,
        "full_overlap_extension": {
            "required_continuous_stator_length_m": required_continuous_length,
            "cell_quantized_cell_count": cell_count,
            "cell_quantized_stator_length_m": cell_quantized_length,
            "cell_quantized_active_primary_mass_kg": cell_primary_mass,
            "tile_quantized_tile_count": tile_count,
            "tile_quantized_stator_length_m": tile_quantized_length,
            "tile_quantized_active_primary_mass_kg": tile_primary_mass,
        },
        "sectional_excitation": {
            "maximum_simultaneously_intersected_cells": active_cells,
            "maximum_cell_window_cells_per_phase": cell_window_phase_cells,
            "cell_window_phase_resistance_ratio_to_a7b": cell_window_resistance_ratio,
            "maximum_simultaneously_intersected_tiles": active_tiles,
            "maximum_tile_window_cells_per_phase": tile_window_phase_cells,
            "tile_window_phase_resistance_ratio_to_a7b": tile_window_resistance_ratio,
            "a7b_required_phase_resistance_ratio": limits[
                "maximum_phase_resistance_ratio_to_a7b"
            ],
        },
        "field_and_cage_inputs_unchanged": {
            "a7b_screen_pass": a7b["screen_pass"],
            "a7b_failed_band_union": a7b["failed_band_union"],
            "rated_phase_current_rms_a": drive["rated_phase_current_rms_a"],
            "maximum_phase_current_rms_a": drive["maximum_phase_current_rms_a"],
        },
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "failed_bands": [name for name, passed in bands.items() if not passed],
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_AS_DRAWN_GEN26_AXIAL_PACKAGE"
            if all(bands.values())
            else "REJECT_AS_DRAWN_GEN26_AXIAL_PACKAGE_PRESERVE_SECTIONAL_DRIVE"
        ),
        "limits": [
            "Force capacity scales with overlapped cage area and the square of current-derived field; fringing is absent.",
            "The current-limited boost is an optimistic command bound, not a transient voltage or field re-solve.",
            "Installed primary mass scales linearly with stator length; structure, power electronics, cooling and containment remain absent.",
            "Sectional resistance ratios count simultaneously intersected cells or whole tiles and do not yet model switching or end-cell force ripple.",
        ],
    }
    return result, profiles


def package_points(profiles: dict[str, list[dict]]) -> tuple[bytes, int]:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    profile_names = list(profiles)
    columns = [
        "overlap_fraction",
        "phase_current_rms_a",
        "force_ratio_to_nominal",
        "effective_work_distance_m",
        "velocity_m_s",
    ]
    writer.writerow(
        ["travel_m", *[f"{name}_{column}" for name in profile_names for column in columns]]
    )
    row_count = len(next(iter(profiles.values())))
    for index in range(row_count):
        writer.writerow(
            [
                next(iter(profiles.values()))[index]["travel_m"],
                *[
                    profiles[name][index][column]
                    for name in profile_names
                    for column in columns
                ],
            ]
        )
    payload = gzip.compress(stream.getvalue().encode("utf-8"), compresslevel=9, mtime=0)
    return payload, row_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result, profiles = calculate()
    points, point_count = package_points(profiles)
    result["profile_artifact"] = {
        "path": str(POINTS_OUTPUT.relative_to(ROOT)),
        "compression": "deterministic gzip CSV, mtime=0",
        "record_count": point_count,
        "bytes": len(points),
        "sha256": hashlib.sha256(points).hexdigest(),
    }
    if args.write:
        POINTS_OUTPUT.write_bytes(points)
        dump_json(OUTPUT, result)
    elif args.check:
        if not POINTS_OUTPUT.exists() or POINTS_OUTPUT.read_bytes() != points:
            raise SystemExit("stale A8a axial-profile artifact")
        compare_json(OUTPUT, result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
