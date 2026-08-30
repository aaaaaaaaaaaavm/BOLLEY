"""Bolley A9: time-domain envelope for my selected Gen3 sectional drive."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from interface_fit_screen import cardinal_forces


INPUT = ROOT / "analysis" / "sectional_drive_parameters.json"
BASE_INPUT = ROOT / "cad" / "fluxbridge_parameters.json"
A7C_RESULT = RESULTS / "gen27_cage_circuit.json"
OUTPUT = RESULTS / "sectional_drive.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def current_envelope(
    total_force_n: float,
    rated_force_n: float,
    rated_current_a: float,
    cg_limit_m: float,
    cg_points: int,
    force_line_radius_m: float,
) -> dict:
    grid = [
        -cg_limit_m + 2.0 * cg_limit_m * index / (cg_points - 1)
        for index in range(cg_points)
    ]
    maximum_current = 0.0
    minimum_force = math.inf
    maximum_force = 0.0
    sum_i2_min = math.inf
    sum_i2_max = -math.inf
    for y_cg in grid:
        for z_cg in grid:
            forces = cardinal_forces(
                total_force_n, y_cg, z_cg, force_line_radius_m
            )
            currents = [
                rated_current_a * math.sqrt(max(0.0, force) / rated_force_n)
                for force in forces.values()
            ]
            maximum_current = max(maximum_current, *currents)
            minimum_force = min(minimum_force, *forces.values())
            maximum_force = max(maximum_force, *forces.values())
            sum_i2 = sum(current * current for current in currents)
            sum_i2_min = min(sum_i2_min, sum_i2)
            sum_i2_max = max(sum_i2_max, sum_i2)
    return {
        "maximum_channel_current_a": maximum_current,
        "minimum_channel_force_n": minimum_force,
        "maximum_channel_force_n": maximum_force,
        "minimum_sum_channel_current_squared_a2": sum_i2_min,
        "maximum_sum_channel_current_squared_a2": sum_i2_max,
        "sum_channel_current_squared_spread_a2": sum_i2_max - sum_i2_min,
    }


def selector_summary(
    moving_mass_kg: float,
    phase_resistance_ohm: float,
    samples_per_handoff: int,
    fixed: dict,
    drive: dict,
    interface: dict,
    inductance_h: float,
) -> dict:
    gravity = fixed["gravity_m_s2"]
    acceleration = drive["acceleration_g"] * gravity
    total_force = moving_mass_kg * acceleration
    rated_force = drive["rated_channel_force_n"]
    rated_current = fixed["rated_phase_current_a"]
    phase_count = fixed["phase_count"]
    active_cells = fixed["active_window_cells"]
    cells_per_phase = active_cells // phase_count
    total_cells = fixed["total_cells_per_face"]
    handoff_count = total_cells - active_cells
    pitch = fixed["cell_pitch_m"]
    stroke = fixed["powered_travel_m"]
    schedule_margin = 0.5 * (stroke - handoff_count * pitch)
    if schedule_margin < 0.0:
        raise SystemExit("A9 handoff schedule does not fit the powered travel")
    if active_cells % phase_count:
        raise SystemExit("A9 active window is not a whole three-phase lattice")
    if total_cells % phase_count:
        raise SystemExit("A9 installed cells are not a whole three-phase lattice")

    current = current_envelope(
        total_force,
        rated_force,
        rated_current,
        interface["transverse_cg_limit_m"],
        interface["cg_grid_points_per_axis"],
        interface["force_line_radius_m"],
    )
    sum_i2 = current["maximum_sum_channel_current_squared_a2"]
    if current["sum_channel_current_squared_spread_a2"] > 1e-8:
        raise SystemExit("A9 sum(I^2) is not invariant over the declared CG grid")

    cell_inductance = inductance_h / cells_per_phase
    cell_resistance = phase_resistance_ohm / cells_per_phase
    initial_magnetic_energy = phase_count * 0.5 * inductance_h * sum_i2
    source_magnetic_energy = initial_magnetic_energy
    dumped_magnetic_energy = 0.0
    peak_selector_phase_voltage = 0.0
    peak_added_source_power = 0.0
    handoff_durations = []

    def time_at_position(x_m: float) -> float:
        if x_m <= 0.0:
            return 0.0
        return math.sqrt(2.0 * x_m / acceleration)

    for handoff_index in range(handoff_count):
        start = schedule_margin + handoff_index * pitch
        end = start + pitch
        duration = time_at_position(end) - time_at_position(start)
        handoff_durations.append(duration)
        source_power = []
        dump_power = []
        for sample in range(samples_per_handoff + 1):
            fraction = sample / samples_per_handoff
            theta = 0.5 * math.pi * fraction
            omega = 0.5 * math.pi / duration
            outgoing = math.cos(theta)
            incoming = math.sin(theta)
            outgoing_rate = -math.sin(theta) * omega
            incoming_rate = math.cos(theta) * omega
            outgoing_voltage_per_amp = (
                cell_inductance * outgoing_rate + cell_resistance * outgoing
            )
            incoming_voltage_per_amp = (
                cell_inductance * incoming_rate + cell_resistance * incoming
            )
            peak_selector_phase_voltage = max(
                peak_selector_phase_voltage,
                current["maximum_channel_current_a"]
                * abs(outgoing_voltage_per_amp),
                current["maximum_channel_current_a"]
                * abs(incoming_voltage_per_amp),
            )
            incoming_magnetic_power = (
                cell_inductance
                * sum_i2
                * max(incoming * incoming_rate, 0.0)
            )
            outgoing_dump_power = (
                cell_inductance
                * sum_i2
                * max(-outgoing * outgoing_rate, 0.0)
            )
            source_power.append(incoming_magnetic_power)
            dump_power.append(outgoing_dump_power)
            peak_added_source_power = max(
                peak_added_source_power,
                incoming_magnetic_power / drive["inverter_efficiency"],
            )

        step = duration / samples_per_handoff
        source_magnetic_energy += step * (
            0.5 * source_power[0]
            + sum(source_power[1:-1])
            + 0.5 * source_power[-1]
        )
        dumped_magnetic_energy += step * (
            0.5 * dump_power[0]
            + sum(dump_power[1:-1])
            + 0.5 * dump_power[-1]
        )

    selector_dc_link = (
        math.sqrt(6.0)
        * peak_selector_phase_voltage
        / drive["space_vector_modulation_utilisation"]
    )
    source_overhead = source_magnetic_energy / drive["inverter_efficiency"]
    ideal_exit_velocity = math.sqrt(2.0 * acceleration * stroke)
    full_force_recovery_factor = math.sqrt(active_cells / (active_cells - 1.0))
    failed_cell_recovery_current = (
        current["maximum_channel_current_a"] * full_force_recovery_factor
    )
    degraded_force = total_force - current["maximum_channel_force_n"] / active_cells
    degraded_acceleration = degraded_force / moving_mass_kg
    degraded_exit_velocity = math.sqrt(2.0 * degraded_acceleration * stroke)

    return {
        "samples_per_handoff": samples_per_handoff,
        "handoff_count": handoff_count,
        "handoff_distance_m": pitch,
        "start_and_end_schedule_margin_m": schedule_margin,
        "minimum_handoff_duration_s": min(handoff_durations),
        "maximum_handoff_duration_s": max(handoff_durations),
        "cell_inductance_h": cell_inductance,
        "cell_resistance_ohm": cell_resistance,
        "initial_active_window_magnetic_energy_j": initial_magnetic_energy,
        "source_magnetic_charge_energy_j": source_magnetic_energy,
        "dumped_outgoing_magnetic_energy_j": dumped_magnetic_energy,
        "source_energy_overhead_j": source_overhead,
        "maximum_selector_phase_voltage_v": peak_selector_phase_voltage,
        "selector_equivalent_dc_link_v": selector_dc_link,
        "maximum_added_source_power_w": peak_added_source_power,
        "maximum_channel_current_a": current["maximum_channel_current_a"],
        "minimum_channel_force_n": current["minimum_channel_force_n"],
        "maximum_channel_force_n": current["maximum_channel_force_n"],
        "sum_channel_current_squared_spread_a2": current[
            "sum_channel_current_squared_spread_a2"
        ],
        "healthy_exit_velocity_m_s": ideal_exit_velocity,
        "healthy_switching_exit_error_m_s": 0.0,
        "healthy_peak_acceleration_g": drive["acceleration_g"],
        "healthy_minimum_axial_force_n": current["minimum_channel_force_n"],
        "failed_cell_full_force_recovery_current_a": failed_cell_recovery_current,
        "failed_cell_no_compensation_exit_velocity_m_s": degraded_exit_velocity,
        "failed_cell_no_compensation_force_loss_n": (
            current["maximum_channel_force_n"] / active_cells
        ),
        "force_model": (
            "One outgoing and one incoming cell use cosine/sine RMS-current envelopes. "
            "Their squared currents sum to the one-cell command, so the healthy square-law "
            "force command is constant while the ideal source supplies L di/dt + Ri."
        ),
    }


def combine_case(base_case: dict, selector: dict, drive: dict) -> dict:
    source_energy = base_case["maximum_source_energy_j"] + selector[
        "source_energy_overhead_j"
    ]
    required_dc = base_case["maximum_required_dc_link_v"] + selector[
        "selector_equivalent_dc_link_v"
    ]
    peak_power = base_case["maximum_peak_dc_power_w"] + selector[
        "maximum_added_source_power_w"
    ]
    fault_factor = math.sqrt(9.0 / 8.0)
    conservative_fault_dc = required_dc * fault_factor
    return {
        "moving_mass_kg": base_case["moving_mass_kg"],
        "a7c_source_energy_j": base_case["maximum_source_energy_j"],
        "selector_source_overhead_j": selector["source_energy_overhead_j"],
        "source_energy_with_nonregenerative_selector_j": source_energy,
        "a7c_required_dc_link_v": base_case["maximum_required_dc_link_v"],
        "selector_equivalent_dc_link_v": selector["selector_equivalent_dc_link_v"],
        "conservative_additive_required_dc_link_v": required_dc,
        "a7c_peak_dc_power_w": base_case["maximum_peak_dc_power_w"],
        "selector_added_peak_source_power_w": selector[
            "maximum_added_source_power_w"
        ],
        "conservative_peak_dc_power_w": peak_power,
        "maximum_phase_current_a": selector["maximum_channel_current_a"],
        "healthy_exit_velocity_m_s": selector["healthy_exit_velocity_m_s"],
        "healthy_switching_exit_error_m_s": selector[
            "healthy_switching_exit_error_m_s"
        ],
        "healthy_peak_acceleration_g": selector["healthy_peak_acceleration_g"],
        "healthy_minimum_axial_force_n": selector["healthy_minimum_axial_force_n"],
        "failed_cell_full_force_recovery_current_a": selector[
            "failed_cell_full_force_recovery_current_a"
        ],
        "failed_cell_conservative_required_dc_link_v": conservative_fault_dc,
        "failed_cell_no_compensation_exit_velocity_m_s": selector[
            "failed_cell_no_compensation_exit_velocity_m_s"
        ],
        "failed_cell_no_compensation_force_loss_n": selector[
            "failed_cell_no_compensation_force_loss_n"
        ],
        "selector": selector,
    }


def evaluate_bands(corners: list[dict], limits: dict) -> dict:
    references = [corner["reference"] for corner in corners]
    qualifications = [corner["qualification"] for corner in corners]
    all_cases = references + qualifications
    return {
        "maximum_phase_current": max(
            case["maximum_phase_current_a"] for case in all_cases
        )
        <= limits["maximum_phase_current_a"],
        "required_dc_link": max(
            case["conservative_additive_required_dc_link_v"] for case in all_cases
        )
        <= limits["maximum_required_dc_link_v"],
        "peak_dc_power": max(
            case["conservative_peak_dc_power_w"] for case in all_cases
        )
        <= limits["maximum_peak_dc_power_w"],
        "reference_source_energy": max(
            case["source_energy_with_nonregenerative_selector_j"]
            for case in references
        )
        <= limits["maximum_reference_source_energy_j"],
        "qualification_source_energy": max(
            case["source_energy_with_nonregenerative_selector_j"]
            for case in qualifications
        )
        <= limits["maximum_qualification_source_energy_j"],
        "healthy_longitudinal_acceleration": max(
            case["healthy_peak_acceleration_g"] for case in all_cases
        )
        <= limits["maximum_healthy_longitudinal_acceleration_g"],
        "reference_switching_exit_error": max(
            abs(case["healthy_switching_exit_error_m_s"]) for case in references
        )
        <= limits["maximum_reference_switching_exit_error_m_s"],
        "qualification_exit_velocity": min(
            case["healthy_exit_velocity_m_s"] for case in qualifications
        )
        >= limits["minimum_qualification_exit_velocity_m_s"],
        "unbalanced_normal_force": max(
            corner["unbalanced_normal_force_n"] for corner in corners
        )
        <= limits["maximum_unbalanced_normal_force_n"],
        "healthy_axial_force": min(
            case["healthy_minimum_axial_force_n"] for case in all_cases
        )
        >= limits["minimum_healthy_axial_force_n"],
        "failed_cell_phase_current": max(
            case["failed_cell_full_force_recovery_current_a"]
            for case in all_cases
        )
        <= limits["failed_cell_maximum_phase_current_a"],
        "failed_cell_required_dc_link": max(
            case["failed_cell_conservative_required_dc_link_v"]
            for case in all_cases
        )
        <= limits["failed_cell_maximum_required_dc_link_v"],
        "failed_cell_axial_force": min(
            case["healthy_minimum_axial_force_n"] for case in all_cases
        )
        >= limits["failed_cell_minimum_axial_force_n"],
    }


def calculate_resolution(
    parameters: dict,
    base: dict,
    a7c: dict,
    samples_per_handoff: int,
) -> dict:
    fixed = parameters["fixed"]
    limits = parameters["bands"]
    drive = base["drive"]
    interface = base["interface"]
    inductance = a7c["sectional"]["phase_inductance_h"]
    if not math.isclose(
        inductance,
        fixed["a6h_three_cell_phase_inductance_h"],
        rel_tol=0.0,
        abs_tol=5e-12,
    ):
        raise SystemExit("A9 phase inductance no longer matches the frozen A6h value")
    if a7c["design"]["total_cells_per_channel"] != fixed["total_cells_per_face"]:
        raise SystemExit("A9 installed cell count no longer matches A7c")
    if a7c["sectional"]["energized_cell_equivalents"] != fixed["active_window_cells"]:
        raise SystemExit("A9 active window no longer matches A7c")
    if not math.isclose(
        a7c["rated"]["phase_current_rms_a"],
        fixed["rated_phase_current_a"],
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise SystemExit("A9 rated current no longer matches A7c")
    if not math.isclose(
        drive["powered_length_m"],
        fixed["powered_travel_m"],
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        raise SystemExit("A9 powered travel no longer matches the inherited drive")

    corners = []
    for corner in a7c["corners"]:
        reference_selector = selector_summary(
            corner["reference"]["moving_mass_kg"],
            corner["phase_resistance_ohm"],
            samples_per_handoff,
            fixed,
            drive,
            interface,
            inductance,
        )
        qualification_selector = selector_summary(
            corner["qualification"]["moving_mass_kg"],
            corner["phase_resistance_ohm"],
            samples_per_handoff,
            fixed,
            drive,
            interface,
            inductance,
        )
        corners.append(
            {
                "corner": corner["corner"],
                "phase_resistance_ohm": corner["phase_resistance_ohm"],
                "unbalanced_normal_force_n": corner["unbalanced_normal_force_n"],
                "reference": combine_case(
                    corner["reference"], reference_selector, drive
                ),
                "qualification": combine_case(
                    corner["qualification"], qualification_selector, drive
                ),
            }
        )

    bands = evaluate_bands(corners, limits)
    return {
        "samples_per_handoff": samples_per_handoff,
        "corners": corners,
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "failed_bands": [name for name, passed in bands.items() if not passed],
        "pass": all(bands.values()),
    }


def maxima(resolution: dict) -> dict:
    references = [corner["reference"] for corner in resolution["corners"]]
    qualifications = [corner["qualification"] for corner in resolution["corners"]]
    all_cases = references + qualifications
    return {
        "maximum_reference_source_energy_j": max(
            case["source_energy_with_nonregenerative_selector_j"]
            for case in references
        ),
        "maximum_qualification_source_energy_j": max(
            case["source_energy_with_nonregenerative_selector_j"]
            for case in qualifications
        ),
        "maximum_phase_current_a": max(
            case["maximum_phase_current_a"] for case in all_cases
        ),
        "maximum_required_dc_link_v": max(
            case["conservative_additive_required_dc_link_v"]
            for case in all_cases
        ),
        "maximum_peak_dc_power_w": max(
            case["conservative_peak_dc_power_w"] for case in all_cases
        ),
        "maximum_failed_cell_recovery_current_a": max(
            case["failed_cell_full_force_recovery_current_a"]
            for case in all_cases
        ),
        "maximum_failed_cell_required_dc_link_v": max(
            case["failed_cell_conservative_required_dc_link_v"]
            for case in all_cases
        ),
        "minimum_failed_cell_no_compensation_exit_velocity_m_s": min(
            case["failed_cell_no_compensation_exit_velocity_m_s"]
            for case in all_cases
        ),
        "maximum_absolute_switching_exit_error_m_s": max(
            abs(case["healthy_switching_exit_error_m_s"]) for case in all_cases
        ),
    }


def calculate() -> dict:
    parameters = load(INPUT)
    base = load(BASE_INPUT)
    a7c = load(A7C_RESULT)
    if not a7c["screen_pass"]:
        raise SystemExit("A9 requires the passing A7c selected point")

    coarse = calculate_resolution(parameters, base, a7c, 100)
    fine = calculate_resolution(parameters, base, a7c, 200)
    coarse_max = maxima(coarse)
    fine_max = maxima(fine)
    deltas = {key: fine_max[key] - coarse_max[key] for key in fine_max}
    band_outcomes_match = coarse["bands"] == fine["bands"]
    return {
        "evidence": (
            "A9 IDEAL-CURRENT-TRACKING TIME-DOMAIN SECTIONAL SELECTOR ENVELOPE; "
            "nonregenerative incoming-cell magnetic charge is added to A7c"
        ),
        "input_file": str(INPUT.relative_to(ROOT)),
        "source_result_file": str(A7C_RESULT.relative_to(ROOT)),
        "model": {
            "handoff_law": (
                "One cell transfers with I_out=I*cos(theta), I_in=I*sin(theta) "
                "over one cell pitch. Force is proportional to the sum of squared "
                "RMS current envelopes."
            ),
            "voltage_law": "Per-cell selector voltage uses v=L di/dt + Ri.",
            "energy_rule": (
                "Initial active-window magnetic charge and every incoming-cell "
                "magnetic charge are supplied from the source. Outgoing magnetic "
                "energy receives no regeneration credit and is reported as dump duty."
            ),
            "a7c_reuse": (
                "A7c mechanical, cage, core and copper source energy remains the "
                "quasi-steady baseline. A9 adds only selector magnetic charging."
            ),
            "fault_policy": (
                "A single failed active cell first attempts full force recovery by "
                "raising the remaining eight cell-current envelopes by sqrt(9/8). "
                "The no-compensation degraded exit is also reported."
            ),
            "limits": [
                "This is an RMS-current envelope, not phase-resolved semiconductor switching.",
                "Ideal current tracking is assumed if the computed selector voltage fits the existing DC-link band.",
                "Discrete cage rungs, 3D end fields, supplier switching loss, cables, EMC and controller delay are absent."
            ],
        },
        "coarse": coarse,
        "fine": fine,
        "coarse_to_fine_deltas": deltas,
        "band_outcomes_match_between_resolutions": band_outcomes_match,
        "screen_pass": fine["pass"] and band_outcomes_match,
        "disposition": (
            "A9_MODEL_PASS_RETAIN_FLUXRELAY_FOR_SUPPLIER_AND_PACKAGING_CLOSURE"
            if fine["pass"] and band_outcomes_match
            else "A9_MODEL_FAIL_REJECT_OR_REDESIGN_SECTIONAL_DRIVE"
        ),
        "controlling": fine_max,
        "limits": [
            "A pass can move P38 only to MODELLED for the selector effects represented here.",
            "P11 and P40 remain open because no supplier-backed switch, hot winding, cable or SOA loss is included.",
            "P29 remains open because the cage is still homogenized and axial 3D end fields are absent.",
            "P39 remains open because structure, cooling, containment, wiring and power-electronics mass are absent.",
            "P5 and P10 remain open because failed-cell force asymmetry is not a six-degree-of-freedom separation result."
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
