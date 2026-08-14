"""Bolley A5b: interface and ideal force screen for the four-fin 6 mm quad-comb.

The bands in validation/A5b_quad_comb_envelope.md were committed before the first output. This
screen cannot replace provider review, nonlinear 3D FEA, structural analysis or measurement.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json, snap_residual
from edge_force_bound import ideal_force_n
from interface_fit_screen import cardinal_centroid, cardinal_forces


INPUT = ROOT / "cad" / "quad_comb_parameters.json"
BASELINE = RESULTS / "baseline.json"
OUTPUT = RESULTS / "quad_comb_screen.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load(INPUT)
    baseline = load(BASELINE)
    interface = p["interface"]
    comb = p["quad_comb"]
    guidance = p["external_guidance"]
    material = p["material_anchor"]
    limits = p["bands"]

    channels = interface["channel_count"]
    fins = comb["fins_per_channel"]
    active_height = comb["active_fin_height_m"]
    active_length = interface["active_length_m"]
    covered_fin_thickness = comb["steel_thickness_m"] + 2.0 * comb["side_cover_per_side_m"]
    slot_width = covered_fin_thickness + 2.0 * comb["clearance_per_side_m"]
    stationary_comb_span = fins * slot_width + (fins + 1) * comb["stationary_pole_web_width_m"]
    total_projection = active_height + comb["radial_tip_cover_m"]
    protrusion_margin = guidance["maximum_side_protrusion_from_rail_plane_m"] - total_projection
    rail_edge_clearance = 0.5 * (interface["body_face_span_m"] - stationary_comb_span)
    usable_face_width = (
        interface["body_face_span_m"]
        - 2.0 * guidance["minimum_rail_width_to_first_protrusion_m"]
    )
    projected_usable_face_fraction = stationary_comb_span / usable_face_width
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

    tooth_count_float = active_length / comb["pole_pitch_m"]
    tooth_count = round(tooth_count_float)
    if not math.isclose(tooth_count_float, tooth_count, abs_tol=1e-12):
        raise ValueError("active length must contain an integer number of pole pitches")
    active_edge_count = fins * tooth_count
    effective_gap = comb["side_cover_per_side_m"] + comb["clearance_per_side_m"]
    force_coefficient = ideal_force_n(1.0, active_edge_count, effective_gap, active_height)
    required_ideal_flux_density = math.sqrt(limits["maximum_channel_force_n"] / force_coefficient)
    design_field = material["design_flux_density_t"]
    ideal_force_at_design_field = ideal_force_n(
        design_field, active_edge_count, effective_gap, active_height
    )
    ideal_force_margin_fraction = (
        ideal_force_at_design_field / limits["maximum_channel_force_n"] - 1.0
    )

    bands = {
        "side_protrusion": total_projection <= guidance["maximum_side_protrusion_from_rail_plane_m"],
        "nominal_protrusion_margin": protrusion_margin >= limits["minimum_nominal_protrusion_margin_m"],
        "rail_edge_keepout": rail_edge_clearance >= guidance["minimum_rail_width_to_first_protrusion_m"],
        "rail_contact": assumed_rail_contact_fraction >= guidance["minimum_rail_contact_fraction"],
        "stationary_comb_between_rail_keepouts": stationary_comb_span <= usable_face_width,
        "projected_usable_face_fraction": projected_usable_face_fraction <= limits["maximum_projected_usable_face_fraction"],
        "interface_mass_preferred": interface_mass <= limits["preferred_interface_mass_kg"],
        "interface_mass_absolute": interface_mass <= limits["absolute_interface_mass_kg"],
        "positive_force_allocation": all_positive,
        "maximum_channel_force": maximum_force <= limits["maximum_channel_force_n"],
        "nominal_slot_clearance": comb["clearance_per_side_m"] >= limits["minimum_nominal_clearance_per_side_m"],
        "tip_cover_not_thinner_than_side_cover": comb["radial_tip_cover_m"] >= comb["side_cover_per_side_m"],
        "ideal_force_at_design_field": ideal_force_at_design_field >= limits["maximum_channel_force_n"],
        "ideal_force_margin_at_design_field": ideal_force_margin_fraction >= limits["minimum_ideal_force_margin_fraction_at_design_field"],
        "required_ideal_flux_density_hard": required_ideal_flux_density <= limits["optimistic_hard_flux_density_ceiling_t"],
    }

    return {
        "evidence": "ANALYTICAL MODEL OUTPUT from ASSUMPTION geometry checked against named EXTERNAL GUIDANCE/MATERIAL DATA",
        "input_file": "cad/quad_comb_parameters.json",
        "source_warning": "CDS and catalogue values are screening anchors; provider requirements and a selected B-H curve supersede them",
        "geometry": {
            "channel_count": channels,
            "fins_per_channel": fins,
            "active_tooth_count_per_fin": tooth_count,
            "active_edge_count_per_channel": active_edge_count,
            "axial_fin_phase": comb["axial_fin_phase"],
            "active_fin_height_m": active_height,
            "total_projection_from_rail_plane_m": total_projection,
            "nominal_protrusion_margin_m": protrusion_margin,
            "covered_fin_thickness_m": covered_fin_thickness,
            "slot_width_m": slot_width,
            "stationary_comb_span_m": stationary_comb_span,
            "rail_edge_to_comb_clearance_m": rail_edge_clearance,
            "usable_face_width_between_rail_keepouts_m": usable_face_width,
            "projected_usable_face_fraction": projected_usable_face_fraction,
            "assumed_rail_contact_fraction": assumed_rail_contact_fraction,
            "active_long_face_area_m2_per_channel": 2.0 * fins * active_height * active_length,
            "nominal_effective_gap_per_side_m": effective_gap,
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
            "records": records,
        },
        "ideal_edge_force_bound": {
            "coefficient_n_per_t2": force_coefficient,
            "design_flux_density_t": design_field,
            "ideal_force_at_design_field_n": ideal_force_at_design_field,
            "ideal_force_margin_fraction_at_design_field": ideal_force_margin_fraction,
            "required_ideal_flux_density_t": required_ideal_flux_density,
            "warning": "This is the same optimistic gap-only bound used to reject A5a, not a nonlinear force prediction.",
        },
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "screen_pass": all(bands.values()),
        "disposition": (
            "PROMOTE_QUAD_COMB_TO_A3B1_NONLINEAR_3D_MODEL"
            if all(bands.values())
            else "DO_NOT_PROMOTE_QUAD_COMB"
        ),
        "limits": [
            "No selected dispenser or launch provider has accepted the interface.",
            "No structural, vibration, wear, tolerance-stack or debris analysis is present.",
            "The ideal force bound ignores finite permeability, leakage, fringing and end effects.",
            "No coil, return-yoke, current, voltage, switching, loss, thermal or normal-force design is present.",
            "Aligned fins maximize simultaneous ideal edge count; continuous force still requires launcher-side axial phasing.",
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
