"""Bolley A9d: supplier-backed 25 C bridge-conduction lower-bound screen."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "analysis" / "supplier_bridge_parameters.json"
OUTPUT = RESULTS / "supplier_bridge_screen.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def shot_time(p: dict) -> float:
    m = p["model_inputs"]
    acceleration = m["acceleration_g"] * m["gravity_m_s2"]
    return math.sqrt(2.0 * acceleration * m["powered_travel_m"]) / acceleration


def conduction_energy(sum_i2: float, path_resistance_ohm: float, duration_s: float, phases: int) -> float:
    return phases * path_resistance_ohm * sum_i2 * duration_s


def calculate() -> dict:
    p = load(INPUT)
    m = p["model_inputs"]
    bands = p["bands"]
    suppliers = p["supplier_candidates"]
    duration = shot_time(p)
    eta = m["inverter_efficiency_assumed_by_a7c_a9"]
    reference_noninverter = m["reference_source_energy_j"] * eta
    qualification_noninverter = m["qualification_source_energy_j"] * eta
    reference_electronics_budget = bands["maximum_reference_source_energy_j"] - reference_noninverter
    qualification_electronics_budget = bands["maximum_qualification_source_energy_j"] - qualification_noninverter
    phases = m["phases_per_face"]
    imax = m["maximum_failed_cell_phase_current_a"]

    onsemi = suppliers["onsemi_nxv08h400xt1"]
    onsemi_records = []
    for n in onsemi["parallel_modules_per_phase_candidates"]:
        path_r = (
            onsemi["rds_module_high_path_max_ohm_at_25c_160a"]
            + onsemi["rds_module_low_path_max_ohm_at_25c_160a"]
        ) / (4.0 * n)
        current_per_characterized_path = imax / (2.0 * n)
        ref_loss = conduction_energy(
            m["reference_sum_face_channel_current_squared_a2"], path_r, duration, phases
        )
        qual_loss = conduction_energy(
            m["qualification_sum_face_channel_current_squared_a2"], path_r, duration, phases
        )
        ref_total = reference_noninverter + ref_loss
        qual_total = qualification_noninverter + qual_loss
        module_count = m["face_channels"] * phases * n
        checks = {
            "voltage_rating": onsemi["voltage_rating_v"] >= bands["nominal_bus_voltage_v"],
            "resistance_datum_current": current_per_characterized_path <= onsemi["rds_characterization_current_a"],
            "reference_energy": ref_total <= bands["maximum_reference_source_energy_j"],
            "qualification_energy": qual_total <= bands["maximum_qualification_source_energy_j"],
        }
        onsemi_records.append(
            {
                "parallel_modules_per_phase": n,
                "effective_phase_path_resistance_ohm_25c_lower_bound": path_r,
                "maximum_failed_cell_current_per_characterized_path_a": current_per_characterized_path,
                "reference_bridge_conduction_loss_j": ref_loss,
                "qualification_bridge_conduction_loss_j": qual_loss,
                "reference_source_energy_with_bridge_conduction_j": ref_total,
                "qualification_source_energy_with_bridge_conduction_j": qual_total,
                "reference_energy_left_for_all_omitted_electrical_losses_j": bands["maximum_reference_source_energy_j"] - ref_total,
                "qualification_energy_left_for_all_omitted_electrical_losses_j": bands["maximum_qualification_source_energy_j"] - qual_total,
                "module_count": module_count,
                "module_only_mass_kg": module_count * onsemi["module_mass_kg"],
                "supplier_400a_48v_switching_characterization_covers_fault_ceiling": (
                    onsemi["switching_characterization_voltage_v"] >= bands["nominal_bus_voltage_v"]
                    and onsemi["switching_characterization_current_a"] >= imax
                ),
                "checks": checks,
                "pass": all(checks.values()),
            }
        )

    infineon = suppliers["infineon_ipt015n10n5"]
    infineon_records = []
    for n in infineon["parallel_devices_per_switch_candidates"]:
        path_r = infineon["rds_on_max_ohm_at_10v_25c"] / n
        current_per_device = imax / n
        ref_loss = conduction_energy(
            m["reference_sum_face_channel_current_squared_a2"], path_r, duration, phases
        )
        qual_loss = conduction_energy(
            m["qualification_sum_face_channel_current_squared_a2"], path_r, duration, phases
        )
        ref_total = reference_noninverter + ref_loss
        qual_total = qualification_noninverter + qual_loss
        checks = {
            "voltage_rating": infineon["voltage_rating_v"] >= bands["nominal_bus_voltage_v"],
            "continuous_current_datum": current_per_device <= infineon["continuous_current_max_a_at_25c"],
            "reference_energy": ref_total <= bands["maximum_reference_source_energy_j"],
            "qualification_energy": qual_total <= bands["maximum_qualification_source_energy_j"],
        }
        infineon_records.append(
            {
                "parallel_devices_per_switch": n,
                "effective_phase_path_resistance_ohm_25c_lower_bound": path_r,
                "maximum_failed_cell_current_per_device_a": current_per_device,
                "reference_bridge_conduction_loss_j": ref_loss,
                "qualification_bridge_conduction_loss_j": qual_loss,
                "reference_source_energy_with_bridge_conduction_j": ref_total,
                "qualification_source_energy_with_bridge_conduction_j": qual_total,
                "reference_energy_left_for_all_omitted_electrical_losses_j": bands["maximum_reference_source_energy_j"] - ref_total,
                "qualification_energy_left_for_all_omitted_electrical_losses_j": bands["maximum_qualification_source_energy_j"] - qual_total,
                "discrete_device_count_for_four_three_phase_bridges": m["face_channels"] * 6 * n,
                "supplier_25c_continuous_current_covers_per_device_fault_share": current_per_device <= infineon["continuous_current_max_a_at_25c"],
                "supplier_pulse_current_covers_per_device_fault_share": current_per_device <= infineon["pulse_current_max_a"],
                "checks": checks,
                "pass": all(checks.values()),
            }
        )

    onsemi_pass = [record for record in onsemi_records if record["pass"]]
    infineon_pass = [record for record in infineon_records if record["pass"]]
    return {
        "evidence": "A9d SUPPLIER-DATASHEET 25 C BRIDGE-CONDUCTION LOWER BOUND",
        "input_file": str(INPUT.relative_to(ROOT)),
        "shot_time_s": duration,
        "reference_noninverter_machine_energy_j": reference_noninverter,
        "qualification_noninverter_machine_energy_j": qualification_noninverter,
        "reference_total_real_electronics_loss_budget_j": reference_electronics_budget,
        "qualification_total_real_electronics_loss_budget_j": qualification_electronics_budget,
        "onsemi": {
            "source_url": onsemi["source_url"],
            "candidates": onsemi_records,
            "minimum_passing_parallel_modules_per_phase": min((r["parallel_modules_per_phase"] for r in onsemi_pass), default=None),
            "passing_candidate_count": len(onsemi_pass),
        },
        "infineon": {
            "source_url": infineon["source_url"],
            "candidates": infineon_records,
            "minimum_passing_parallel_devices_per_switch": min((r["parallel_devices_per_switch"] for r in infineon_pass), default=None),
            "passing_candidate_count": len(infineon_pass),
        },
        "screen_pass": bool(onsemi_pass or infineon_pass),
        "disposition": "A9D_LOWER_BOUND_SURVIVES_P11_P39_P40_REMAIN_OPEN" if (onsemi_pass or infineon_pass) else "A9D_BRIDGE_LOWER_BOUND_REJECTS_FLUXRELAY_PULSE_CHAIN",
        "limits": [
            "The onsemi path assumes ideal sharing across the supplier-described combined half bridge and across parallel modules.",
            "The Infineon path assumes ideal sharing across parallel discrete MOSFETs and omits package/bus resistance.",
            "Both paths use 25 C resistance data. Hot semiconductor resistance is absent.",
            "Switching, selector, gate-drive, capacitor ESR, busbar, cable, connector, source impedance and cooling losses are absent.",
            "A passing lower bound cannot close P11, P39 or P40."
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
