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
    )
    if committed not in valid_sets:
        raise SystemExit(
            "partial result set: expected "
            f"a declared stage set through "
            f"{sorted(CORE_RESULTS | A3A_RESULTS | A5A_RESULTS | A3B0_RESULTS | A5B_RESULTS | A3B1_RESULTS)}, "
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
    stage = (
        "A1/A2/A3a/A5a/A3b0/A5b/A3b1"
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
