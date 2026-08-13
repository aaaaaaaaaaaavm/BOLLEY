"""Bolley A1: first-order kinematic, mass, force-area and energy screen.

This is a screen, not an electromagnetic motor model. Run-sheet bands were committed in
validation/A1_first_order_sizing.md before its first recorded output.
"""

from __future__ import annotations

import argparse
import math

from common import RESULTS, compare_json, dump_json, load_parameters, rail_forces


OUTPUT = RESULTS / "baseline.json"


def calculate() -> dict:
    p = load_parameters()
    payload = p["payload"]
    duty = p["duty"]
    rail = p["rail"]
    screen = p["screens"]
    g = p["constants"]["gravity_m_s2"]

    acceleration = duty["acceleration_g"] * g
    velocity = math.sqrt(2.0 * acceleration * duty["powered_length_m"])
    total_face_area = (
        rail["corner_count"]
        * rail["faces_per_corner"]
        * rail["active_width_per_face_m"]
        * rail["magnetic_active_length_m"]
    )
    corner_face_area = total_face_area / rail["corner_count"]
    magnetic_mass = (
        total_face_area
        * rail["magnetic_equivalent_thickness_m"]
        * rail["magnetic_density_kg_m3"]
    )
    interface_mass = magnetic_mass + rail["nonmagnetic_increment_kg"]

    reference_moving_mass = payload["reference_mass_kg"] + interface_mass
    qualification_moving_mass = payload["qualification_mass_kg"] + interface_mass
    reference_force = reference_moving_mass * acceleration
    qualification_force = qualification_moving_mass * acceleration

    limit = payload["transverse_cg_limit_m"]
    radius = rail["force_line_radius_m"]
    worst_forces = rail_forces(qualification_force, limit, limit, radius)
    worst_channel_force = max(worst_forces.values())
    required_shear = worst_channel_force / corner_face_area

    reference_ke = 0.5 * reference_moving_mass * velocity**2
    payload_ke = 0.5 * payload["reference_mass_kg"] * velocity**2
    energy_low_efficiency = reference_ke / screen["efficiency_low"]
    energy_high_efficiency = reference_ke / screen["efficiency_high"]
    peak_mechanical_power = reference_force * velocity
    pole_passage = velocity / rail["pole_pitch_m"]
    utilisation = payload["reference_mass_kg"] / reference_moving_mass

    bands = {
        "velocity_11p8_to_12p0": 11.8 <= velocity <= 12.0,
        "interface_mass_preferred": interface_mass <= screen["rail_mass_preferred_kg"],
        "interface_mass_absolute": interface_mass <= screen["rail_mass_kill_kg"],
        "required_shear": required_shear <= screen["required_shear_band_pa"],
        "channel_force": worst_channel_force <= screen["channel_force_band_n"],
        "mechanical_utilisation": utilisation >= 0.94,
        "gross_energy_at_40pct": energy_low_efficiency <= screen["gross_energy_limit_j"],
        "pole_passage": pole_passage <= screen["pole_passage_band_hz"],
    }

    return {
        "evidence": "MODEL OUTPUT from ASSUMPTION inputs; not experimentally validated",
        "inputs": {
            "reference_payload_kg": payload["reference_mass_kg"],
            "qualification_payload_kg": payload["qualification_mass_kg"],
            "acceleration_g": duty["acceleration_g"],
            "powered_length_m": duty["powered_length_m"],
            "cg_limit_m": limit,
        },
        "interface": {
            "total_active_face_area_m2": total_face_area,
            "active_face_area_per_corner_m2": corner_face_area,
            "magnetic_material_mass_kg": magnetic_mass,
            "screened_incremental_mass_kg": interface_mass,
            "effective_nominal_gap_m": rail["aluminium_cover_m"] + rail["mechanical_clearance_m"],
        },
        "reference_case": {
            "moving_mass_kg": reference_moving_mass,
            "acceleration_m_s2": acceleration,
            "exit_velocity_m_s": velocity,
            "total_force_n": reference_force,
            "payload_ke_j": payload_ke,
            "total_moving_ke_j": reference_ke,
            "mechanical_utilisation_fraction": utilisation,
            "gross_energy_screen_j_at_40pct": energy_low_efficiency,
            "gross_energy_screen_j_at_60pct": energy_high_efficiency,
            "peak_mechanical_power_w": peak_mechanical_power,
            "pole_passage_hz": pole_passage,
        },
        "qualification_case": {
            "moving_mass_kg": qualification_moving_mass,
            "total_force_n": qualification_force,
            "worst_corner_force_n": worst_channel_force,
            "required_worst_corner_shear_pa": required_shear,
            "published_shear_benchmark_pa": screen["published_shear_benchmark_pa"],
            "benchmark_margin_fraction": screen["published_shear_benchmark_pa"] / required_shear - 1.0,
        },
        "bands": bands,
        "overall_pass": all(bands.values()),
        "limits": [
            "No flux-linkage, saturation, normal-force, voltage or thermal model is present.",
            "The efficiency range is an assumption used only for an energy screen.",
            "The external shear benchmark is not performance evidence for this geometry.",
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

