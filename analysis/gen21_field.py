"""Bolley A6b: run the Gen2.1 Fluxmanifold through the A6 field engine."""

from __future__ import annotations

import gen2_field as engine
from common import RESULTS, ROOT


engine.INPUT = ROOT / "cad" / "gen21_field_parameters.json"
engine.OUTPUT = RESULTS / "gen21_field.json"
engine.FIGURE_DIR = ROOT / "analysis" / "figures" / "a6b"
engine.FIGURE_MANIFEST = engine.FIGURE_DIR / "FIGURES.json"
engine.GATE_LABEL = "A6b"
engine.DESIGN_LABEL = "Gen2.1 Fluxmanifold"
engine.FIGURE_PREFIX = "A6b"
engine.PROMOTE_DISPOSITION = "PROMOTE_GEN21_FLUXMANIFOLD_TO_CIRCUIT_AND_CAD_CLOSURE"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_GEN21_FLUXMANIFOLD"


if __name__ == "__main__":
    engine.main()
