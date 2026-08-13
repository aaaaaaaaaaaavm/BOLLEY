# Bolley

**A cooperative electromagnetic CubeSat deployer that spends a few hundred grams on the
spacecraft to remove kilograms of machinery from the launcher.**

> **Status:** Phase 0 design study. Nothing has been built, measured, qualified or flown.
> Every number in this repository is either an assumption, a first-order model output or
> external evidence labelled as such.

![Bolley Gen2 nominal assembly](cad/renders/gen2/01_gen2_hero.png)

VOLLEY asked whether an unmodified CubeSat could receive a programmable deployment velocity
without carrying propulsion. Its answer used a reusable magnetic sled. The model worked, but
the sled became 9.445 kg: most of the energy accelerated launcher hardware and most of the
mechanism existed to stop and return it.

Bolley changes one premise. A compatible CubeSat carries four **passive reaction interfaces**.
All windings, switches, sensors and stored energy remain on the launcher. The spacecraft becomes
the passive translator of a segmented linear electromagnetic machine.

That small concession removes the launch sled, the post-release brake and the return stroke.

The repository records the uncomfortable branches as carefully as the promising one. The buried
corner return, three-fin comb and shared-pole quad-comb were each rejected by a different bound.
Gen1 Fluxfoil then closed its thin-sheet and lumped-circuit screens, but exact CAD found a 66.7:1
copper-window deficit. That failure produced **Fluxbridge**: a thin passive perforated magnetic
matrix with a shorted copper ladder, spending 0.285 kg on a 3U interface so the launcher no longer
needs a massive moving primary.

A3g found ten robust Fluxbridge candidates and selected a 30 mm-pitch Gen2 point. A5d turned it
into seven STEP masters, seven STL previews, a discrete cage coupon and an alternating-layer
winding with zero nominal interference. A6 then did what the earlier lumped model could not: an
independently meshed nonlinear field solve. It rejected the operating point—0.6568 T mean blade
field, 3.2346 T stationary-core peak and 1.3945× the predicted inductance. Gen2.1 is therefore a
stationary-return redesign, not an attempt to hide the failed bands. No candidate has passed
transient force FEA, provider review, structural analysis or hardware test.

## The proposed machine

- Four independently controlled face channels apply axial force around the spacecraft.
- Software distributes force so its centroid follows the declared payload centre of gravity.
- Six 150 mm stator tiles provide a 0.90 m acceleration zone.
- The Phase 0 reference duty is a 4 kg 3U payload, 8 g and approximately 12 m/s.
- A 6 kg 3U is the qualification sizing case, not silently treated as a 4 kg satellite.
- No permanent magnets, powered spacecraft hardware, pyrotechnics or pressure vessels are added.
- An independent gate carries ascent loads and prevents an uncommanded deployment.
- When the field ends, the CubeSat coasts out. No moving launcher member follows it.

## What is not claimed

Bolley has not demonstrated force density, commutation voltage, thermal margin, electromagnetic
compatibility, tip-off, rail life, cost or customer acceptance. The current calculations are
screens that decide which coupon to build. They are not validation of the machine.

The exact combination may be unusual. That is not proof of novelty or patentability.

## Current controlled baseline

| Layer | Current evidence | Disposition |
|---|---|---|
| Passive spacecraft interface | Four 6.25 mm Fluxbridge blades per face; 0.285 kg total modelled mass | Retained for Gen2.1 |
| Nominal mechanical package | Seven STEP + seven STL masters; 13/13 A5d CAD bands | Passes nominal fit only |
| Selected Gen2 operating point | A3g `p30_B0.56` | Rejected by A6 |
| Independent field solution | 621,180-element fine mesh; 10/13 A6 bands | Return geometry must change |
| Hardware evidence | None | Central claim remains open |

## Start here

1. [`REQUIREMENTS.md`](REQUIREMENTS.md) — what the machine must do.
2. [`docs/CONCEPT.md`](docs/CONCEPT.md) — architecture and shot sequence.
3. [`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) — numbers that can end the concept.
4. [`validation/README.md`](validation/README.md) — why bands are written before runs.
5. [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) — the work that remains.
6. [`docs/TOPOLOGY_SCREEN.md`](docs/TOPOLOGY_SCREEN.md) — why the original flux return was rejected.
7. [`docs/INTERFACE_FIT_SCREEN.md`](docs/INTERFACE_FIT_SCREEN.md) — the comb-fin envelope and allocation result.
8. [`docs/EDGE_FORCE_BOUND.md`](docs/EDGE_FORCE_BOUND.md) — why the three-fin comb was rejected before FEA.
9. [`docs/QUAD_COMB_SCREEN.md`](docs/QUAD_COMB_SCREEN.md) — the smallest redesign that recovered ideal force margin.
10. [`docs/FLUXBRIDGE_CAGE.md`](docs/FLUXBRIDGE_CAGE.md) — why the passive cage replaced Gen1.
11. [`docs/FLUXBRIDGE_OPTIMIZATION.md`](docs/FLUXBRIDGE_OPTIMIZATION.md) — the robust Gen2 search.
12. [`docs/GEN2_CAD_FIT.md`](docs/GEN2_CAD_FIT.md) — CAD evidence and downloadable STEP/STL packages.
13. [`docs/GEN2_FIELD.md`](docs/GEN2_FIELD.md) — the independent field result that rejected A3g.
14. [`DECISION_LOG.md`](DECISION_LOG.md) — compact decision chain with full ADRs.
15. [`docs/FIGURE_INDEX.md`](docs/FIGURE_INDEX.md) — every visual, its source and evidence class.

## Reproduce

The algebraic stages require only Python. Gen2 CAD uses the pinned packages in
`requirements-cad.txt`; A6 field reproduction uses `requirements-field.txt`.

```bash
python tools/check_repo.py
python analysis/gen2_field.py --check   # full three-mesh A6 re-solve
```

`tools/check_repo.py` verifies deterministic outputs, package manifests, local links and the
declared stage sequence. The complete A6 re-solve is kept explicit because it is materially more
expensive than an artifact-integrity check.

## Repository rules

1. Requirements precede calculations.
2. Validation bands precede results and are never widened after a run.
3. Model-to-model agreement is a cross-check, not experimental validation.
4. Generated results are changed through their scripts, never by hand.
5. A failed result changes the design or kills it. It does not change the threshold.
6. Assumptions, external data, model outputs and measurements are never mixed without labels.
7. This repository is an engineering record, not a paper-production project.
