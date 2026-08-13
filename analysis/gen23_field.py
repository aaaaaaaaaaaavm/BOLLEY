"""Bolley A6d: run Gen2.3 Fluxrib through the common field engine."""

from __future__ import annotations

import gen2_field as engine
from common import RESULTS, ROOT


engine.INPUT = ROOT / "cad" / "gen23_field_parameters.json"
engine.OUTPUT = RESULTS / "gen23_field.json"
engine.FIGURE_DIR = ROOT / "analysis" / "figures" / "a6d"
engine.FIGURE_MANIFEST = engine.FIGURE_DIR / "FIGURES.json"
engine.GATE_LABEL = "A6d"
engine.DESIGN_LABEL = "Gen2.3 Fluxrib"
engine.FIGURE_PREFIX = "A6d"
engine.PROMOTE_DISPOSITION = "PROMOTE_GEN23_FLUXRIB_TO_CIRCUIT_CAD_AND_TRANSIENT_FORCE_CLOSURE"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_GEN23_FLUXRIB"


if __name__ == "__main__":
    engine.main()
