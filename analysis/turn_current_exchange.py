"""Bolley A9f: trade unused DC-link voltage for lower sectional-drive current."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


INPUT = ROOT / "analysis" / "turn_current_exchange_parameters.json"
OUTPUT = RESULTS / "turn_current_exchange.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    p = load(INPUT)
    b = p["baseline"]
    s = p["search"]
    module = p["supplier_module"]
    bands = p["bands"]
    candidates = []

    healthy_voltage_limit_with_margin = (
        bands["nominal_dc_link_v"]
        / (1.0 + bands["minimum_healthy_dc_link_margin_fraction"])
    )

    for turns in s["turns_per_cell"]:
        scale = turns / b["turns_per_cell"]
        rated_current = b["rated_phase_current_a"] / scale
        failed_current = b["maximum_failed_cell_phase_current_a"] / scale
        conductor_area = b["conductor_area_per_turn_mm2"] / scale
        phase_resistance = b["phase_resistance_nominal_ohm"] * scale**2
        phase_inductance = b["active_window_phase_inductance_h"] * scale**2
        healthy_voltage = b["maximum_healthy_required_dc_link_v"] * scale
        failed_voltage = b["maximum_failed_cell_required_dc_link_v"] * scale
        healthy_margin = bands["nominal_dc_link_v"] / healthy_voltage - 1.0
        reference_sum_i2 = b["reference_sum_face_channel_current_squared_a2"] / scale**2
        qualification_sum_i2 = b["qualification_sum_face_channel_current_squared_a2"] / scale**2

        selected_parallel = None
        electrical = None
        for parallel in range(1, s["maximum_parallel_onsemi_modules_per_phase_per_local_bridge"] + 1):
            current_per_internal_path = (
                failed_current
                / (module["internal_parallel_paths_when_combined"] * parallel)
            )
            local_phase_path_r = (
                b["active_abc_modules_per_face"]
                * module["combined_half_bridge_effective_phase_path_ohm_25c"]
                / parallel
            )
            reference_loss = (
                b["phases_per_face"]
                * local_phase_path_r
                * reference_sum_i2
                * b["shot_time_s"]
            )
            qualification_loss = (
                b["phases_per_face"]
                * local_phase_path_r
                * qualification_sum_i2
                * b["shot_time_s"]
            )
            reference_energy = b["reference_noninverter_machine_energy_j"] + reference_loss
            qualification_energy = b["qualification_noninverter_machine_energy_j"] + qualification_loss
            if (
                current_per_internal_path <= module["rds_characterization_current_a_per_internal_path"]
                and reference_energy <= bands["maximum_reference_source_energy_j"]
                and qualification_energy <= bands["maximum_qualification_source_energy_j"]
            ):
                selected_parallel = parallel
                electrical = {
                    "maximum_failed_cell_current_per_supplier_characterized_internal_path_a": current_per_internal_path,
                    "effective_three_active_module_phase_path_resistance_ohm": local_phase_path_r,
                    "reference_local_bridge_conduction_loss_j": reference_loss,
                    "qualification_local_bridge_conduction_loss_j": qualification_loss,
                    "reference_source_energy_j": reference_energy,
                    "qualification_source_energy_j": qualification_energy,
                }
                break

        installed_module_count = (
            b["installed_abc_modules"] * b["phases_per_face"] * selected_parallel
            if selected_parallel is not None
            else None
        )
        module_mass = (
            installed_module_count * module["module_mass_kg"]
            if installed_module_count is not None
            else None
        )
        checks = {
            "phase_current": rated_current <= bands["maximum_phase_current_a"],
            "healthy_dc_link_margin": healthy_margin >= bands["minimum_healthy_dc_link_margin_fraction"],
            "failed_cell_dc_link": failed_voltage <= bands["maximum_failed_cell_required_dc_link_v"],
            "supplier_module_partition_found": selected_parallel is not None,
            "reference_energy": electrical is not None and electrical["reference_source_energy_j"] <= bands["maximum_reference_source_energy_j"],
            "qualification_energy": electrical is not None and electrical["qualification_source_energy_j"] <= bands["maximum_qualification_source_energy_j"],
        }
        if electrical is not None:
            worst_demand = max(
                electrical["reference_source_energy_j"] / bands["maximum_reference_source_energy_j"],
                healthy_voltage / healthy_voltage_limit_with_margin,
                failed_voltage / bands["maximum_failed_cell_required_dc_link_v"],
                rated_current / bands["maximum_phase_current_a"],
            )
        else:
            worst_demand = math.inf
        candidates.append(
            {
                "turns_per_cell": turns,
                "turn_scale_from_a9b": scale,
                "rated_phase_current_a": rated_current,
                "failed_cell_phase_current_a": failed_current,
                "conductor_area_per_turn_mm2": conductor_area,
                "phase_resistance_nominal_ohm": phase_resistance,
                "active_window_phase_inductance_h": phase_inductance,
                "healthy_required_dc_link_v_scaled": healthy_voltage,
                "healthy_dc_link_margin_fraction": healthy_margin,
                "failed_cell_required_dc_link_v_scaled": failed_voltage,
                "minimum_parallel_modules_per_phase_per_local_bridge": selected_parallel,
                **(electrical or {}),
                "installed_onsemi_module_count": installed_module_count,
                "module_only_mass_kg": module_mass,
                "worst_selection_normalized_demand": worst_demand,
                "checks": checks,
                "pass": all(checks.values()),
            }
        )

    feasible = [candidate for candidate in candidates if candidate["pass"]]
    selected = min(
        feasible,
        key=lambda c: (
            c["module_only_mass_kg"],
            c["worst_selection_normalized_demand"],
            c["turns_per_cell"],
        ),
    ) if feasible else None

    return {
        "evidence": "A9f FIXED-MMF TURN/CURRENT EXCHANGE WITH 25 C SUPPLIER LOCAL-BRIDGE CONDUCTION",
        "input_file": str(INPUT.relative_to(ROOT)),
        "healthy_voltage_limit_with_inherited_10pct_margin_v": healthy_voltage_limit_with_margin,
        "candidate_count": len(candidates),
        "feasible_candidate_count": len(feasible),
        "candidates": candidates,
        "selected_candidate": selected,
        "screen_pass": selected is not None,
        "disposition": "A9F_SELECT_12TURN_LOCAL_BRIDGE_FOR_FRESH_FIELD_CAD_AND_SWITCHING_CLOSURE" if selected and selected["turns_per_cell"] == 12 else ("A9F_SELECT_DIFFERENT_TURN_EXCHANGE_POINT" if selected else "A9F_NO_FEASIBLE_TURN_EXCHANGE"),
        "limits": [
            "The field and force are held by fixed MMF for this screen; the selected winding requires a fresh nonlinear-field reclosure.",
            "Resistance and inductance use ideal N-squared scaling at constant total slot copper and mean turn geometry.",
            "The selected conductor area has not been routed in CAD or tied to a winding supplier tolerance.",
            "Supplier hot Rds(on), switching loss, gate drive, local DC-link parts, busbar, cooling and fault isolation remain absent.",
            "Module-only mass is not packaged electrical mass and does not close P39."
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
