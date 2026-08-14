# Bolley

**A cooperative electromagnetic CubeSat deployer that spends a few hundred grams on the
spacecraft to remove kilograms of machinery from the launcher.**

> **Status:** This is my Phase 0 design study. I have not built, measured, qualified or flown
> Bolley. I label every number here as an assumption, model output, external datum or measurement
> so I cannot quietly turn a calculation into evidence.

![A8b Fluxrelay feasible design island](analysis/figures/a8b/A8b_feasible_island.png)

I began with VOLLEY by asking whether I could give an unmodified CubeSat a programmable deployment
velocity without making it carry propulsion. I answered that question with a reusable magnetic
sled. The model worked, but the sled became 9.445 kg: most of my energy accelerated launcher
hardware, and most of my mechanism existed only to stop and return it.

With Bolley, I change one premise. I let a compatible CubeSat carry four **passive reaction
interfaces** while I keep every winding, switch, sensor and joule of stored energy on the launcher.
The spacecraft itself becomes the passive translator of a segmented linear electromagnetic
machine.

That small concession lets me remove the launch sled, the post-release brake and the return stroke.

I record the uncomfortable branches as carefully as the promising one. I rejected a buried return,
a three-fin comb and a shared-pole quad-comb for different physical reasons. Gen1 Fluxfoil passed
my thin-sheet circuit, then exact CAD exposed a 66.7:1 copper-window deficit. I answered that failure
with **Fluxbridge**: a passive perforated magnetic matrix with a shorted copper ladder.

I then took the design through seven field iterations. Gen2.5 Fluxweb gave me the first 13/13
transverse-field pass. Its four lanes still overheated, so I added a fifth in Gen2.6 Quintweb. A6g
again passed 13/13; in A7b I found that the fifth lane closed cage temperature, current density,
slip and secondary efficiency. Only the 125% winding-resistance reference shot remained high, at
959.9 J against 900 J.

In A8a I found the more important axial contradiction: a 336 mm cage cannot remain fully engaged
while travelling 900 mm through a 900 mm stator. My as-drawn package produces 10.70 m/s, and a
simple full-overlap extension reaches 22.20 kg.

In A8b I closed that analytical contradiction by co-designing cage length, cell pitch, current and
copper instead of correcting them one at a time. Of my 2,856 declared candidates, 77 pass every
hard band. I selected **Gen2.7 Fluxrelay** by minimax margin: 27 cells at 45.3 mm pitch, 380 A and
10.4 mm2 per turn; a 318.6 mm passive cage traverses a 1.2231 m sectional primary with 2.25 mm
engagement guards. I calculate a 895.47 J hot reference shot and 15.91 kg installed primary mass.
Those margins are model outputs, not hardware evidence, and my 1.534 T stationary peak is still a
current-scaled A6g surrogate. Fresh A6h field and A7c circuit reclosure are my next kill gates.

## The architecture I am carrying forward

- Four independently controlled face channels apply axial force around the spacecraft.
- Software distributes force so its centroid follows the declared payload centre of gravity.
- Each face channel contains a 27-cell, 1.2231 m sectional stationary primary.
- A 318.6 mm five-lane passive cage energises at most three cells per phase in each channel.
- The Phase 0 reference duty is a 4 kg 3U payload, 8 g and approximately 12 m/s.
- A 6 kg 3U is the qualification sizing case, not silently treated as a 4 kg satellite.
- No permanent magnets, powered spacecraft hardware, pyrotechnics or pressure vessels are added.
- An independent gate carries ascent loads and prevents an uncommanded deployment.
- When the field ends, the CubeSat coasts out. No moving launcher member follows it.

I continue to reject the original six-tile / 900 mm arrangement. In Fluxrelay I count every
installed cell against the launcher mass band, but I charge only the conservative active window
with pulse loss. That is the correction: inactive copper does not disappear from my mass ledger.

## The zero-modification control I use

