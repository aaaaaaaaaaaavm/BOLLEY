# A5f Gen3 12-turn winding-envelope reclosure

Date frozen: 2026-08-31

State: MODELLED, REJECTED

Pre-run correction: ADR-056 replaces my first cross-section-only copper check with the A5e copper-volume consistency quantity. No A5f calculator or result existed when I made that correction.

## Question

A9f selected 12 turns per cell at 126.66666666666667 A because the original 4-turn/380 A winding makes the sectional power electronics too large. I had not shown that twelve insulated turns can occupy the A5e stator without changing its magnetic source window, copper amount or nominal non-interference.

A5f asks one narrower question: can I replace the A5e homogeneous four-turn copper pack with a twelve-turn rectangular-wire envelope and retain the same nominal stator/cage geometry and A5e copper volume?

## Result

No. I evaluated 81 nominal bare-wire widths from 2.00 through 2.80 mm. Fifty-four candidates pass every declared check except the detailed copper-volume band. None passes all bands.

The geometry-feasible candidate with the smallest copper-volume error uses a 2.53 x 1.4550468392368454 mm bare rounded rectangle. With the frozen Grade 2 insulation envelope it reaches a 123.80074942778953 mm mean turn length and 5,150.111176196045 mm3 of copper per cell. That is 4.3851175613739635% above A5e's 4,933.76 mm3 target, against the unchanged 0.5% band.

The candidate preferred by the frozen minimum-envelope rule if I ignore the copper-volume failure is 2.31 x 1.5936227286879734 mm bare. It fits nominally with 0.6850000000000005 mm inter-layer and upper-yoke clearance, 36.39101817049621 mm same-layer axial clearance and 25.74707500895467% gross slot fill, but its 126.01796365900758 mm mean turn length uses 5,242.347288214715 mm3 of copper. That is 6.254606795116002% too much.

I reject the fixed-inner-span twelve-turn winding. I do not alter the 0.5% copper-volume band and I do not promote an A5f candidate.

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

The candidate layout is four nested conductor envelopes through the in-plane ring wall by three radial layers. Adjacent stator cells retain A5e's alternating lower/upper coil layers. The detailed conductor centreline lengths determine copper volume.

## Selection rule

Among candidates passing every hard band, I select in this order:

1. minimum total gross insulated conductor-envelope area per coil side;
2. maximum smaller radial clearance between the two alternating coil layers and between the upper layer and the back yoke;
3. minimum gross ring-wall thickness;
4. smaller nominal bare width.

No candidate reached this selection because the copper-volume band rejected all 81 points.

## Hard bands

| Band | Criterion | Result |
|---|---:|---|
| Turns | exactly 12 | PASS |
| Excitation | exactly 1,520 A-turn RMS | PASS |
| Copper current density | <= 40 A/mm2 | PASS |
| Bare cross-section identity | <= 1e-12 relative error from 41.6 mm2 per coil side | PASS |
| Detailed copper volume | <= 0.5% relative error from 4,933.76 mm3 per cell | FAIL for every candidate |
| Gross insulated slot fill | <= 60% | PASS for the 54 geometry-feasible candidates |
| Coil to Fluxrelay | >= 0.5 mm | PASS for the 54 geometry-feasible candidates |
| Inter-layer radial clearance | >= 0 mm | PASS for the 54 geometry-feasible candidates |
| Upper coil to back yoke | >= 0 mm | PASS for the 54 geometry-feasible candidates |
| Same-layer axial clearance | >= 0 mm | PASS for the 54 geometry-feasible candidates |
| Coil/core intersection | <= 1e-6 mm3 | PASS for the 54 geometry-feasible candidates by positive axis-aligned separation |
| Adjacent-coil intersection | <= 1e-6 mm3 | PASS for the 54 geometry-feasible candidates by positive axis-aligned separation |

## Evidence boundary

A5f is a nominal rectangular-wire envelope and path-length model. It does not establish winding manufacturability, voltage insulation qualification, thermal life, turn-to-turn partial-discharge behaviour, supplier availability, lead routing, local bridge placement or vibration survival.

I do not export STEP or STL for a point rejected upstream on copper volume. A separate declared redesign may shorten the in-plane winding path while retaining A9f's electrical point.
