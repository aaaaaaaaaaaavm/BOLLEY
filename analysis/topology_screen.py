"""Bolley A3a: analytical moving-interface topology screen.

This is not FEA and does not predict motor force. The bands in
validation/A3a_flux_path_screen.md were committed before the first recorded output.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "cad" / "topology_candidates.json"
FORCE_RESULT = RESULTS / "force_allocation.json"
BASELINE_RESULT = RESULTS / "baseline.json"
OUTPUT = RESULTS / "topology_screen.json"
MU_0 = 4.0e-7 * math.pi


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def l_return_mass(normal_gap_flux_t: float, candidate: dict, common: dict) -> dict:
    width = candidate["active_width_per_face_m"]
    core_b = candidate["core_flux_density_screen_t"]
    leg_depth = normal_gap_flux_t / core_b * width
    l_area = 2.0 * width * leg_depth - leg_depth**2
    tooth_length = candidate["pole_pitch_m"] * candidate["tooth_duty_fraction"]
    steel_volume = (
        common["channel_count"]
        * candidate["tooth_count_per_channel"]
        * l_area
        * tooth_length
    )
    steel_mass = steel_volume * common["steel_density_kg_m3"]
    return {
        "normal_gap_flux_t": normal_gap_flux_t,
        "leg_depth_m": leg_depth,
        "l_cross_section_m2": l_area,
        "steel_mass_kg": steel_mass,
        "interface_increment_kg": steel_mass + common["moving_nonactive_allowance_kg"],
    }


def flux_at_mass_limit(limit_kg: float, candidate: dict, common: dict) -> float:
    low = 0.0
    high = candidate["core_flux_density_screen_t"]
    for _ in range(80):
        middle = 0.5 * (low + high)
        mass = l_return_mass(middle, candidate, common)["interface_increment_kg"]
        if mass <= limit_kg:
            low = middle
        else:
            high = middle
    return low


def active_area(candidate: dict, common: dict) -> float:
    return (
        candidate["active_faces_per_channel"]
        * candidate["active_width_per_face_m"]
        * common["active_length_m"]
    )


def calculate() -> dict:
    inputs = load(INPUT)
    common = inputs["common"]
    force_result = load(FORCE_RESULT)
    baseline = load(BASELINE_RESULT)
    worst_force = force_result["maximum_channel_force_n"]
    required_area = worst_force / common["required_shear_band_pa"]

    corner = inputs["corner_l_return"]
    fin = inputs["opposed_through_flux_fin"]
    induction = inputs["single_sided_induction_lane"]
    corner_area = active_area(corner, common)
    fin_area = active_area(fin, common)
    induction_area = active_area(induction, common)
    required_shear = worst_force / corner_area
    ideal_equal_component_b = math.sqrt(MU_0 * required_shear)

    preferred_flux_cap = flux_at_mass_limit(
        common["preferred_interface_mass_kg"], corner, common
    )
    kill_flux_cap = flux_at_mass_limit(common["kill_interface_mass_kg"], corner, common)
    l_sweep = [l_return_mass(value, corner, common) for value in corner["normal_gap_flux_sweep_t"]]

    fin_steel_volume = (
        common["channel_count"]
        * fin["active_width_per_face_m"]
        * common["active_length_m"]
        * fin["tooth_duty_fraction"]
        * fin["steel_thickness_m"]
    )
    fin_steel_mass = fin_steel_volume * common["steel_density_kg_m3"]
    fin_mass = fin_steel_mass + common["moving_nonactive_allowance_kg"]

    induction_volume = (
        common["channel_count"]
        * induction["active_width_per_face_m"]
        * common["active_length_m"]
        * induction["conductor_thickness_m"]
    )
    induction_conductor_mass = induction_volume * common["aluminium_density_kg_m3"]
    induction_mass = induction_conductor_mass + common["moving_nonactive_allowance_kg"]
    frequency = baseline["reference_case"]["pole_passage_hz"]
    permeability = MU_0 * induction["relative_permeability"]
    skin_depth = math.sqrt(
        2.0 * induction["aluminium_resistivity_ohm_m"]
        / (2.0 * math.pi * frequency * permeability)
    )

    bands = {
        "corner_active_area": corner_area >= required_area,
        "corner_preferred_mass_supports_ideal_equal_component_field": (
            preferred_flux_cap >= ideal_equal_component_b
        ),
        "opposed_fin_active_area": fin_area >= required_area,
        "opposed_fin_preferred_mass": fin_mass <= common["preferred_interface_mass_kg"],
        "induction_lane_active_area": induction_area >= required_area,
        "induction_lane_preferred_mass": induction_mass <= common["preferred_interface_mass_kg"],
        "at_least_one_candidate_passes_area_and_preferred_mass": any(
            (
                corner_area >= required_area
                and preferred_flux_cap >= ideal_equal_component_b,
                fin_area >= required_area and fin_mass <= common["preferred_interface_mass_kg"],
                induction_area >= required_area
                and induction_mass <= common["preferred_interface_mass_kg"],
            )
        ),
    }

    return {
        "evidence": "ANALYTICAL MODEL OUTPUT from ASSUMPTION inputs; not FEA or measurement",
        "inputs_file": "cad/topology_candidates.json",
        "force_source": "analysis/results/force_allocation.json",
        "worst_channel_force_n": worst_force,
        "required_area_at_band_m2_per_channel": required_area,
        "required_shear_on_equal_area_pa": required_shear,
        "maxwell_stress_screen": {
            "relation": "tau = Bn * Bt / mu0",
            "optimistic_equal_component_flux_t": ideal_equal_component_b,
            "interpretation": "lower-bound field component only; not a motor prediction",
        },
        "candidates": {
            "corner_l_return": {
                "active_area_m2_per_channel": corner_area,
                "preferred_mass_normal_flux_cap_t": preferred_flux_cap,
                "kill_mass_normal_flux_cap_t": kill_flux_cap,
                "preferred_flux_cap_to_ideal_equal_component_ratio": (
                    preferred_flux_cap / ideal_equal_component_b
                ),
                "kill_flux_cap_to_ideal_equal_component_ratio": (
                    kill_flux_cap / ideal_equal_component_b
                ),
                "sweep": l_sweep,
                "disposition": (
                    "PROMOTE_TO_NONLINEAR_FEA"
                    if bands["corner_preferred_mass_supports_ideal_equal_component_field"]
                    else "DO_NOT_PROMOTE_AS_PRIMARY"
                ),
                "unresolved": [
                    "actual normal/tangential field ratio",
                    "leakage and corner fringing",
                    "nonlinear B-H saturation",
                    "cover and adhesive gap",
                ],
            },
            "opposed_through_flux_fin": {
                "active_area_m2_per_channel": fin_area,
                "steel_mass_kg": fin_steel_mass,
                "interface_increment_kg": fin_mass,
                "double_sided_access_proven": fin["double_sided_access_proven"],
                "disposition": "PROMOTE_TO_INTERFACE_FIT_THEN_NONLINEAR_FEA",
                "unresolved": [
                    "double-sided stator access",
                    "fin buckling and capture",
                    "nonlinear force and normal-force balance",
                ],
            },
            "single_sided_induction_lane": {
                "active_area_m2_per_channel": induction_area,
                "conductor_mass_kg": induction_conductor_mass,
                "interface_increment_kg": induction_mass,
                "pole_passage_frequency_hz": frequency,
                "aluminium_skin_depth_m": skin_depth,
                "thickness_to_skin_depth_ratio": induction["conductor_thickness_m"] / skin_depth,
                "force_and_thermal_model_complete": induction["force_and_thermal_model_complete"],
                "disposition": "RETAIN_AS_TRANSIENT_MODEL_FALLBACK",
                "unresolved": [
                    "starting and terminal slip",
                    "secondary joule heating",
                    "end and edge effects",
                    "attractive normal force",
                ],
            },
        },
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "screen_survives": bands["at_least_one_candidate_passes_area_and_preferred_mass"],
        "limits": [
            "No candidate force is predicted.",
            "The steel flux-density screen is not a material B-H curve.",
            "Maxwell stress is an optimistic local-field bound, not average motor shear.",
            "Mechanical access is deliberately left to A5 cross-section fit work.",
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

