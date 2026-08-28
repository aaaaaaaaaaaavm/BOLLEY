"""Bolley A11: Fluxpiston chamber fill, controlled leakage and feed screen."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "analysis" / "fluxpiston_flow_parameters.json"
OUTPUT = RESULTS / "fluxpiston_flow.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def choked_mass_flux(
    pressure_pa: float,
    temperature_k: float,
    gamma: float,
    gas_constant: float,
    discharge_coefficient: float,
) -> float:
    critical = (2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (2.0 * (gamma - 1.0)))
    return (
        discharge_coefficient
        * pressure_pa
        * math.sqrt(gamma / (gas_constant * temperature_k))
        * critical
    )


def kinetic_energy(mass_kg: float, velocity_m_s: float) -> float:
    return 0.5 * mass_kg * velocity_m_s**2


def trim_energy(mass_kg: float, gas_velocity: float, command_velocity: float) -> float:
    return kinetic_energy(mass_kg, command_velocity) - kinetic_energy(mass_kg, gas_velocity)


def calculate() -> dict:
    p = load(INPUT)
    fluid = p["fluid"]
    bands = p["bands"]
    stroke = p["stroke_m"]
    face_area = p["effective_face_area_m2"]
    swept_volume = face_area * stroke
    records = []
    case_summaries = {}

    for case_name, case in p["cases"].items():
        mass = case["payload_mass_kg"]
        velocity = case["gas_velocity_m_s"]
        energy = kinetic_energy(mass, velocity)
        mean_force = energy / stroke
        chamber_pressure = mean_force / face_area
        acceleration = mean_force / mass
        pressure_cap = mass * p["acceleration_limit_g"] * p["gravity_m_s2"] / face_area
        pressure_headroom = (pressure_cap - chamber_pressure) / pressure_cap
        shot_time = 2.0 * stroke / velocity
        case_records = []

        for clearance in p["clearance_m"]:
            leakage_area = p["moving_perimeter_m"] * clearance
            for temperature in p["temperature_k"]:
                leak_flux = choked_mass_flux(
                    chamber_pressure,
                    temperature,
                    fluid["heat_capacity_ratio"],
                    fluid["specific_gas_constant_j_kg_k"],
                    fluid["discharge_coefficient"],
                )
                leakage_rate = leak_flux * leakage_area
                leakage_mass = leakage_rate * shot_time
                chamber_fill_mass = (
                    chamber_pressure
                    * (p["dead_volume_m3"] + swept_volume)
                    / (fluid["specific_gas_constant_j_kg_k"] * temperature)
                )
                peak_volume_growth_rate = face_area * velocity
                peak_fill_rate = (
                    chamber_pressure
                    * peak_volume_growth_rate
                    / (fluid["specific_gas_constant_j_kg_k"] * temperature)
                )
                peak_supply_rate = peak_fill_rate + leakage_rate
                reservoir_flux = choked_mass_flux(
                    p["reservoir_pressure_pa"],
                    temperature,
                    fluid["heat_capacity_ratio"],
                    fluid["specific_gas_constant_j_kg_k"],
                    p["reservoir_discharge_coefficient"],
                )
                supply_area = peak_supply_rate / reservoir_flux
                supply_diameter = math.sqrt(4.0 * supply_area / math.pi)
                record = {
                    "case": case_name,
                    "clearance_m": clearance,
                    "temperature_k": temperature,
                    "leakage_area_m2": leakage_area,
                    "leakage_rate_kg_s": leakage_rate,
                    "leakage_mass_kg": leakage_mass,
                    "chamber_fill_mass_kg": chamber_fill_mass,
                    "total_gas_mass_kg": chamber_fill_mass + leakage_mass,
                    "peak_fill_rate_kg_s": peak_fill_rate,
                    "peak_supply_rate_kg_s": peak_supply_rate,
                    "equivalent_supply_orifice_area_m2": supply_area,
                    "equivalent_supply_orifice_diameter_m": supply_diameter,
                }
                records.append(record)
                case_records.append(record)

        worst_mass = max(case_records, key=lambda row: row["total_gas_mass_kg"])
        worst_feed = max(case_records, key=lambda row: row["equivalent_supply_orifice_diameter_m"])
        case_summaries[case_name] = {
            "payload_mass_kg": mass,
            "command_velocity_m_s": case["command_velocity_m_s"],
            "gas_velocity_m_s": velocity,
            "trim_delta_v_m_s": case["command_velocity_m_s"] - velocity,
            "gas_kinetic_energy_j": energy,
            "trim_kinetic_energy_j": trim_energy(
                mass, velocity, case["command_velocity_m_s"]
            ),
            "mean_force_n": mean_force,
            "mean_chamber_pressure_pa": chamber_pressure,
            "gas_acceleration_g": acceleration / p["gravity_m_s2"],
            "pressure_cap_at_8g_pa": pressure_cap,
            "pressure_headroom_fraction": pressure_headroom,
            "shot_time_s": shot_time,
            "swept_volume_m3": swept_volume,
            "worst_gas_mass_point": worst_mass,
            "worst_feed_point": worst_feed,
        }

    worst_mass_record = max(records, key=lambda row: row["total_gas_mass_kg"])
    worst_feed_record = max(
        records, key=lambda row: row["equivalent_supply_orifice_diameter_m"]
    )
    maximum_acceleration = max(
        case["gas_acceleration_g"] for case in case_summaries.values()
    )
    minimum_headroom = min(
        case["pressure_headroom_fraction"] for case in case_summaries.values()
    )
    maximum_trim = max(
        case["trim_kinetic_energy_j"] for case in case_summaries.values()
    )
    campaign_mass = p["shot_count"] * worst_mass_record["total_gas_mass_kg"]
    reservoir_volume = (
        campaign_mass
        * fluid["specific_gas_constant_j_kg_k"]
        * max(p["temperature_k"])
        / p["reservoir_pressure_pa"]
    )

    checks = [
        {
            "id": 1,
            "name": "maximum gas-stage acceleration",
            "value": maximum_acceleration,
            "limit": bands["maximum_gas_acceleration_g"],
            "status": "PASS"
            if maximum_acceleration <= bands["maximum_gas_acceleration_g"]
            else "FAIL",
        },
        {
            "id": 2,
            "name": "minimum pressure headroom to 8 g",
            "value": minimum_headroom,
            "limit": bands["minimum_pressure_headroom_fraction"],
            "status": "PASS"
            if minimum_headroom >= bands["minimum_pressure_headroom_fraction"]
            else "FAIL",
        },
        {
            "id": 3,
            "name": "worst gas mass per shot",
            "value": worst_mass_record["total_gas_mass_kg"],
            "limit": bands["maximum_gas_mass_per_shot_kg"],
            "status": "PASS"
            if worst_mass_record["total_gas_mass_kg"]
            <= bands["maximum_gas_mass_per_shot_kg"]
            else "FAIL",
        },
        {
            "id": 4,
            "name": "twelve-shot campaign gas mass",
            "value": campaign_mass,
            "limit": bands["maximum_campaign_gas_mass_kg"],
            "status": "PASS"
            if campaign_mass <= bands["maximum_campaign_gas_mass_kg"]
            else "FAIL",
        },
        {
            "id": 5,
            "name": "equivalent 20 bar reservoir volume",
            "value": reservoir_volume,
            "limit": bands["maximum_equivalent_reservoir_volume_m3"],
            "status": "PASS"
            if reservoir_volume <= bands["maximum_equivalent_reservoir_volume_m3"]
            else "FAIL",
        },
        {
            "id": 6,
            "name": "peak equivalent supply-orifice diameter",
            "value": worst_feed_record["equivalent_supply_orifice_diameter_m"],
            "limit": bands["maximum_supply_orifice_diameter_m"],
            "status": "PASS"
            if worst_feed_record["equivalent_supply_orifice_diameter_m"]
            <= bands["maximum_supply_orifice_diameter_m"]
            else "FAIL",
        },
        {
            "id": 7,
            "name": "maximum trim kinetic energy",
            "value": maximum_trim,
            "limit": bands["maximum_trim_energy_j"],
            "status": "PASS" if maximum_trim <= bands["maximum_trim_energy_j"] else "FAIL",
        },
        {
            "id": 8,
            "name": "complete clearance and temperature grid retained",
            "value": len(records),
            "limit": len(p["cases"]) * len(p["clearance_m"]) * len(p["temperature_k"]),
            "status": "PASS"
            if len(records)
            == len(p["cases"]) * len(p["clearance_m"]) * len(p["temperature_k"])
            else "FAIL",
        },
        {
            "id": 9,
            "name": "friction, contact, rarefied flow and plume evidence",
            "value": None,
            "limit": "MODEL_AND_TEST_REQUIRED",
            "status": "OPEN",
        },
    ]
    pass_count = sum(check["status"] == "PASS" for check in checks)

    return {
        "schema": "bolley.fluxpiston-flow.result/1",
        "evidence_class": "IDEAL_GAS_PLUS_CHOKED_CLEARANCE_FLOW_SCREEN",
        "controlled_input": str(INPUT.relative_to(ROOT)),
        "case_summaries": case_summaries,
        "grid": records,
        "campaign": {
            "shot_count": p["shot_count"],
            "worst_gas_mass_per_shot_kg": worst_mass_record["total_gas_mass_kg"],
            "worst_corner": {
                "case": worst_mass_record["case"],
                "clearance_m": worst_mass_record["clearance_m"],
                "temperature_k": worst_mass_record["temperature_k"],
            },
            "campaign_gas_mass_kg": campaign_mass,
            "equivalent_reservoir_volume_m3_at_20bar_and_330k": reservoir_volume,
            "maximum_supply_orifice_diameter_m": worst_feed_record[
                "equivalent_supply_orifice_diameter_m"
            ],
        },
        "checks": checks,
        "pass_count": pass_count,
        "check_count": len(checks),
        "disposition": "PROMOTE_TO_DYNAMIC_REGULATOR_BLOWDOWN_AND_CONTACT_GATE_NOT_CAD",
        "limitations": [
            "constant mean chamber pressure",
            "ideal gas",
            "continuum choked flow to vacuum",
            "no valve or regulator dynamics",
            "no wall heat transfer",
            "no seal contact or guide friction",
            "no plume impulse or contamination",
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
