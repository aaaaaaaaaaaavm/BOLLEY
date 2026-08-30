# A5f Gen3 12-turn winding-envelope reclosure

Date frozen: 2026-08-31

State: DECLARED, NOT RUN

Pre-run correction: ADR-056 replaces my first cross-section-only copper check with the A5e copper-volume consistency quantity. No A5f calculator or result existed when I made that correction.

## Question

A9f selected 12 turns per cell at 126.66666666666667 A because the original 4-turn/380 A winding makes the sectional power electronics too large. I have not shown that twelve insulated turns can occupy the A5e stator without changing its magnetic source window, copper amount or nominal non-interference.

A5f asks one narrower question: can I replace the A5e homogeneous four-turn copper pack with a twelve-turn rectangular-wire envelope and retain the same nominal stator/cage geometry and A5e copper volume?

This is not a manufacturing tolerance gate. I use nominal bare conductor dimensions and the IEC Grade 2 maximum insulation increase. Bare-wire dimensional tolerance, bend radius, coating selection, terminals, impregnation and supplier acceptance remain open.

## Controlled inputs

I inherit from A5e and A9f:

- 12 turns per cell;
- 126.66666666666667 A RMS phase current;
- 1,520 A-turn RMS excitation;
- 3.466666666666667 mm2 target bare copper area per turn;
- 41.6 mm2 target bare copper area per coil side;
- 118.6 mm A5e mean turn length;
- 4,933.76 mm3 A5e copper volume per cell;
- 45.3 mm cell pitch;
- 40.1 mm inner axial coil span;
- 8.8 mm inner transverse coil span;
- 0.5 mm minimum coil-to-Fluxrelay radial clearance;
- 60% maximum gross slot fill;
- 1e-6 mm3 nominal solid-intersection ceiling.

I search nominal bare rectangular-wire width from 2.00 through 2.80 mm in 0.01 mm increments. For every width I solve the bare thickness required to retain the A9f copper cross-section after the IEC corner radius is removed from the rectangle. I apply the Grade 2 maximum 0.17 mm increase to each overall conductor dimension.

The candidate layout is four nested conductor envelopes through the in-plane ring wall by three radial layers. Adjacent stator cells retain A5e's alternating lower/upper coil layers. The detailed conductor centreline lengths determine copper volume. I do not assume that equal cross-section means equal copper volume.

## Selection rule

Among candidates passing every hard band, I select in this order:

1. minimum total gross insulated conductor-envelope area per coil side;
2. maximum smaller radial clearance between the two alternating coil layers and between the upper layer and the back yoke;
3. minimum gross ring-wall thickness;
4. smaller nominal bare width.

I will not change this rule after execution.

## Hard bands

| Band | Criterion | Source |
|---|---:|---|
| Turns | exactly 12 | A9f selected point |
| Excitation | exactly 1,520 A-turn RMS | A6h/A9f controlled excitation |
| Copper current density | <= 40 A/mm2 | inherited A8b/A5e winding limit |
| Bare cross-section identity | <= 1e-12 relative error from 41.6 mm2 per coil side | controlled A9f turn/current exchange |
| Detailed copper volume | <= 0.5% relative error from 4,933.76 mm3 per cell | inherited A5e copper-volume consistency band, corrected by ADR-056 |
| Gross insulated slot fill | <= 60% | inherited A5e band |
| Coil to Fluxrelay | >= 0.5 mm | inherited A5e band |
| Inter-layer radial clearance | >= 0 mm | nominal non-interference |
| Upper coil to back yoke | >= 0 mm | nominal non-interference |
| Same-layer axial clearance | >= 0 mm | nominal non-interference |
| Coil/core intersection | <= 1e-6 mm3 | inherited A5e solid-intersection band |
| Adjacent-coil intersection | <= 1e-6 mm3 | inherited A5e solid-intersection band |

## Evidence boundary

A5f may show a nominal insulated-winding envelope fits. It cannot establish winding manufacturability, voltage insulation qualification, thermal life, turn-to-turn partial-discharge behaviour, supplier availability, lead routing, local bridge placement or vibration survival.

The selected A9f point does not replace the controlled Gen3 baseline unless A5f passes and its later electrical/field/package gates also pass.
