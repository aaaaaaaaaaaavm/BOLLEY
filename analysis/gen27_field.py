"""Bolley A6h: run the selected Gen2.7 Fluxrelay point through the field engine."""

from __future__ import annotations

import gen2_field as engine
from common import RESULTS, ROOT


engine.INPUT = ROOT / "cad" / "gen27_field_parameters.json"
engine.OUTPUT = RESULTS / "gen27_field.json"
engine.FIGURE_DIR = ROOT / "analysis" / "figures" / "a6h"
engine.FIGURE_MANIFEST = engine.FIGURE_DIR / "FIGURES.json"
engine.GATE_LABEL = "A6h"
engine.DESIGN_LABEL = "Gen2.7 Fluxrelay n27_p45.3_I380_A10.4"
engine.FIGURE_PREFIX = "A6h"
engine.PROMOTE_DISPOSITION = "PROMOTE_SELECTED_GEN27_FLUXRELAY_TO_A7C_AND_GEN3_CAD"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_SELECTED_GEN27_FLUXRELAY_FIELD_POINT"


if __name__ == "__main__":
    engine.main()
