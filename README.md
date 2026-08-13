# Bolley

**A cooperative electromagnetic CubeSat deployer that spends a few hundred grams on the
spacecraft to remove kilograms of machinery from the launcher.**

> **Status:** Phase 0 design study. Nothing has been built, measured, qualified or flown.
> Every number in this repository is either an assumption, a first-order model output or
> external evidence labelled as such.

![A8a separates the stroke failure from the circuit correction](analysis/figures/a8a/A8a_correction_trade.png)

VOLLEY asked whether an unmodified CubeSat could receive a programmable deployment velocity
without carrying propulsion. Its answer used a reusable magnetic sled. The model worked, but
the sled became 9.445 kg: most of the energy accelerated launcher hardware and most of the
mechanism existed to stop and return it.

Bolley changes one premise. A compatible CubeSat carries four **passive reaction interfaces**.
All windings, switches, sensors and stored energy remain on the launcher. The spacecraft becomes
the passive translator of a segmented linear electromagnetic machine.

That small concession removes the launch sled, the post-release brake and the return stroke.

The repository records the uncomfortable branches as carefully as the promising one. A buried
return, three-fin comb and shared-pole quad-comb were rejected by different bounds. Gen1 Fluxfoil
passed its thin-sheet circuit and then exact CAD exposed a 66.7:1 copper-window deficit. That
failure produced **Fluxbridge**: a passive perforated magnetic matrix with a shorted copper ladder.

The design then survived seven field iterations. Gen2.5 Fluxweb was the first 13/13 transverse
field pass. Its four lanes still overheated, so Gen2.6 Quintweb added a fifth. A6g again passed
13/13; A7b showed that the fifth lane closed cage temperature, current density, slip and
secondary efficiency. Only the 125% winding-resistance reference shot remained high, at 959.9 J
against 900 J.

A8a then found the more important axial contradiction: a 336 mm cage cannot remain fully engaged
while travelling 900 mm through a 900 mm stator. The as-drawn package produces 10.70 m/s, and a
full-overlap extension reaches 22.20 kg. Sectional excitation survives—the required resistance
ratio is 0.8202 and cell/tile windows produce 0.50/0.70—but the axial package does not. That is the
current correction boundary. No candidate has passed transient force FEA, provider review,
structural analysis or hardware test.

## The architecture that remains

- Four independently controlled face channels apply axial force around the spacecraft.
- Software distributes force so its centroid follows the declared payload centre of gravity.
- A sectional stationary primary energises only cells overlapped by the passive interface.
- The Phase 0 reference duty is a 4 kg 3U payload, 8 g and approximately 12 m/s.
- A 6 kg 3U is the qualification sizing case, not silently treated as a 4 kg satellite.
- No permanent magnets, powered spacecraft hardware, pyrotechnics or pressure vessels are added.
- An independent gate carries ascent loads and prevents an uncommanded deployment.
- When the field ends, the CubeSat coasts out. No moving launcher member follows it.

The original six-tile / 900 mm arrangement is rejected by A8a. Tile count, active cage length and
conductor area are now co-design variables; they are not quietly inherited by the next CAD model.

## The zero-modification control

The same design programme now records a second sledless branch in
[VOLLEY Gen6](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/GEN6_RAIL_DRIVE.md): drive
directly on the CubeSat's existing CDS aluminium corner rails. Its 0.45 T sizing is attractive,
but its 0.55 transverse edge-effect factor is still an assumption awaiting 3D transient evidence.

That branch is Bolley's control, not a result to ignore. A cooperative interface must earn its
0.35–0.40 kg by giving a more reliable flux path, lower sensitivity to somebody else's rail alloy
and anodised geometry, better force-centroid authority or a cheaper launcher. “No sled” alone is
no longer enough to justify Bolley.

## What is not claimed

Bolley has not demonstrated force density, commutation voltage, thermal margin, electromagnetic
compatibility, tip-off, rail life, cost or customer acceptance. The current calculations are
screens that decide which coupon to build. They are not validation of the machine.

The exact combination may be unusual. That is not proof of novelty or patentability.

## Current controlled baseline

| Layer | Current evidence | Disposition |
|---|---|---|
| Passive spacecraft interface | Five layered Quintweb blades per face; 0.38823 kg modelled increment | A6g field pass; 11.77 g below absolute limit |
| Transverse field | 751,282-element fine mesh; 13/13 A6g bands | Retained for the next axial co-design |
| Cage + circuit | 3,528 A7b CG/corner/payload points; 2/4 corners pass all 19 bands | Translator closes; hot reference energy does not |
| Axial engagement | 9,001 A8a travel points; 5/10 bands | Exact 900 mm package rejected |
| Sectional excitation | Cell/tile phase resistance = 0.50/0.70× A7b | Retained as Gen2.7 mechanism, not yet a circuit |
| CAD | Seven STEP + seven STL Gen2 masters and deterministic packages | Historical nominal geometry; Gen3 blocked on A8b |
| Hardware evidence | None | Central claim remains open |

## Start here

1. [`REQUIREMENTS.md`](REQUIREMENTS.md) — what the machine must do.
2. [`HISTORY.md`](HISTORY.md) — real project lineage without backdating Bolley.
3. [`docs/CONCEPT.md`](docs/CONCEPT.md) — architecture and shot sequence.
4. [`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) — numbers that can end the concept.
5. [`docs/GEN26_FIELD.md`](docs/GEN26_FIELD.md) — the passing five-lane transverse field.
6. [`docs/GEN26_CAGE_CIRCUIT.md`](docs/GEN26_CAGE_CIRCUIT.md) — the isolated hot-energy miss.
7. [`docs/AXIAL_ENGAGEMENT.md`](docs/AXIAL_ENGAGEMENT.md) — why the exact axial package is rejected.
8. [`docs/GEN2_CAD_FIT.md`](docs/GEN2_CAD_FIT.md) — historical CAD evidence and STEP/STL packages.
9. [`validation/STATUS.md`](validation/STATUS.md) — every declared run and its disposition.
10. [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) — the live defect register.
11. [`DECISION_LOG.md`](DECISION_LOG.md) — compact decision chain with full ADRs.
12. [`docs/FIGURE_INDEX.md`](docs/FIGURE_INDEX.md) — every visual, its source and evidence class.

## Reproduce

The algebraic stages require only Python. Gen2 CAD uses the pinned packages in
`requirements-cad.txt`; A6 field reproduction uses `requirements-field.txt`.

```bash
python tools/check_repo.py
python analysis/axial_engagement.py --check
python analysis/gen26_field.py --check  # full three-mesh A6g re-solve
```

`tools/check_repo.py` verifies deterministic outputs, package manifests, local links and the
declared stage sequence. The complete A6g re-solve is kept explicit because it is materially more
expensive than an artifact-integrity check.

## Repository rules

1. Requirements precede calculations.
2. Validation bands precede results and are never widened after a run.
3. Model-to-model agreement is a cross-check, not experimental validation.
4. Generated results are changed through their scripts, never by hand.
5. A failed result changes the design or kills it. It does not change the threshold.
6. Assumptions, external data, model outputs and measurements are never mixed without labels.
7. This repository is an engineering record, not a paper-production project.
