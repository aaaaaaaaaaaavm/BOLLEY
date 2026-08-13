"""Bolley A3b1: flux-conservation bound for the A5b shared-pole stator sketch.

This is a topology kill test, not FEA. It asks whether the narrow stationary webs can turn the
gap flux into a conventional shared back yoke without exceeding the declared pole field. The
bands in validation/A3b1_stator_throat_bound.md precede the first recorded output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import RESULTS, ROOT, compare_json, dump_json
from edge_force_bound import ideal_force_n


GEOMETRY_INPUT = ROOT / "cad" / "quad_comb_parameters.json"
TOPOLOGY_INPUT = ROOT / "cad" / "stator_throat_parameters.json"
FORCE_INPUT = RESULTS / "quad_comb_screen.json"
OUTPUT = RESULTS / "stator_throat_bound.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def calculate() -> dict:
    geometry = load(GEOMETRY_INPUT)
    topology = load(TOPOLOGY_INPUT)
    force_result = load(FORCE_INPUT)
    interface = geometry["interface"]
    comb = geometry["quad_comb"]
    shared = topology["shared_pole_array"]
    material = topology["material_anchor"]
    limits = topology["bands"]

    required_gap_field = force_result["ideal_edge_force_bound"]["required_ideal_flux_density_t"]
    fin_height = comb["active_fin_height_m"]
    throat_width = comb["stationary_pole_web_width_m"]
    preferred_pole_field = material["preferred_pole_flux_density_t"]
    hard_pole_field = material["optimistic_hard_pole_flux_density_t"]

    outer_multiplier = shared["outer_pole_flux_multiplicity"]
    interior_multiplier = shared["interior_pole_flux_multiplicity"]
    outer_field = required_gap_field * fin_height * outer_multiplier / throat_width
    interior_field = required_gap_field * fin_height * interior_multiplier / throat_width

    maximum_gap_field_from_hard_interior_throat = (
        hard_pole_field * throat_width / (interior_multiplier * fin_height)
    )
    active_edges = force_result["geometry"]["active_edge_count_per_channel"]
    effective_gap = force_result["geometry"]["nominal_effective_gap_per_side_m"]
    ideal_force_at_throat_limited_field = ideal_force_n(
        maximum_gap_field_from_hard_interior_throat,
        active_edges,
        effective_gap,
        fin_height,
    )

    required_outer_width_preferred = (
        required_gap_field * fin_height * outer_multiplier / preferred_pole_field
    )
    required_interior_width_preferred = (
        required_gap_field * fin_height * interior_multiplier / preferred_pole_field
    )
    required_outer_width_hard = (
        required_gap_field * fin_height * outer_multiplier / hard_pole_field
    )
    required_interior_width_hard = (
        required_gap_field * fin_height * interior_multiplier / hard_pole_field
    )
    slot_width = force_result["geometry"]["slot_width_m"]

    def footprint(outer_width: float, interior_width: float) -> float:
        return (
            comb["fins_per_channel"] * slot_width
            + shared["outer_pole_count"] * outer_width
            + shared["interior_pole_count"] * interior_width
        )

    preferred_footprint = footprint(
        required_outer_width_preferred, required_interior_width_preferred
    )
    hard_footprint = footprint(required_outer_width_hard, required_interior_width_hard)
    usable_face_width = force_result["geometry"]["usable_face_width_between_rail_keepouts_m"]
    preferred_face_fraction = preferred_footprint / usable_face_width
    hard_face_fraction = hard_footprint / usable_face_width

    bands = {
        "outer_throat_preferred_field": outer_field <= preferred_pole_field,
        "outer_throat_hard_field": outer_field <= hard_pole_field,
        "interior_throat_preferred_field": interior_field <= preferred_pole_field,
        "interior_throat_hard_field": interior_field <= hard_pole_field,
        "throat_limited_ideal_force": (
            ideal_force_at_throat_limited_field >= limits["minimum_average_channel_force_n"]
        ),
        "preferred_resized_footprint": (
            preferred_face_fraction <= limits["maximum_projected_usable_face_fraction"]
        ),
        "hard_resized_footprint": (
            hard_face_fraction <= limits["maximum_projected_usable_face_fraction"]
        ),
    }

    return {
        "evidence": "ANALYTICAL FLUX-CONSERVATION UPPER BOUND from ASSUMPTION topology with named EXTERNAL MATERIAL ANCHOR",
        "geometry_input_file": "cad/quad_comb_parameters.json",
        "topology_input_file": "cad/stator_throat_parameters.json",
        "force_input_file": "analysis/results/quad_comb_screen.json",
        "topology": "five shared alternating-polarity pole webs turning into one radial back yoke",
        "geometry": {
            "fin_count": comb["fins_per_channel"],
            "fin_height_m": fin_height,
            "slot_width_m": slot_width,
            "drawn_pole_throat_width_m": throat_width,
            "outer_pole_count": shared["outer_pole_count"],
            "interior_pole_count": shared["interior_pole_count"],
            "outer_flux_multiplicity": outer_multiplier,
            "interior_flux_multiplicity": interior_multiplier,
        },
        "flux_bound": {
            "required_ideal_gap_flux_density_t": required_gap_field,
            "required_outer_throat_flux_density_t": outer_field,
            "required_interior_throat_flux_density_t": interior_field,
            "maximum_gap_flux_density_from_hard_interior_throat_t": (
                maximum_gap_field_from_hard_interior_throat
            ),
            "ideal_force_at_throat_limited_gap_field_n": ideal_force_at_throat_limited_field,
        },
        "resized_shared_pole_array": {
            "required_outer_width_at_preferred_field_m": required_outer_width_preferred,
            "required_interior_width_at_preferred_field_m": required_interior_width_preferred,
            "footprint_at_preferred_field_m": preferred_footprint,
            "usable_face_fraction_at_preferred_field": preferred_face_fraction,
            "required_outer_width_at_hard_field_m": required_outer_width_hard,
            "required_interior_width_at_hard_field_m": required_interior_width_hard,
            "footprint_at_hard_field_m": hard_footprint,
            "usable_face_fraction_at_hard_field": hard_face_fraction,
        },
        "material_anchor": material,
        "bands": bands,
        "band_pass_count": sum(bands.values()),
        "band_count": len(bands),
        "screen_pass": all(bands.values()),
        "disposition": (
            "SHARED_POLE_QUAD_COMB_EARNS_NONLINEAR_FEA"
            if all(bands.values())
            else "REJECT_SHARED_POLE_QUAD_COMB_STATOR"
        ),
        "limits": [
            "Flux is assumed uniform and leakage-free; a real field solution can only worsen local peaks.",
            "The bound applies to a conventional shared radial back yoke, not every imaginable stator topology.",
            "No winding, voltage, current, thermal or force-ripple result is present.",
            "A failed shared stator rejects that stator topology; it does not erase the A5b moving-interface result.",
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
