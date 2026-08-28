"""Bolley A12: sourced public chassis-mass envelope for Gen5 Fluxframe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "analysis" / "fluxframe_mass_parameters.json"
OUTPUT = RESULTS / "fluxframe_mass.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load(INPUT)
    required_credit = p["fluxrelay_interface_mass_kg"] - p["net_mass_preference_kg"]
    records = []
    for item in p["structure_comparators"]:
        records.append(
            {
                **item,
                "required_replacement_fraction": required_credit / item["mass_kg"],
                "hypothetical_full_replacement_net_added_mass_kg": p[
                    "fluxrelay_interface_mass_kg"
                ]
                - item["mass_kg"],
                "credit_granted_kg": 0.0,
            }
        )

    maximum_fraction = max(row["required_replacement_fraction"] for row in records)
    maximum_full_replacement_net = max(
        row["hypothetical_full_replacement_net_added_mass_kg"] for row in records
    )
    labels_preserved = any(
        row["mass_semantics"] == "PUBLISHED_UPPER_BOUND" for row in records
    ) and all(row["mass_semantics"] for row in records)
    checks = [
        {
            "id": 1,
            "name": "required credit below every public mass comparator",
            "value": required_credit,
            "limit": min(row["mass_kg"] for row in records),
            "status": "PASS"
            if required_credit < min(row["mass_kg"] for row in records)
            else "FAIL",
        },
        {
            "id": 2,
            "name": "maximum required replacement fraction",
            "value": maximum_fraction,
            "limit": p["maximum_required_replacement_fraction"],
            "status": "PASS"
            if maximum_fraction <= p["maximum_required_replacement_fraction"]
            else "FAIL",
        },
        {
            "id": 3,
            "name": "worst hypothetical full-replacement net addition",
            "value": maximum_full_replacement_net,
            "limit": p["net_mass_preference_kg"],
            "status": "PASS"
            if maximum_full_replacement_net <= p["net_mass_preference_kg"]
            else "FAIL",
        },
        {
            "id": 4,
            "name": "current gross interface below absolute limit",
            "value": p["fluxrelay_interface_mass_kg"],
            "limit": p["gross_mass_absolute_kg"],
            "status": "PASS"
            if p["fluxrelay_interface_mass_kg"] <= p["gross_mass_absolute_kg"]
            else "FAIL",
        },
        {
            "id": 5,
            "name": "source mass semantics preserved",
            "value": labels_preserved,
            "limit": True,
            "status": "PASS" if labels_preserved else "FAIL",
        },
        {
            "id": 6,
            "name": "bus-specific removed-part credit",
            "value": None,
            "limit": "SELECTED_BUS_LEDGER_REQUIRED",
            "status": "OPEN",
        },
        {
            "id": 7,
            "name": "structural thermal electrical and magnetic equivalence",
            "value": None,
            "limit": "COUPLED_MODEL_AND_TEST_REQUIRED",
            "status": "OPEN",
        },
        {
            "id": 8,
            "name": "rail and provider compatibility",
            "value": None,
            "limit": "DRAWING_REVIEW_AND_PROVIDER_DISPOSITION_REQUIRED",
            "status": "OPEN",
        },
    ]
    return {
        "schema": "bolley.fluxframe-mass.result/1",
        "evidence_class": "SOURCED_PUBLIC_MASS_ENVELOPE",
        "controlled_input": str(INPUT.relative_to(ROOT)),
        "required_displaced_mass_kg": required_credit,
        "comparators": records,
        "checks": checks,
        "pass_count": sum(check["status"] == "PASS" for check in checks),
        "open_count": sum(check["status"] == "OPEN" for check in checks),
        "disposition": "PROMOTE_TO_SELECTED_BUS_LEDGER_NOT_NET_MASS_CLOSURE",
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
