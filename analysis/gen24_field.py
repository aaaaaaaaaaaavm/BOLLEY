"""Bolley A6e: run Gen2.4 Fluxrib through the common field engine."""

from __future__ import annotations

import gen2_field as engine
from common import RESULTS, ROOT


engine.INPUT = ROOT / "cad" / "gen24_field_parameters.json"
engine.OUTPUT = RESULTS / "gen24_field.json"
engine.FIGURE_DIR = ROOT / "analysis" / "figures" / "a6e"
engine.FIGURE_MANIFEST = engine.FIGURE_DIR / "FIGURES.json"
engine.GATE_LABEL = "A6e"
engine.DESIGN_LABEL = "Gen2.4 Fluxrib"
engine.FIGURE_PREFIX = "A6e"
engine.PROMOTE_DISPOSITION = "PROMOTE_GEN24_TO_CIRCUIT_CAD_AND_TRANSIENT_FORCE_CLOSURE"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_GEN24_FLUXRIB"


if __name__ == "__main__":
    engine.main()
