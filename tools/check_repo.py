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
STAGED_RESULTS = {"topology_screen.json"}


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
    valid_sets = (CORE_RESULTS, CORE_RESULTS | STAGED_RESULTS)
    if committed not in valid_sets:
        raise SystemExit(
            "partial result set: expected "
            f"{sorted(CORE_RESULTS)} or {sorted(CORE_RESULTS | STAGED_RESULTS)}, "
            f"found {sorted(committed)}"
        )

    run("analysis/baseline.py", "--check")
    run("analysis/force_allocation.py", "--check")
    run("analysis/architecture_trade.py", "--check")
    run("tools/make_baseline.py", "--check")
    if STAGED_RESULTS <= committed:
        run("analysis/topology_screen.py", "--check")
        run("tools/make_topology_screen.py", "--check")
    elif (ROOT / "docs" / "TOPOLOGY_SCREEN.md").exists():
        raise SystemExit("docs/TOPOLOGY_SCREEN.md exists before the A3a result")
    check_links()
    stage = "A1/A2/A3a" if STAGED_RESULTS <= committed else "A1/A2 with A3a declared"
    print(f"OK: {stage} generated results and local links are current")


if __name__ == "__main__":
    main()
