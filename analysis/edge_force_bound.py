"""Bolley A3b0: ideal energy-gradient upper bound for the A5a comb-fin.

This is deliberately simpler than FEA. It asks whether the frozen three-fin geometry can meet
the A3 force gate even when steel reluctance, leakage, fringing, end effects and current limits
are all ignored. The bands in validation/A3b0_edge_force_bound.md precede the first output.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json


GEOMETRY_INPUT = ROOT / "cad" / "comb_fin_parameters.json"
BOUND_INPUT = ROOT / "cad" / "edge_force_bound_parameters.json"
OUTPUT = RESULTS / "edge_force_bound.json"
MU_0_H_PER_M = 4.0 * math.pi * 1e-7


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def ideal_force_n(
    flux_density_t: float,
    edge_count: int,
    effective_gap_per_side_m: float,
    active_fin_height_m: float,
) -> float:
    """Return the gap-dominated upper-bound force for active overlap edges.

    For two equal gaps in series, L=N^2*mu0*A/(2*g). With A=h*x and
    B=mu0*N*i/(2*g), 0.5*i^2*dL/dx becomes B^2*g*h/mu0 per active edge.
    """

    return (
        edge_count
        * flux_density_t**2
        * effective_gap_per_side_m
        * active_fin_height_m
        / MU_0_H_PER_M
    )


def calculate() -> dict:
    geometry = load(GEOMETRY_INPUT)
    bound = load(BOUND_INPUT)
    interface = geometry["interface"]
    comb = geometry["comb_fin"]
    model = bound["model"]
    limits = bound["bands"]

    tooth_count_float = interface["active_length_m"] / comb["pole_pitch_m"]
    tooth_count = round(tooth_count_float)
    if not math.isclose(tooth_count_float, tooth_count, abs_tol=1e-12):
        raise ValueError("active length must contain an integer number of pole pitches")

    edge_count = (
        comb["fins_per_channel"]
        * tooth_count
        * model["active_overlap_edges_per_tooth_and_fin"]
    )
    effective_gap = comb["side_cover_per_side_m"] + comb["clearance_per_side_m"]
    coefficient = ideal_force_n(1.0, edge_count, effective_gap, comb["active_fin_height_m"])
    required_force = limits["minimum_average_channel_force_n"]
    required_flux_density = math.sqrt(required_force / coefficient)
    optimistic_ceiling = limits["optimistic_hard_flux_density_ceiling_t"]
    force_at_optimistic_ceiling = ideal_force_n(
        optimistic_ceiling, edge_count, effective_gap, comb["active_fin_height_m"]
    )

    sweep = []
    sweep_index = 0
    value = model["minimum_sweep_flux_density_t"]
    while value <= model["maximum_sweep_flux_density_t"] + 1e-12:
        flux_density = round(value, 10)
        sweep.append(
            {
                "flux_density_t": flux_density,
                "ideal_force_n": ideal_force_n(
                    flux_density, edge_count, effective_gap, comb["active_fin_height_m"]
                ),
            }
        )
        sweep_index += 1
        value = (
            model["minimum_sweep_flux_density_t"]
            + sweep_index * model["sweep_step_flux_density_t"]
        )

    force_per_fin_at_preferred = ideal_force_n(
        limits["preferred_maximum_required_flux_density_t"],
        tooth_count,
        effective_gap,
        comb["active_fin_height_m"],
    )
    force_per_fin_at_hard = ideal_force_n(
        optimistic_ceiling, tooth_count, effective_gap, comb["active_fin_height_m"]
    )
    minimum_fins_at_preferred = math.ceil(required_force / force_per_fin_at_preferred)
    minimum_fins_at_hard = math.ceil(required_force / force_per_fin_at_hard)

    bands = {
        "force_at_optimistic_hard_ceiling": force_at_optimistic_ceiling >= required_force,
        "required_flux_density_preferred": (
            required_flux_density <= limits["preferred_maximum_required_flux_density_t"]
        ),
        "required_flux_density_hard": required_flux_density <= optimistic_ceiling,
    }
    hard_pass = bands["force_at_optimistic_hard_ceiling"] and bands[
        "required_flux_density_hard"
    ]

    return {
        "evidence": "ANALYTICAL UPPER BOUND from ASSUMPTION geometry with named EXTERNAL MATERIAL ANCHOR",
        "geometry_input_file": "cad/comb_fin_parameters.json",
        "bound_input_file": "cad/edge_force_bound_parameters.json",
        "topology": "two-gap through-flux switched-reluctance overlap comb",
        "derivation": {
            "inductance": "L = N^2 * mu0 * A / (2 * g)",
            "force": "F = 0.5 * i^2 * dL/dx",
            "substitution": "F_per_edge = B^2 * g * h / mu0",
            "warning": "This is an optimistic upper bound, not Maxwell-stress FEA or hardware evidence.",
        },
        "geometry": {
            "fins_per_channel": comb["fins_per_channel"],
            "active_tooth_count_per_fin": tooth_count,
            "simultaneously_active_overlap_edge_count": edge_count,
            "active_fin_height_m": comb["active_fin_height_m"],
            "side_cover_m": comb["side_cover_per_side_m"],
            "mechanical_clearance_m": comb["clearance_per_side_m"],
            "effective_gap_per_side_m": effective_gap,
        },
        "force_bound": {
            "coefficient_n_per_t2": coefficient,
            "required_average_channel_force_n": required_force,
            "required_ideal_flux_density_t": required_flux_density,
            "optimistic_hard_flux_density_ceiling_t": optimistic_ceiling,
            "ideal_force_at_optimistic_hard_ceiling_n": force_at_optimistic_ceiling,
            "minimum_fins_at_preferred_field": minimum_fins_at_preferred,
            "minimum_fins_at_hard_ceiling": minimum_fins_at_hard,
            "sweep": sweep,
        },
        "material_anchor": bound["material_anchor"],
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "hard_screen_pass": hard_pass,
        "disposition": (
            "THREE_FIN_COMB_EARNS_NONLINEAR_MODEL"
            if hard_pass
            else "REJECT_THREE_FIN_COMB_BEFORE_FEA"
        ),
        "limits": [
            "All active edges are assumed to reach the stated flux density simultaneously.",
            "Steel reluctance, saturation shape, leakage, fringing and end effects are ignored.",
            "No ampere-turn, copper-window, voltage, current, switching, loss or thermal limit is applied.",
            "The 2.0 T ceiling is deliberately optimistic and is not a supplier guarantee.",
            "A passing upper bound would only earn a nonlinear 3D model; a failure rejects the geometry.",
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
