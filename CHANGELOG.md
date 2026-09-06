# Changelog

## 2026-09-06: my BSX audit and A5h execution

I found that check_repo.py rejected every result added after A12, so the checker could not inspect A9 through A9f or A5f/A5g. I extended its declared stage sequence without accepting unknown or partial sets and wired the new evidence into the existing checks.

I executed A5h from its frozen 2026-08-31 inputs and bands, added a result evaluator, and required source and artifact hashes for all four STEP/STL scopes. This is nominal conductor-envelope CAD, not winding manufacture, electrical closure or qualification. A5f's failed fixed-path result remains unchanged.


I keep two more useful chronological records than a conventional software changelog:

- [`HISTORY.md`](HISTORY.md) records the engineering lineage and corrections.
- [`DECISION_LOG.md`](DECISION_LOG.md) records every frozen gate and disposition.

This file records repository-level changes that do not belong to one physical analysis.

## 2026-08-31

- I added a four-quadrant knowledge map that separates model-bounded facts, latent repository
  mining, known evidence gaps and Unbound architecture searches.
- I added an assumption and constraint ledger. Every controlled architecture rule now has a source,
  a stated consequence and explicit delete/move/invert/merge/scale attacks without changing the
  controlled baseline.
- I separated current open problems by the kind of evidence that can move them, while keeping
  `OPEN_PROBLEMS.md` authoritative for wording and status.
- I opened `VLAB-B002` for a powered cooperative spacecraft interface and `VLAB-B003` for
  distributed Fluxpiston feed. Both remain lab questions and change no BOLLEY requirement.

## 2026-08-28

- I retained the selected Gen3 Fluxrelay baseline, A5e and the A10–A12 architecture work without
  turning exploratory branches into completion claims.
- I applied CC BY 4.0 across the repository and added citation, provenance, contribution, metadata,
  workflow and issue-reporting surfaces. Bolley had no earlier explicit licence, so I added no
  fictitious superseded-licence file.
