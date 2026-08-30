"""Bolley A9e: lower-bound hardware count for two sectional selector realizations."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "analysis" / "selector_realization_parameters.json"
OUTPUT = RESULTS / "selector_realization_screen.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load(INPUT)
    f = p["fixed"]
    selector = p["series_selector_device"]
    local = p["local_bridge_module"]
    current_loss_factor_j_per_ohm = (
        f["phases_per_face"]
        * f["reference_sum_face_channel_current_squared_a2"]
        * f["shot_time_s"]
    )
    total_electronics_budget = (
        f["maximum_reference_source_energy_j"]
        - f["reference_noninverter_machine_energy_j"]
    )

    shared_records = []
    fixed_series_r_numerator = (
        f["active_cells_per_phase"]
        * selector["bidirectional_banks_per_cell_position"]
        * selector["rds_on_max_ohm_at_10v_25c"]
    )
    for bridge in p["passing_a9d_shared_bridge_candidates"]:
        remaining = bridge["reference_remaining_loss_budget_j"]
        maximum_added_path_r = remaining / current_loss_factor_j_per_ohm
        minimum_parallel_per_bank = math.ceil(fixed_series_r_numerator / maximum_added_path_r)
        realized_path_r = fixed_series_r_numerator / minimum_parallel_per_bank
        realized_loss = realized_path_r * current_loss_factor_j_per_ohm
        selector_device_count = (
            f["installed_cell_positions"]
            * selector["bidirectional_banks_per_cell_position"]
            * minimum_parallel_per_bank
        )
        shared_records.append(
            {
                "bridge_candidate": bridge["id"],
                "bridge_remaining_reference_loss_budget_j": remaining,
                "maximum_total_selector_phase_path_resistance_ohm": maximum_added_path_r,
                "minimum_parallel_mosfets_per_bidirectional_bank": minimum_parallel_per_bank,
                "realized_selector_phase_path_resistance_ohm_lower_bound": realized_path_r,
                "realized_selector_conduction_loss_j_lower_bound": realized_loss,
                "installed_selector_mosfet_count_lower_bound": selector_device_count,
                "energy_fit": realized_loss <= remaining,
            }
        )

    n_local = 1
    while True:
        local_path_r = (
            f["active_abc_modules_per_face"]
            * local["combined_half_bridge_effective_phase_path_ohm_25c"]
            / n_local
        )
        local_loss = local_path_r * current_loss_factor_j_per_ohm
        if local_loss <= total_electronics_budget:
            break
        n_local += 1
    installed_local_modules = f["installed_abc_modules"] * f["phases_per_face"] * n_local
    active_local_bridges = f["face_channels"] * f["active_abc_modules_per_face"]
    active_local_modules = active_local_bridges * f["phases_per_face"] * n_local
    local_record = {
        "minimum_parallel_onsemi_modules_per_phase_per_local_bridge": n_local,
        "effective_three_active_module_phase_path_resistance_ohm": local_path_r,
        "reference_local_bridge_conduction_loss_j": local_loss,
        "reference_source_energy_with_local_bridge_conduction_j": f["reference_noninverter_machine_energy_j"] + local_loss,
        "reference_energy_left_for_switching_bus_and_gate_drive_j": total_electronics_budget - local_loss,
        "installed_local_three_phase_bridges": f["installed_abc_modules"],
        "active_local_three_phase_bridges_during_shot": active_local_bridges,
        "installed_onsemi_module_count_lower_bound": installed_local_modules,
        "active_onsemi_module_count_during_shot": active_local_modules,
        "module_only_installed_mass_kg": installed_local_modules * local["module_mass_kg"],
        "energy_fit": local_loss <= total_electronics_budget,
    }

    checks = {
        "all_shared_selector_solutions_fit_by_construction": all(r["energy_fit"] for r in shared_records),
        "local_bridge_solution_fits_by_construction": local_record["energy_fit"],
        "positive_total_electronics_budget": total_electronics_budget > 0.0,
    }
    return {
        "evidence": "A9e SECTIONAL-SELECTOR TOPOLOGY AND 25 C SUPPLIER-CONDUCTION LOWER BOUND",
        "input_file": str(INPUT.relative_to(ROOT)),
        "current_loss_factor_j_per_ohm": current_loss_factor_j_per_ohm,
        "reference_total_electronics_loss_budget_j": total_electronics_budget,
        "shared_bridge_plus_series_selector": {
            "supplier_device": selector["name"],
            "records": shared_records,
            "interpretation": "The count is the minimum installed MOSFET count for the selector alone under ideal sharing and 25 C Rds(on). Main-bridge devices are additional."
        },
        "local_bridge_per_abc_module": {
            "supplier_module": local["name"],
            **local_record,
            "interpretation": "The module mass is power modules only. Gate drives, PCB/bus, local capacitors, cooling and control are additional."
        },
        "checks": checks,
        "check_pass_count": sum(checks.values()),
        "check_count": len(checks),
        "screen_pass": all(checks.values()),
        "disposition": "A9E_NO_SELECTOR_PROMOTED_SECTIONAL_PARTITION_REQUIRES_REDESIGN",
        "limits": [
            "No part-count or mass pass band exists in this run; counts are outputs, not reasons silently converted into thresholds.",
            "The shared-selector lower bound assumes three selected cell switches in series per phase and ideal current sharing in every parallel bank.",
            "The local-bridge lower bound duplicates a complete three-phase bridge at every ABC module and counts only supplier module mass.",
            "Switching loss, hot Rds(on), selector commutation, gate drive, busbar, capacitor, cable, cooling and package fit remain absent."
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
