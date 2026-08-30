"""Bolley A9c: derive the resistance ceiling left by my 900 J reference-shot cap."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "analysis" / "hot_winding_margin_parameters.json"
OUTPUT = RESULTS / "hot_winding_margin.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load(INPUT)
    c = p["controlled_corner"]
    ext = p["external_datum"]
    limit = p["bands"]["maximum_reference_source_energy_j"]

    m0 = c["resistance_multiplier_low"]
    m1 = c["resistance_multiplier_high"]
    e0 = c["a7c_reference_energy_low_j"]
    e1 = c["a7c_reference_energy_high_j"]
    a9b_energy = c["a9b_reference_energy_j"]

    slope = (e1 - e0) / (m1 - m0)
    selector_overhead = a9b_energy - e1
    maximum_multiplier = m0 + (limit - selector_overhead - e0) / slope
    reconstructed_limit = e0 + slope * (maximum_multiplier - m0) + selector_overhead

    alpha = ext["temperature_coefficient_per_c"]
    tref = ext["reference_temperature_c"]
    maximum_ideal_copper_temperature = tref + (maximum_multiplier - 1.0) / alpha
    a7c_hot_corner_temperature = tref + (m1 - 1.0) / alpha

    checks = {
        "positive_energy_slope": slope > 0.0,
        "a9b_is_above_a7c_hot_corner": selector_overhead > 0.0,
        "solved_multiplier_above_existing_1p25_corner": maximum_multiplier > m1,
        "back_substitution_hits_900j": abs(reconstructed_limit - limit) <= 1e-9,
    }

    return {
        "evidence": "A9c DERIVED RESISTANCE/TEMPERATURE CEILING FROM COMMITTED MODEL OUTPUTS AND NIST COPPER DATUM",
        "input_file": str(INPUT.relative_to(ROOT)),
        "a7c_reference_energy_slope_j_per_resistance_multiplier": slope,
        "a9_selector_source_overhead_j": selector_overhead,
        "a9b_margin_to_900j_j": limit - a9b_energy,
        "maximum_phase_resistance_multiplier": maximum_multiplier,
        "remaining_multiplier_above_a7c_1p25_corner": maximum_multiplier - m1,
        "a7c_1p25_equivalent_ideal_copper_temperature_c": a7c_hot_corner_temperature,
        "maximum_equivalent_ideal_copper_temperature_c": maximum_ideal_copper_temperature,
        "remaining_temperature_above_a7c_1p25_corner_c": maximum_ideal_copper_temperature - a7c_hot_corner_temperature,
        "back_substituted_reference_source_energy_j": reconstructed_limit,
        "external_datum": ext,
        "checks": checks,
        "check_pass_count": sum(checks.values()),
        "check_count": len(checks),
        "screen_pass": all(checks.values()),
        "disposition": "A9C_TARGET_DEFINED_P40_REMAINS_OPEN",
        "limits": [
            "The temperature conversion assumes the model's 1.00 resistance state is the finished winding at 20 C.",
            "Manufacturing tolerance, terminations, cable resistance and semiconductor loss can consume the derived margin before copper temperature does.",
            "The NIST copper coefficient does not establish a manufactured winding state or hardware qualification."
        ]
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
