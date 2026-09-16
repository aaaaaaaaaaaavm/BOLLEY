"""Generate the current review surface from committed result records.

This is reporting, not a new physical analysis. A screening script can pass while its
design is rejected; the disposition is therefore displayed separately from screen_pass.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROWS = [
    ("A9b", "sectional_drive_a9b.json", "A9b_sectional_drive_residual_reclosure.md", "Sectional drive", "Model reclosure; supplier and package work remains"),
    ("A9c", "hot_winding_margin.json", "A9c_hot_winding_margin.md", "Hot winding", "Resistance/temperature allowance; P40 remains open"),
    ("A9d", "supplier_bridge_screen.json", "A9d_supplier_bridge_lower_bound.md", "Supplier bridge", "Conduction lower bound; full electronics remain open"),
    ("A9e", "selector_realization_screen.json", "A9e_selector_realization_lower_bound.md", "Selector arrangement", "No selector promoted; electrical partition requires redesign"),
    ("A9f", "turn_current_exchange.json", "A9f_turn_current_exchange.md", "12-turn candidate", "Selected for fresh field, switching and package checks"),
    ("A5f", "gen3_12turn_winding_fit.json", "A5f_gen3_12turn_winding.md", "First winding fit", "Failed copper-volume gate; failure retained"),
    ("A5g", "gen3_12turn_path_fit.json", "A5g_gen3_12turn_path.md", "Corrected path", "Analytical path fit; detailed CAD follows"),
    ("A5h", "gen3_12turn_detailed_fit.json", "A5h_gen3_12turn_detailed_cad.md", "Detailed winding CAD", "Nominal envelopes only; not a manufacturing release"),
    ("A9g", "selected_winding_reclosure.json", "A9g_selected_winding_reclosure.md", "12-turn drive reclosure", "Six of sixteen assumed loss corners pass; hot switching remains open"),
]


def outputs():
    records = []
    for run, filename, sheet, label, limit in ROWS:
        path = ROOT / "analysis/results" / filename
        raw = path.read_bytes()
        data = json.loads(raw)
        if type(data.get("screen_pass")) is not bool:
            raise ValueError(f"{run}: missing boolean screen_pass")
        if not (ROOT / "validation" / sheet).is_file():
            raise ValueError(f"{run}: missing run sheet")
        disposition = data.get("disposition")
        if run == "A5h":
            disposition = f"{data['band_pass_count']}/{data['band_count']} nominal-CAD bands"
        if not isinstance(disposition, str) or not disposition:
            raise ValueError(f"{run}: missing design disposition")
        records.append((run, filename, sheet, label, limit, data, disposition,
                        hashlib.sha256(raw).hexdigest()))

    chosen = records[4][5]["selected_candidate"]
    hot = records[1][5]
    lines = [
        "# Current Fluxrelay review", "",
        "I generate this review from the committed result files with `tools/make_review_snapshot.py`.",
        "It supplements the historical [run status](../validation/STATUS.md) with the later drive and winding sequence.",
        "A passing screen means its declared calculation checks passed. The design disposition can still be a rejection.",
        "Nothing here is hardware evidence.", "",
        "![Current drive and winding evidence](../figures/current-review.svg)", "",
        "| Run | Screen checks | Design disposition | Remaining boundary |",
        "|---|---|---|---|",
    ]
    for run, filename, sheet, label, limit, data, disposition, digest in records:
        lines.append(f"| [{run}](../validation/{sheet}) | {'PASS' if data['screen_pass'] else 'FAIL'} | `{disposition}` | {limit} |")
    lines += ["", "## The selected electrical screen", "",
        "These A9f values use the declared scaling and supplier conduction assumptions. They do not include a complete hot switching implementation.", "",
        "| Quantity | Model output |", "|---|---:|",
        f"| Turns per cell | {chosen['turns_per_cell']} |",
        f"| Rated phase current | {chosen['rated_phase_current_a']:.3f} A |",
        f"| Reference source energy | {chosen['reference_source_energy_j']:.3f} J |",
        f"| Qualification source energy | {chosen['qualification_source_energy_j']:.3f} J |",
        f"| Healthy required DC link | {chosen['healthy_required_dc_link_v_scaled']:.3f} V |",
        f"| Failed-cell required DC link | {chosen['failed_cell_required_dc_link_v_scaled']:.3f} V |",
        f"| Supplier modules | {chosen['installed_onsemi_module_count']} |",
        f"| Module-only mass | {chosen['module_only_mass_kg']:.4f} kg |", "",
        f"A9c's earlier configuration has {hot['a9b_margin_to_900j_j']:.3f} J remaining below its reference cap,",
        f"equivalent to only {hot['remaining_temperature_above_a7c_1p25_corner_c']:.3f} C beyond its inherited hot-winding corner under that model.",
        "That is not the margin of the later A9f candidate; the configurations must stay separate.", "",
        "## Selected-partition reclosure", "",
        "[A9g](SELECTED_WINDING_RECLOSURE.md) reruns the ideal-current handoff model at twelve turns.",
        "It reproduces the current/voltage/energy scaling at two resolutions. The selected 25 C",
        "conduction point leaves 10.280918 J below the reference cap; only six of sixteen assumed",
        "conduction/additional-loss corners pass. This does not close the actual winding field or hot switching.", "",
        "## What I would close next", "",
        "1. Check RMS, peak, internal-path and package current definitions against the supplier data before crediting a device rating.",
        "2. Re-solve the field/current distribution for the actual A5h winding, including terminals and lead routing.",
        "3. Couple hot conduction, switching, parasitics, protection, supply sag and thermal paths across the full campaign.",
        "4. Carry the lane gap and guide alignment through manufacturing, thermal and dynamic tolerances.",
        "5. Close installed mass and six-degree-of-freedom release/fault behaviour before a full-system prototype design review.", "",
        "The [completion standard](COMPLETION_STANDARD.md) still applies. The shared",
        "[prototype programme](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/PROTOTYPE_READINESS.md)",
        "defines the intended build package and the dependency order. These are open work, not newly passed gates.", "",
        "## Reproduction and provenance", "",
        "Run `python tools/make_review_snapshot.py --check` to check these surfaces against their source files.",
        "This does not rerun the physical analyses. `python tools/check_repo.py` checks the existing repository pipeline;",
        "full solver and CAD reconstruction remain distinct from artifact checks.", "",
        "| Source | SHA-256 |", "|---|---|",
    ]
    for run, filename, sheet, label, limit, data, disposition, digest in records:
        lines.append(f"| [{filename}](../analysis/results/{filename}) | `{digest}` |")
    markdown = "\n".join(lines) + "\n"
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="748" viewBox="0 0 1100 748" role="img" aria-labelledby="title desc">',
           '<title id="title">BOLLEY drive and winding evidence</title>',
           '<desc id="desc">Nine computational screens. A9e rejects its selector arrangement despite passing its screening checks. A5h closes nominal winding CAD only. A9g exposes the remaining loss budget. No hardware evidence.</desc>',
           '<rect width="1100" height="748" rx="16" fill="#0d1b2a"/>',
           '<g font-family="Arial, sans-serif">',
           '<text x="32" y="43" font-size="15" fill="#7dd3fc">BOLLEY / FLUXRELAY</text>',
           '<text x="32" y="82" font-size="30" font-weight="bold" fill="#ffffff">The latest drive and winding evidence</text>',
           '<text x="32" y="111" font-size="16" fill="#cbd5e1">Calculation checks and design acceptance are separate verdicts.</text>']
    for i, (run, filename, sheet, label, limit, data, disposition, digest) in enumerate(records):
        y = 144 + i * 60
        negative = not data["screen_pass"] or "NO_SELECTOR_PROMOTED" in disposition
        colour = "#fda4af" if negative else "#7dd3fc"
        verdict = "DESIGN REJECTED" if "NO_SELECTOR_PROMOTED" in disposition else ("SCREEN FAILED" if not data["screen_pass"] else "BOUNDED RESULT")
        svg += [f'<rect x="24" y="{y}" width="1052" height="52" rx="7" fill="#172b40"/>',
                f'<text x="40" y="{y+23}" font-size="17" font-weight="bold" fill="{colour}">{run}</text>',
                f'<text x="110" y="{y+23}" font-size="17" fill="#ffffff">{html.escape(label)}</text>',
                f'<text x="810" y="{y+23}" font-size="13" font-weight="bold" fill="{colour}">{verdict}</text>',
                f'<text x="110" y="{y+43}" font-size="14" fill="#cbd5e1">{html.escape(limit)}</text>']
    svg += ['<text x="32" y="717" font-size="15" fill="#fbbf24">MODEL / NOMINAL CAD ONLY  |  Physical performance and flight readiness remain unverified.</text>', '</g></svg>']
    return {ROOT / "docs/CURRENT_REVIEW.md": markdown,
            ROOT / "figures/current-review.svg": "\n".join(svg) + "\n"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f"stale review surface: {path.relative_to(ROOT)}")
        else:
            path.write_text(content)
    print("Current review matches source results; no hardware gate is promoted")


if __name__ == "__main__":
    main()
