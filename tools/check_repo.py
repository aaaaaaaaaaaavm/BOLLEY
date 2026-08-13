"""Repository integrity check with a valid pre-run state."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis" / "results"
EXPECTED_RESULTS = {
    "baseline.json",
    "force_allocation.json",
    "architecture_trade.json",
}


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
    if committed != EXPECTED_RESULTS:
        raise SystemExit(f"partial result set: expected {sorted(EXPECTED_RESULTS)}, found {sorted(committed)}")

    run("analysis/baseline.py", "--check")
    run("analysis/force_allocation.py", "--check")
    run("analysis/architecture_trade.py", "--check")
    run("tools/make_baseline.py", "--check")
    check_links()
    print("OK: generated results, baseline and local links are current")


if __name__ == "__main__":
    main()

