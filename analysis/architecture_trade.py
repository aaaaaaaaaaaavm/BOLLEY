"""Common-duty moving-mass comparison. Electrical efficiency is deliberately excluded."""

from __future__ import annotations

import argparse

from baseline import calculate as calculate_baseline
from common import RESULTS, compare_json, dump_json


OUTPUT = RESULTS / "architecture_trade.json"


def calculate() -> dict:
    baseline = calculate_baseline()
    velocity = baseline["reference_case"]["exit_velocity_m_s"]
    payload_mass = baseline["inputs"]["reference_payload_kg"]
    interface_mass = baseline["interface"]["screened_incremental_mass_kg"]
    candidates = {
        "VOLLEY_sled_at_common_duty": {"launcher_moving_mass_kg": 9.445, "source": "VOLLEY model output"},
        "Bolley_U_target": {"launcher_moving_mass_kg": 0.8, "source": "design target"},
        "Bolley_R_baseline": {"launcher_moving_mass_kg": interface_mass, "source": "first-order screen"},
    }
    for item in candidates.values():
        total = payload_mass + item["launcher_moving_mass_kg"]
        item["total_moving_mass_kg"] = total
        item["payload_mass_fraction"] = payload_mass / total
        item["total_mechanical_energy_j"] = 0.5 * total * velocity**2
        item["nonpayload_mechanical_energy_j"] = 0.5 * item["launcher_moving_mass_kg"] * velocity**2

    return {
        "evidence": "MODEL OUTPUT and labelled design targets",
        "common_duty_velocity_m_s": velocity,
        "payload_mass_kg": payload_mass,
        "candidates": candidates,
        "limits": [
            "This isolates moving-mass burden and does not compare motor electrical efficiency.",
            "Bolley-U has no completed mechanical or electromagnetic design.",
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

