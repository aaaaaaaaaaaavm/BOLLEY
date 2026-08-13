"""Bolley A6c: run Gen2.2 Fluxmanifold-R4 through the common field engine."""

from __future__ import annotations

import gen2_field as engine
from common import RESULTS, ROOT


engine.INPUT = ROOT / "cad" / "gen22_field_parameters.json"
engine.OUTPUT = RESULTS / "gen22_field.json"
engine.FIGURE_DIR = ROOT / "analysis" / "figures" / "a6c"
engine.FIGURE_MANIFEST = engine.FIGURE_DIR / "FIGURES.json"
engine.GATE_LABEL = "A6c"
engine.DESIGN_LABEL = "Gen2.2 Fluxmanifold-R4"
engine.FIGURE_PREFIX = "A6c"
engine.PROMOTE_DISPOSITION = "PROMOTE_GEN22_TO_CIRCUIT_CAD_AND_TRANSIENT_FORCE_CLOSURE"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_GEN22_FLUXMANIFOLD_R4"


if __name__ == "__main__":
    engine.main()
