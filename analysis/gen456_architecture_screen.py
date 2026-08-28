"""Bolley A10: architecture-independent Gen4-Gen6 premise screen."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "analysis" / "gen456_parameters.json"
OUTPUT = RESULTS / "gen456_architecture_screen.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def kinetic_energy(mass_kg: float, velocity_m_s: float) -> float:
    return 0.5 * mass_kg * velocity_m_s**2


def trim_energy(mass_kg: float, velocity_m_s: float, authority_m_s: float) -> float:
    upper = kinetic_energy(mass_kg, velocity_m_s + authority_m_s)
    lower = kinetic_energy(mass_kg, max(0.0, velocity_m_s - authority_m_s))
    nominal = kinetic_energy(mass_kg, velocity_m_s)
    return max(upper - nominal, nominal - lower)


def band(identifier: int, name: str, value, limit, status: str, note: str) -> dict:
    return {
        "id": identifier,
        "name": name,
        "value": value,
        "limit": limit,
        "status": status,
        "note": note,
    }


def calculate() -> dict:
    control = load(INPUT)
    gravity = control["gravity_m_s2"]
    stroke = control["powered_stroke_m"]
    acceleration_limit = control["acceleration_limit_g"] * gravity
    reference = control["reference"]
    qualification = control["qualification"]
    fluxrelay = control["fluxrelay"]
    piston = control["fluxpiston"]

    maximum_velocity = math.sqrt(2.0 * acceleration_limit * stroke)
    required_acceleration_for_12 = reference["target_velocity_m_s"] ** 2 / (2.0 * stroke)
    required_stroke_for_12 = reference["target_velocity_m_s"] ** 2 / (2.0 * acceleration_limit)

    displaced_mass_needed = max(
        0.0,
        fluxrelay["gross_interface_mass_kg"] - control["interface_mass_preference_kg"],
    )
    displaced_fraction = displaced_mass_needed / fluxrelay["gross_interface_mass_kg"]

    pressure_cases = {}
    for name, case, target_velocity in (
        (
            "reference",
            reference,
            reference["consistent_screen_velocity_m_s"],
        ),
        (
            "qualification",
            qualification,
            qualification["target_velocity_m_s"],
        ),
    ):
        energy = kinetic_energy(case["payload_mass_kg"], target_velocity)
        average_force = energy / stroke
        mean_pressure = average_force / piston["effective_face_area_m2"]
        average_acceleration = average_force / case["payload_mass_kg"]
        pressure_cases[name] = {
            "payload_mass_kg": case["payload_mass_kg"],
            "target_velocity_m_s": target_velocity,
            "kinetic_energy_j": energy,
            "average_force_n": average_force,
            "mean_pressure_pa": mean_pressure,
            "average_acceleration_m_s2": average_acceleration,
            "average_acceleration_g": average_acceleration / gravity,
            "swept_volume_l": 1000.0 * piston["effective_face_area_m2"] * stroke,
        }

    trim_cases = {
        name: trim_energy(
            case["payload_mass_kg"],
            case["target_velocity_m_s"],
            piston["trim_velocity_authority_m_s"],
        )
        for name, case in pressure_cases.items()
    }
    maximum_trim_energy = max(trim_cases.values())
    first_interface_allocation = (
        piston["pressure_cup_mass_assumption_kg"]
        + piston["short_trim_secondary_mass_assumption_kg"]
    )

    strain_energy = pressure_cases["reference"]["kinetic_energy_j"]
    strain_specific_energy = strain_energy / control["strainrail"][
        "available_interface_mass_kg"
    ]

    burn_drop = [
        {
            "stage_acceleration_m_s2": acceleration,
            "time_s": control["burn_and_drop"]["relative_velocity_m_s"] / acceleration,
            "stage_delta_v_m_s": control["burn_and_drop"]["relative_velocity_m_s"],
        }
        for acceleration in control["burn_and_drop"]["stage_accelerations_m_s2"]
    ]

    bands = [
        band(
            1,
            "12 m/s, 0.90 m and 8 g are mutually consistent",
            maximum_velocity,
            reference["target_velocity_m_s"],
            "PASS" if maximum_velocity >= reference["target_velocity_m_s"] else "FAIL",
            "Architecture-independent constant-acceleration ceiling from rest.",
        ),
        band(
            2,
            "Fluxframe displaced mass needed for the preference",
            displaced_mass_needed,
            "REPORT",
            "REPORT",
            "I award no credit until a selected bus identifies removed parts.",
        ),
        band(
            3,
            "Fluxpiston reference mean pressure",
            pressure_cases["reference"]["mean_pressure_pa"],
            piston["pressure_screen_limit_pa"],
            "PASS"
            if pressure_cases["reference"]["mean_pressure_pa"]
            <= piston["pressure_screen_limit_pa"]
            else "FAIL",
            "Ideal constant-pressure work at the requirement-consistent 11.8 m/s screen point.",
        ),
        band(
            4,
            "Fluxpiston qualification mean pressure",
            pressure_cases["qualification"]["mean_pressure_pa"],
            piston["pressure_screen_limit_pa"],
            "PASS"
            if pressure_cases["qualification"]["mean_pressure_pa"]
            <= piston["pressure_screen_limit_pa"]
            else "FAIL",
            "Ideal constant-pressure work for 6 kg at 10 m/s.",
        ),
        band(
            5,
            "Both ideal pressure cases remain at or below 8 g",
            max(case["average_acceleration_g"] for case in pressure_cases.values()),
            control["acceleration_limit_g"],
            "PASS"
            if max(case["average_acceleration_g"] for case in pressure_cases.values())
            <= control["acceleration_limit_g"]
            else "FAIL",
            "This is a mean-force screen; valve and pressure transients remain open.",
        ),
        band(
            6,
            "Short electromagnetic trim energy",
            maximum_trim_energy,
            25.0,
            "PASS" if maximum_trim_energy <= 25.0 else "FAIL",
            "Largest kinetic-energy correction for +/-0.25 m/s.",
        ),
        band(
            7,
            "First Gen6 interface mass allocation",
            first_interface_allocation,
            control["interface_mass_preference_kg"],
            "PASS"
            if first_interface_allocation <= control["interface_mass_preference_kg"]
            else "FAIL",
            "Assumptions only; this excludes seal, capture, fasteners and structure.",
        ),
        band(
            8,
            "Spacecraft-side hardware remains passive",
            True,
            True,
            "PASS",
            "The concept adds no power, software, permanent magnet, pyro or pressure vessel.",
        ),
        band(
            9,
            "No launcher propulsion member follows the payload",
            True,
            True,
            "PASS",
            "The payload interface is the piston; the stage tube and trim stator remain.",
        ),
        band(
            10,
            "Seal leakage, friction and contamination evidence",
            None,
            "MEASUREMENT REQUIRED",
            "OPEN",
            "I do not convert ideal pressure work into seal evidence.",
        ),
        band(
            11,
            "Burn-and-drop thrust-arc timing",
            burn_drop,
            "REPORT",
            "REPORT",
            "Every case spends 12 m/s of host delta-v; time is not the only cost.",
        ),
        band(
            12,
            "Strainrail required specific energy",
            strain_specific_energy,
            control["strainrail"]["screen_specific_energy_limit_j_kg"],
            "PASS"
            if strain_specific_energy
            <= control["strainrail"]["screen_specific_energy_limit_j_kg"]
            else "FAIL",
            "I reject material-limit optimism at the current interface mass.",
        ),
    ]

    status_counts = {
        status: sum(item["status"] == status for item in bands)
        for status in ("PASS", "FAIL", "OPEN", "REPORT")
    }

    return {
        "schema": "bolley.gen456.architecture-screen.result/1",
        "evidence_class": "FIRST_ORDER_ARCHITECTURE_SCREEN",
        "controlled_input": str(INPUT.relative_to(ROOT)),
        "kinematic_consistency": {
            "maximum_velocity_at_8g_over_0p9m_m_s": maximum_velocity,
            "acceleration_required_for_12m_s_g": required_acceleration_for_12 / gravity,
            "stroke_required_for_12m_s_at_8g_m": required_stroke_for_12,
        },
        "fluxframe": {
            "gross_interface_mass_kg": fluxrelay["gross_interface_mass_kg"],
            "displaced_mass_needed_for_0p25kg_net_kg": displaced_mass_needed,
            "displaced_fraction_of_interface": displaced_fraction,
            "credit_status": "WITHHELD_PENDING_BUS_LEDGER",
        },
        "fluxpiston": {
            "pressure_cases": pressure_cases,
            "trim_energy_cases_j": trim_cases,
            "maximum_trim_energy_j": maximum_trim_energy,
            "first_interface_mass_allocation_kg": first_interface_allocation,
            "mass_allocation_status": "ASSUMPTION_NOT_CAD",
            "seal_status": "OPEN",
        },
        "burn_and_drop": burn_drop,
        "strainrail": {
            "required_energy_j": strain_energy,
            "available_interface_mass_kg": control["strainrail"][
                "available_interface_mass_kg"
            ],
            "required_specific_energy_j_kg": strain_specific_energy,
        },
        "bands": bands,
        "status_counts": status_counts,
        "disposition": {
            "requirements": "REJECT_INCONSISTENT_TRIPLET_AND_CORRECT_BY_ADR",
            "gen4": "RETAIN_FOR_A9_AND_PACKAGED_CLOSURE",
            "gen5": "PROMOTE_ONLY_TO_BUS_SPECIFIC_NET_MASS_GATE",
            "gen6": "PROMOTE_ONLY_TO_SEAL_PRESSURE_TRANSIENT_AND_TRIM_AUTHORITY_GATES",
            "strainrail": "REJECT_AT_CURRENT_MASS_AND_SPECIFIC_ENERGY_BAND",
            "burn_and_drop": "RETAIN_AS_MISSION_LEVEL_COMPARATOR",
        },
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
