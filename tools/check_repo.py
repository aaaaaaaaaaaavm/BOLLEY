"""Repository integrity check with a valid pre-run state."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis" / "results"
CORE_RESULTS = {
    "baseline.json",
    "force_allocation.json",
    "architecture_trade.json",
}
A3A_RESULTS = {"topology_screen.json"}
A5A_RESULTS = {"interface_fit_screen.json"}
A3B0_RESULTS = {"edge_force_bound.json"}
A5B_RESULTS = {"quad_comb_screen.json"}
A3B1_RESULTS = {"stator_throat_bound.json"}
A3C_RESULTS = {"induction_screen.json"}
A3D_RESULTS = {"induction_operating_point.json"}
A3E_RESULTS = {"stator_circuit.json"}
A5C_RESULTS = {"cad_fit.json"}
A3F_RESULTS = {"fluxbridge_cage.json"}
A3G_RESULTS = {"fluxbridge_optimization.json"}
A5D_RESULTS = {"gen2_cad_fit.json"}
A6_RESULTS = {"gen2_field.json"}
A6B_RESULTS = {"gen21_field.json"}


def run(*parts: str) -> None:
    subprocess.run([sys.executable, *parts], cwd=ROOT, check=True)


def check_links() -> None:
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for document in ROOT.rglob("*.md"):
        for target in pattern.findall(document.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (document.parent / clean).resolve()
            if not resolved.exists():
                raise SystemExit(f"broken local link in {document.relative_to(ROOT)}: {target}")


def main() -> None:
    banned = [ROOT / "paper", ROOT / "paper.tex", ROOT / "bibliography.bib"]
    present = [path.relative_to(ROOT) for path in banned if path.exists()]
    if present:
        raise SystemExit(f"paper-production paths are outside repository scope: {present}")

    for script in list((ROOT / "analysis").glob("*.py")) + list((ROOT / "tools").glob("*.py")):
        subprocess.run([sys.executable, "-m", "py_compile", str(script)], check=True)

    committed = {path.name for path in RESULTS.glob("*.json")}
    if not committed:
        if (ROOT / "docs" / "BASELINE.md").exists():
            raise SystemExit("docs/BASELINE.md exists before generated results")
        check_links()
        print("OK: pre-run repository; bands exist and no model results are committed")
        return
    valid_sets = (
        CORE_RESULTS,
        CORE_RESULTS | A3A_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS | A5C_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS | A5C_RESULTS | A3F_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS | A5C_RESULTS | A3F_RESULTS | A3G_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS | A5C_RESULTS | A3F_RESULTS | A3G_RESULTS | A5D_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS | A5C_RESULTS | A3F_RESULTS | A3G_RESULTS | A5D_RESULTS | A6_RESULTS,
        CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS | A5C_RESULTS | A3F_RESULTS | A3G_RESULTS | A5D_RESULTS | A6_RESULTS | A6B_RESULTS,
    )
    if committed not in valid_sets:
        raise SystemExit(
            "partial result set: expected "
            f"a declared stage set through "
            f"{sorted(CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS | A3C_RESULTS | A3D_RESULTS | A3E_RESULTS)}, "
            f"found {sorted(committed)}"
        )

    run("analysis/baseline.py", "--check")
    run("analysis/force_allocation.py", "--check")
    run("analysis/architecture_trade.py", "--check")
    run("tools/make_baseline.py", "--check")
    if A3A_RESULTS <= committed:
        run("analysis/topology_screen.py", "--check")
        run("tools/make_topology_screen.py", "--check")
    elif (ROOT / "docs" / "TOPOLOGY_SCREEN.md").exists():
        raise SystemExit("docs/TOPOLOGY_SCREEN.md exists before the A3a result")
    check_links()
    cad_build = ROOT / "cad" / "BUILD.json"
    if cad_build.exists():
        subprocess.run([sys.executable, "cad/build_gen1.py", "--check"], cwd=ROOT, check=True)
        render_manifest = ROOT / "cad" / "renders" / "gen1" / "RENDERS.json"
        if render_manifest.exists():
            subprocess.run([sys.executable, "cad/render_gen1.py", "--check"], cwd=ROOT, check=True)
    else:
        generated_cad_docs = [ROOT / "cad" / "DIMENSIONS.md", ROOT / "cad" / "BOM.md"]
        if any(path.exists() for path in generated_cad_docs):
            raise SystemExit("generated CAD documents exist before cad/BUILD.json")
    gen2_build = ROOT / "cad" / "BUILD_GEN2.json"
    if gen2_build.exists():
        subprocess.run([sys.executable, "cad/build_gen2.py", "--check"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "cad/render_gen2.py", "--check"], cwd=ROOT, check=True)
        run("tools/package_gen2_cad.py", "--check")
        run("tools/make_gen2_cad_docs.py", "--check")
        run("tools/make_figure_index.py", "--check")
    elif any(
        path.exists()
        for path in (ROOT / "cad" / "GEN2_DIMENSIONS.md", ROOT / "cad" / "GEN2_BOM.md")
    ):
        raise SystemExit("generated Gen2 CAD documents exist before cad/BUILD_GEN2.json")
    if A5A_RESULTS <= committed:
        run("analysis/interface_fit_screen.py", "--check")
        run("tools/make_interface_fit_screen.py", "--check")
    elif (ROOT / "docs" / "INTERFACE_FIT_SCREEN.md").exists():
        raise SystemExit("docs/INTERFACE_FIT_SCREEN.md exists before the A5a result")
    if A3B0_RESULTS <= committed:
        run("analysis/edge_force_bound.py", "--check")
        run("tools/make_edge_force_bound.py", "--check")
    elif (ROOT / "docs" / "EDGE_FORCE_BOUND.md").exists():
        raise SystemExit("docs/EDGE_FORCE_BOUND.md exists before the A3b0 result")
    if A5B_RESULTS <= committed:
        run("analysis/quad_comb_screen.py", "--check")
        run("tools/make_quad_comb_screen.py", "--check")
    elif (ROOT / "docs" / "QUAD_COMB_SCREEN.md").exists():
        raise SystemExit("docs/QUAD_COMB_SCREEN.md exists before the A5b result")
    if A3B1_RESULTS <= committed:
        run("analysis/stator_throat_bound.py", "--check")
        run("tools/make_stator_throat_bound.py", "--check")
    elif (ROOT / "docs" / "STATOR_THROAT_BOUND.md").exists():
        raise SystemExit("docs/STATOR_THROAT_BOUND.md exists before the A3b1 result")
    if A3C_RESULTS <= committed:
        run("analysis/induction_screen.py", "--check")
        run("tools/make_induction_screen.py", "--check")
    elif (ROOT / "docs" / "INDUCTION_SCREEN.md").exists():
        raise SystemExit("docs/INDUCTION_SCREEN.md exists before the A3c result")
    if A3D_RESULTS <= committed:
        run("analysis/induction_operating_point.py", "--check")
        run("tools/make_induction_operating_point.py", "--check")
    elif (ROOT / "docs" / "INDUCTION_OPERATING_POINT.md").exists():
        raise SystemExit("docs/INDUCTION_OPERATING_POINT.md exists before the A3d result")
    if A3E_RESULTS <= committed:
        run("analysis/stator_circuit.py", "--check")
        run("tools/make_stator_circuit.py", "--check")
    elif (ROOT / "docs" / "STATOR_CIRCUIT.md").exists():
        raise SystemExit("docs/STATOR_CIRCUIT.md exists before the A3e result")
    if A5C_RESULTS <= committed:
        run("analysis/cad_fit_check.py", "--check")
        run("tools/make_cad_fit.py", "--check")
    elif (ROOT / "docs" / "CAD_FIT.md").exists():
        raise SystemExit("docs/CAD_FIT.md exists before the A5c result")
    if A3F_RESULTS <= committed:
        run("analysis/fluxbridge_cage.py", "--check")
        run("tools/make_fluxbridge_cage.py", "--check")
    elif (ROOT / "docs" / "FLUXBRIDGE_CAGE.md").exists():
        raise SystemExit("docs/FLUXBRIDGE_CAGE.md exists before the A3f result")
    if A3G_RESULTS <= committed:
        run("analysis/fluxbridge_optimization.py", "--check")
        run("tools/make_fluxbridge_optimization.py", "--check")
    elif (ROOT / "docs" / "FLUXBRIDGE_OPTIMIZATION.md").exists():
        raise SystemExit("docs/FLUXBRIDGE_OPTIMIZATION.md exists before the A3g result")
    if A5D_RESULTS <= committed:
        run("analysis/gen2_cad_fit.py", "--check")
        run("tools/make_gen2_cad_fit.py", "--check")
    elif (ROOT / "docs" / "GEN2_CAD_FIT.md").exists():
        raise SystemExit("docs/GEN2_CAD_FIT.md exists before the A5d result")
    if A6_RESULTS <= committed:
        run("analysis/gen2_field.py", "--artifact-check")
        run("tools/make_gen2_field.py", "--check")
    elif (ROOT / "docs" / "GEN2_FIELD.md").exists():
        raise SystemExit("docs/GEN2_FIELD.md exists before the A6 result")
    if A6B_RESULTS <= committed:
        run("analysis/gen21_field.py", "--artifact-check")
        run("tools/make_gen21_field.py", "--check")
    elif (ROOT / "docs" / "GEN21_FIELD.md").exists():
        raise SystemExit("docs/GEN21_FIELD.md exists before the A6b result")
    stage = (
        "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d/A3e/A5c/A3f/A3g/A5d/A6/A6b"
        if A6B_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d/A3e/A5c/A3f/A3g/A5d/A6 with A6b declared"
        if A6_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d/A3e/A5c/A3f/A3g/A5d with A6 declared"
        if A5D_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d/A3e/A5c/A3f/A3g with A5d declared"
        if A3G_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d/A3e/A5c/A3f with A3g declared"
        if A3F_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d/A3e/A5c with A3f declared"
        if A5C_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d/A3e with A5c declared"
        if A3E_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c/A3d with A3e declared"
        if A3D_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1/A3c with A3d declared"
        if A3C_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b/A3b1 with A3c declared"
        if A3B1_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0/A5b with A3b1 declared"
        if A5B_RESULTS <= committed
        else "A1/A2/A3a/A5a/A3b0 with A5b declared"
        if A3B0_RESULTS <= committed
        else "A1/A2/A3a/A5a with A3b0 declared"
        if A5A_RESULTS <= committed
        else "A1/A2/A3a with A5a declared"
        if A3A_RESULTS <= committed
        else "A1/A2 with A3a declared"
    )
    print(f"OK: {stage} generated results and local links are current")


if __name__ == "__main__":
    main()
