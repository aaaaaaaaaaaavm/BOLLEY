"""Bolley A5a: analytical comb-fin envelope and force-allocation screen.

This is a preliminary geometry check against CDS guidance, not dispenser acceptance, structural
analysis, FEA or measurement. The bands in validation/A5a_comb_fin_envelope.md were committed
before the first recorded output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json, force_centroid, snap_residual


INPUT = ROOT / "cad" / "comb_fin_parameters.json"
BASELINE = RESULTS / "baseline.json"
OUTPUT = RESULTS / "interface_fit_screen.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def cardinal_forces(total_force_n: float, y_cg_m: float, z_cg_m: float, radius_m: float) -> dict:
    """Minimize peak positive force for channels at (+/-r,0) and (0,+/-r)."""

    delta_y = total_force_n * y_cg_m / radius_m
    delta_z = total_force_n * z_cg_m / radius_m
    minimum_y_pair = abs(delta_y)
    maximum_y_pair = total_force_n - abs(delta_z)
    if minimum_y_pair > maximum_y_pair:
        raise ValueError("requested force centroid is outside the cardinal-channel convex hull")
    unconstrained_y_pair = 0.5 * (total_force_n + abs(delta_z) - abs(delta_y))
    y_pair = min(max(unconstrained_y_pair, minimum_y_pair), maximum_y_pair)
    z_pair = total_force_n - y_pair
    return {
        "y-": 0.5 * (y_pair - delta_y),
        "y+": 0.5 * (y_pair + delta_y),
        "z-": 0.5 * (z_pair - delta_z),
        "z+": 0.5 * (z_pair + delta_z),
    }


def cardinal_centroid(forces: dict, radius_m: float) -> tuple[float, float, float]:
    total = sum(forces.values())
    y = radius_m * (forces["y+"] - forces["y-"]) / total
    z = radius_m * (forces["z+"] - forces["z-"]) / total
    return total, y, z


def calculate() -> dict:
    p = load(INPUT)
    baseline = load(BASELINE)
    interface = p["interface"]
    comb = p["comb_fin"]
    guidance = p["external_guidance"]
    limits = p["bands"]

    channels = interface["channel_count"]
    fins = comb["fins_per_channel"]
    active_height = comb["active_fin_height_m"]
    active_length = interface["active_length_m"]
    covered_fin_thickness = comb["steel_thickness_m"] + 2.0 * comb["side_cover_per_side_m"]
    slot_width = covered_fin_thickness + 2.0 * comb["clearance_per_side_m"]
    stationary_comb_span = (
        fins * slot_width + (fins + 1) * comb["stationary_pole_web_width_m"]
    )
    moving_root_span = stationary_comb_span
    total_projection = active_height + comb["radial_tip_cover_m"]
    rail_edge_clearance = 0.5 * (interface["body_face_span_m"] - moving_root_span)
    usable_face_width = (
        interface["body_face_span_m"]
        - 2.0 * guidance["minimum_rail_width_to_first_protrusion_m"]
    )
    projected_usable_face_fraction = moving_root_span / usable_face_width
    assumed_rail_contact_fraction = 1.0

    steel_volume = (
        channels
        * fins
        * active_height
        * active_length
        * comb["axial_tooth_duty_fraction"]
        * comb["steel_thickness_m"]
    )
    side_cover_volume = (
        channels
        * fins
        * 2.0
        * active_height
        * active_length
        * comb["side_cover_per_side_m"]
    )
    tip_cover_volume = (
        channels
        * fins
        * covered_fin_thickness
        * active_length
        * comb["radial_tip_cover_m"]
    )
    steel_mass = steel_volume * comb["steel_density_kg_m3"]
    cover_mass = (side_cover_volume + tip_cover_volume) * comb["aluminium_density_kg_m3"]
    interface_mass = steel_mass + cover_mass + comb["root_capture_fastener_allowance_kg"]

    active_area_per_channel = 2.0 * fins * active_height * active_length
    total_force = baseline["qualification_case"]["total_force_n"]
    radius = interface["force_line_radius_m"]
    cg_limit = interface["transverse_cg_limit_m"]
    points = interface["cg_grid_points_per_axis"]
    grid = [(-cg_limit + 2.0 * cg_limit * index / (points - 1)) for index in range(points)]
    records = []
    maximum_force = 0.0
    minimum_force = float("inf")
    maximum_fraction = 0.0
    maximum_sum_error = 0.0
    maximum_centroid_error = 0.0
    all_positive = True
    for y_cg in grid:
        for z_cg in grid:
            forces = cardinal_forces(total_force, y_cg, z_cg, radius)
            recovered_total, recovered_y, recovered_z = cardinal_centroid(forces, radius)
            local_max = max(forces.values())
            local_min = min(forces.values())
            maximum_force = max(maximum_force, local_max)
            minimum_force = min(minimum_force, local_min)
            maximum_fraction = max(maximum_fraction, local_max / total_force)
            maximum_sum_error = max(maximum_sum_error, abs(recovered_total - total_force))
            maximum_centroid_error = max(
                maximum_centroid_error, abs(recovered_y - y_cg), abs(recovered_z - z_cg)
            )
            all_positive = all_positive and local_min >= -1e-12
            records.append(
                {
                    "y_cg_m": y_cg,
                    "z_cg_m": z_cg,
                    "forces_n": forces,
                    "maximum_channel_force_n": local_max,
                    "minimum_channel_force_n": local_min,
                }
            )

    developed_shear = maximum_force / active_area_per_channel
    bands = {
        "side_protrusion": total_projection <= guidance["maximum_side_protrusion_from_rail_plane_m"],
        "rail_edge_keepout": rail_edge_clearance >= guidance["minimum_rail_width_to_first_protrusion_m"],
        "rail_contact": assumed_rail_contact_fraction >= guidance["minimum_rail_contact_fraction"],
        "stationary_comb_between_rail_keepouts": stationary_comb_span <= usable_face_width,
        "projected_usable_face_fraction": projected_usable_face_fraction <= limits["maximum_projected_usable_face_fraction"],
        "interface_mass_preferred": interface_mass <= limits["preferred_interface_mass_kg"],
        "interface_mass_absolute": interface_mass <= limits["absolute_interface_mass_kg"],
        "positive_force_allocation": all_positive,
        "maximum_channel_force": maximum_force <= limits["maximum_channel_force_n"],
        "developed_shear": developed_shear <= limits["maximum_developed_shear_pa"],
        "nominal_slot_clearance": comb["clearance_per_side_m"] >= limits["minimum_nominal_clearance_per_side_m"],
    }

    return {
        "evidence": "ANALYTICAL MODEL OUTPUT from ASSUMPTION geometry checked against named EXTERNAL GUIDANCE",
        "input_file": "cad/comb_fin_parameters.json",
        "source_warning": "CDS Rev. 14.1 is preliminary guidance; launch-provider requirements supersede it",
        "geometry": {
            "channel_count": channels,
            "fins_per_channel": fins,
            "active_fin_height_m": active_height,
            "total_projection_from_rail_plane_m": total_projection,
            "covered_fin_thickness_m": covered_fin_thickness,
            "slot_width_m": slot_width,
            "stationary_comb_span_m": stationary_comb_span,
            "rail_edge_to_comb_clearance_m": rail_edge_clearance,
            "usable_face_width_between_rail_keepouts_m": usable_face_width,
            "projected_usable_face_fraction": projected_usable_face_fraction,
            "assumed_rail_contact_fraction": assumed_rail_contact_fraction,
            "active_area_m2_per_channel": active_area_per_channel,
            "nominal_effective_gap_per_side_m": (
                comb["side_cover_per_side_m"] + comb["clearance_per_side_m"]
            ),
        },
        "moving_mass": {
            "segmented_steel_kg": steel_mass,
            "side_and_tip_cover_kg": cover_mass,
            "root_capture_fastener_allowance_kg": comb["root_capture_fastener_allowance_kg"],
            "interface_increment_kg": interface_mass,
        },
        "force_allocation": {
            "qualification_total_force_n": total_force,
            "grid_point_count": len(records),
            "minimum_channel_force_n": minimum_force,
            "maximum_channel_force_n": maximum_force,
            "maximum_channel_fraction": maximum_fraction,
            "maximum_force_sum_error_n": snap_residual(maximum_sum_error),
            "maximum_centroid_error_m": snap_residual(maximum_centroid_error),
            "required_developed_shear_pa": developed_shear,
            "records": records,
        },
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_COMB_FIN_TO_NONLINEAR_FEA_AND_PROVIDER_REVIEW"
            if all(bands.values())
            else "DO_NOT_PROMOTE_COMB_FIN"
        ),
        "limits": [
            "No selected dispenser or launch provider has accepted the interface.",
            "No structural, vibration, wear or debris analysis is present.",
            "No electromagnetic force, voltage, loss, thermal or normal-force result is present.",
            "The 50 g root/capture/fastener value is a mass allowance, not a design.",
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

