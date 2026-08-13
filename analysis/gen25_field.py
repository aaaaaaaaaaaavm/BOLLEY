"""Bolley A6f: run Gen2.5 Fluxweb through the common field engine."""

from __future__ import annotations

import gen2_field as engine
from common import RESULTS, ROOT


engine.INPUT = ROOT / "cad" / "gen25_field_parameters.json"
engine.OUTPUT = RESULTS / "gen25_field.json"
engine.FIGURE_DIR = ROOT / "analysis" / "figures" / "a6f"
engine.FIGURE_MANIFEST = engine.FIGURE_DIR / "FIGURES.json"
engine.GATE_LABEL = "A6f"
engine.DESIGN_LABEL = "Gen2.5 Fluxweb"
engine.FIGURE_PREFIX = "A6f"
engine.PROMOTE_DISPOSITION = "PROMOTE_GEN25_FLUXWEB_TO_CAGE_CIRCUIT_CAD_AND_TRANSIENT_FORCE_CLOSURE"
engine.REJECT_DISPOSITION = "DO_NOT_PROMOTE_GEN25_FLUXWEB"


if __name__ == "__main__":
    engine.main()
