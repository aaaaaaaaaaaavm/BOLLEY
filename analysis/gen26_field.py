"""Bolley A6g: run Gen2.6 Quintweb through the common field engine."""

from __future__ import annotations

import gen2_field as engine
from common import RESULTS, ROOT


engine.INPUT = ROOT / "cad" / "gen26_field_parameters.json"
engine.OUTPUT = RESULTS / "gen26_field.json"
engine.FIGURE_DIR = ROOT / "analysis" / "figures" / "a6g"
engine.FIGURE_MANIFEST = engine.FIGURE_DIR / "FIGURES.json"
engine.GATE_LABEL = "A6g"
engine.DESIGN_LABEL = "Gen2.6 Quintweb"
engine.FIGURE_PREFIX = "A6g"
engine.PROMOTE_DISPOSITION = "PROMOTE_GEN26_QUINTWEB_TO_CAGE_CIRCUIT_AND_CAD_CLOSURE"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_GEN26_QUINTWEB"


if __name__ == "__main__":
    engine.main()
