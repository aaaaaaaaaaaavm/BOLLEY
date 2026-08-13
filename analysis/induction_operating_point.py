"""Bolley A3d: revised 0.60 T Fluxfoil operating point after the frozen A3c efficiency miss."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from induction_screen import calculate as calculate_thin_sheet


INPUT = ROOT / "cad" / "fluxfoil_a3d_parameters.json"
OUTPUT = RESULTS / "induction_operating_point.json"


def calculate() -> dict:
    result = calculate_thin_sheet(INPUT)
    with INPUT.open(encoding="utf-8") as handle:
        p = json.load(handle)
    result["evidence"] = (
        "A3d REVISED OPERATING-POINT MODEL OUTPUT after the frozen A3c efficiency failure"
    )
    result["supersedes"] = (
        "A3c 0.50 T operating point only; A3c result and geometry remain immutable"
    )
    result["bands"]["external_field_ceiling"] = (
        p["fluxfoil"]["external_field_rms_t"]
        <= p["bands"]["maximum_external_field_rms_t"]
    )
    result["band_pass_count"] = sum(result["bands"].values())
    result["band_count"] = len(result["bands"])
    result["screen_pass"] = all(result["bands"].values())
    result["disposition"] = (
        "PROMOTE_A3D_FLUXFOIL_TO_EXPLICIT_STATOR_AND_CIRCUIT_MODEL"
        if result["screen_pass"]
        else "DO_NOT_PROMOTE_A3D_FLUXFOIL"
    )
    return result


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
