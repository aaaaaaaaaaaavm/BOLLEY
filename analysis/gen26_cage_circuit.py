"""Bolley A7b: run Quintweb through the common post-field cage/circuit engine."""

from __future__ import annotations

import gen25_cage_circuit as engine
from common import RESULTS, ROOT


engine.FIELD_PARAMETERS = ROOT / "cad" / "gen26_field_parameters.json"
engine.FIELD_RESULT = RESULTS / "gen26_field.json"
engine.INPUT = ROOT / "cad" / "gen26_cage_parameters.json"
engine.OUTPUT = RESULTS / "gen26_cage_circuit.json"
engine.POINTS_OUTPUT = RESULTS / "gen26_cage_circuit_points.csv.gz"
engine.GATE_LABEL = "A7b"
engine.DESIGN_LABEL = "Gen2.6 Quintweb"
engine.PROMOTE_DISPOSITION = "PROMOTE_GEN26_QUINTWEB_TO_GEN3_CAD_AND_TRANSIENT_FORCE_MODEL"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_GEN26_QUINTWEB_CAGE_CIRCUIT_POINT"


if __name__ == "__main__":
    engine.main()
