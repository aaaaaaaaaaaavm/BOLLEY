# A5h Gen3 detailed 12-turn winding CAD

Date frozen: 2026-08-31

State: DECLARED, NOT RUN

## Question

A5g found a nominal path-corrected 12-turn winding envelope that restores A5e copper volume. It was still an analytical envelope. A5h asks whether twelve individual maximum-insulation conductor envelopes can be built around the unchanged Gen3 core without solid intersection when repeated through an ABC module and all 27 cells on one face.

## Controlled geometry

I inherit A5g's selected winding without another search:

- 12 turns per cell as four nested in-plane turns by three radial layers;
- 2.31 x 1.5936227286879734 mm bare conductor screen;
- 2.48 x 1.7636227286879733 mm maximum insulated envelope;
- 36.39101817049621 x 8.8 mm inner winding opening;
- 6.75 mm lower winding start above the payload face;
- 0.6850000000000005 mm gap between alternating coil layers;
- unchanged A5e 27-cell core, 45.3 mm pitch, Fluxrelay cage and track geometry.

The CAD conductor solids use the maximum rectangular insulation envelope. I keep copper corner rounding in the analytical volume calculation because the insulation envelope, rather than the copper corner surface, controls nominal interference.

## Hard bands

| Band | Criterion | Source |
|---|---:|---|
| Turn solids per cell | exactly 12 | A5g topology |
| Full-face turn solids | exactly 324 | 27 cells x 12 turns |
| Coil/core intersection | <= 1e-6 mm3 | inherited A5e |
| Consecutive-cell coil intersection | <= 1e-6 mm3 | inherited A5e |
| Same-layer coil intersection | <= 1e-6 mm3 | inherited A5e |
| Coil to Fluxrelay radial clearance | >= 0.5 mm | inherited A5e |
| Inter-layer radial clearance | >= 0 mm | A5g nominal non-interference |
| Upper coil to back yoke | >= 0 mm | A5g nominal non-interference |
| Analytical copper volume | <= 0.5% relative error from 4,933.76 mm3 per cell | inherited A5e |
| Mean turn length | <= 0.5% relative error from 118.6 mm | A5g/A5e |

## Artifacts

A pass must create reproducible STEP and STL masters for:

- one detailed 12-turn cell;
- one three-cell ABC module;
- the full 27-cell winding set for one face;
- the full 27-cell core plus detailed winding set for one face.

I do not require a four-face assembly render in A5h. Four-face rotation was already closed by A5e and A5h changes only the winding solids.

## Evidence boundary

A5h is nominal CAD. It does not include manufacturing tolerance, thermal growth, enamel damage at bends, terminals, lead exits, impregnation, bridge mounting, cooling, switching loss or vibration. A pass does not replace A5e as the controlled full assembly until the downstream package and electrical gates also pass.
