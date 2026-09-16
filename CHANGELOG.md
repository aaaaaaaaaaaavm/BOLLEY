# Changelog

## 2026-09-16: selected winding reclosure and public review

I declared A9g before execution, reran the 12-turn partition through the existing time-domain
handoff model at two resolutions and checked the current, voltage and energy scaling independently.
The local-bridge sensitivity retains all 16 assumed loss corners: six satisfy the reference cap.
Only 10.280918 J remains at the 25 C conduction point. No supplier hot-switching claim follows.
P11, P39 and P40 remain open; P38 keeps its previous bounded modelled disposition.
The project now has a visual website linked from this README, with nominal CAD and direct evidence routes.

## 2026-09-15: reconcile the register against A9b-A9f and A5f-A5h

I read the later run sheets back against the defect register before choosing the next run
configuration, because four rows still described the state at A7c and A5e.

P38 moves from `OPEN` to `MODELLED`. That is the disposition A9b authorises in its own words, a
pass "may move P38 to MODELLED only for the ideal-current-tracking selector effects represented by
A9", and ADR-049 ties keeping it open to a failure that did not occur. The row now also records
what the modelled state rests on: A9's transient ran at 4 turns and 380 A.

P11, P39 and P40 keep their states and gain the numbers the later runs attached to them. P11 now
names the single partial supplier datum that exists, 25 C conduction resistance for the onsemi
NXV08H400XT1. P39 records that A9f puts 2.5488 kg of module-only mass against the 91.896 g A5e
leaves in the material band, 27.7 times the whole remainder, and that is before busbar, capacitors,
gate drive, cooling, wiring or structure. P40 now keeps three margins apart instead of reading them
as one trend: 6.588 J at A7c, 2.252 J at A9c for the A9b configuration, and 889.719 J at A9f's
selected point under a different loss model.

The same three-margin correction goes into `docs/KNOWLEDGE_MAP.md`, `docs/ASSUMPTION_LEDGER.md` and
`docs/KILL_CRITERIA.md`, each of which quoted 6.588 J as the live margin of the selected point. The
kill threshold itself is unchanged.

What this decides: the next configuration to run is the A5h winding at A9f's 12-turn, 126.667 A
partition. A9's transient, and therefore everything P38 rests on, is at the old 4-turn partition.
The exchange holds MMF at 1,520 A-turns and leaves the mechanical and magnetic geometry alone, but
phase resistance and inductance scale with (N/4)^2, link demand with N/4, and bridge conduction with
current squared, and A9f says a selected point "must return to nonlinear field and CAD/winding
checks because the turn packing and current distribution have changed".

No close condition edited, no acceptance band touched, no result recomputed. A5f's copper-volume
failure and A9e's selector rejection stay as recorded.

## 2026-09-14: expose the later drive and winding decisions

I shortened the README around the controlled Fluxrelay assembly and the separately selected
12-turn candidate. The former page remains accessible at its exact revision. I added a generated
current review linked from the historical status page: A9b–A9f and A5f–A5h now carry source hashes,
calculation verdicts, design dispositions and remaining limits together.

The distinction matters at A9e: its screen_pass is true while its disposition rejects the selector
arrangement. The review preserves that rejection and A5f's copper-volume failure. A5h remains a
nominal-CAD result. No analysis, acceptance band or physical closure changes. The repository
checker now rejects stale review surfaces.

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