In VOLLEY I tested the strongest zero-modification control: drive directly on the existing CDS
aluminium corner rails. In [A30](https://github.com/aaaaaaaaaaaavm/VOLLEY/commit/acce22e04f3ba81e8d44d5318f78949a0518fb7a)
I rejected it. My solved transverse edge factor is 0.0253 rather than 0.55, leaving only 41.9 N even
at a generous 0.60 T. Pole pitch cannot simultaneously rescue the narrow conductor and large
rail-to-stator gap.

My surviving VOLLEY direction is now a roughly 90 mm conductive plate: 0.248 kg in the analytical
example, with much better edge utilization. I use that as Bolley's honest control. Fluxrelay must
earn its 0.371 kg interface through four-channel force-centroid authority, a controlled magnetic
path, tolerance to rail alloy/anodization, lower launcher complexity or lower cost. I do not accept
“no sled” alone as enough.

## What is not claimed

I have not demonstrated force density, commutation voltage, thermal margin, electromagnetic
compatibility, tip-off, rail life, cost or customer acceptance. I use the current calculations as
screens to decide which coupon to build. I do not treat them as validation of the machine.

I think the exact combination may be unusual. I do not treat that as proof of novelty or
patentability.

## My current controlled baseline

| Layer | Current evidence | Disposition |
|---|---|---|
| Selected payload interface | 318.6 mm five-lane Fluxrelay cage; 0.37136 kg modelled increment | 28.64 g below absolute limit; both preferences missed |
| Selected primary | 27 cells/channel, 45.3 mm pitch, 380 A, 10.4 mm2/turn | 1.2231 m and 15.908 kg installed |
| A8b coupled closure | 77/2,856 candidates pass; selected worst demand 0.99496 | Analytical point promoted to A6h/A7c |
| Transverse field | A6g 751,282-element fine mesh passed 13/13 at 375 A | A8b's 380 A point still needs fresh A6h meshes |
| Cage + circuit | Selected hot reference 895.47 J; qualification 1,305.16 J | Must be reclosed from A6h field/inductance |
| Axial engagement | 318.6 mm cage inside 1.2231 m stator over 900 mm travel | 2.25 mm modelled guard at both endpoints |
| CAD | Seven STEP + seven STL historical Gen2 masters | Gen3 Fluxrelay geometry is next, not yet evidence |
| Hardware evidence | None | Central claim remains open |

## Start here

1. [`REQUIREMENTS.md`](REQUIREMENTS.md) — what the machine must do.
2. [`HISTORY.md`](HISTORY.md) — real project lineage without backdating Bolley.
3. [`docs/CONCEPT.md`](docs/CONCEPT.md) — architecture and shot sequence.
4. [`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) — numbers that can end the concept.
5. [`docs/GEN26_FIELD.md`](docs/GEN26_FIELD.md) — the passing five-lane transverse field.
6. [`docs/GEN26_CAGE_CIRCUIT.md`](docs/GEN26_CAGE_CIRCUIT.md) — the isolated hot-energy miss.
7. [`docs/AXIAL_ENGAGEMENT.md`](docs/AXIAL_ENGAGEMENT.md) — why the exact axial package is rejected.
8. [`docs/GEN27_CODESIGN.md`](docs/GEN27_CODESIGN.md) — the selected Fluxrelay package and margins.
9. [`docs/GEN2_CAD_FIT.md`](docs/GEN2_CAD_FIT.md) — historical CAD evidence and STEP/STL packages.
10. [`validation/STATUS.md`](validation/STATUS.md) — every declared run and its disposition.
11. [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) — the live defect register.
12. [`DECISION_LOG.md`](DECISION_LOG.md) — compact decision chain with full ADRs.
13. [`docs/FIGURE_INDEX.md`](docs/FIGURE_INDEX.md) — every visual, its source and evidence class.

## Reproduce

The algebraic stages require only Python. Gen2 CAD uses the pinned packages in
`requirements-cad.txt`; A6 field reproduction uses `requirements-field.txt`.

```bash
python tools/check_repo.py
python analysis/gen27_codesign.py --check
python analysis/gen26_field.py --check  # full three-mesh A6g re-solve
```

`tools/check_repo.py` verifies deterministic outputs, package manifests, local links and the
declared stage sequence. The complete A6g re-solve is kept explicit because it is materially more
expensive than an artifact-integrity check.

## Rules I use for this repository

1. I write requirements before calculations.
2. I freeze validation bands before results and never widen them after a run.
3. I call model-to-model agreement a cross-check, not experimental validation.
4. I change generated results through their scripts, never by hand.
5. I let a failed result change the design or kill it; I do not change the threshold.
6. I never mix assumptions, external data, model outputs and measurements without labels.
7. I keep this repository as my engineering record, not a paper-production project.
