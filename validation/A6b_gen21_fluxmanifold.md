# A6b — Gen2.1 Fluxmanifold nonlinear field gate

**State at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear RMS-equivalent magnetostatic FEA  
**Purpose:** decide whether a wider, radius-fed stationary return repairs A6 without changing the
passive Fluxbridge principle or hiding the failed Gen2 point.

## Why this candidate exists

A6 localised Gen2's failure. The four moving blades were balanced and below their ligament limit,
but the 3 mm back yoke crowded flux into a sharp inner corner. Mean blade field was low while the
return peak and independently integrated inductance were high.

Non-validation development meshes were used to size a correction before this run sheet was
written. Their results may explain the candidate but cannot pass this gate. The formal geometry,
three meshes and all bands below are now frozen before the A6b output exists.

## The Fluxmanifold correction

- Spread the four blade centres from 3.2 to 4.0 mm pitch; interface projection remains 6.25 mm.
- Grow the stationary face from 20 to 28 mm, outer legs to 7.3 mm and back yoke to 7.0 mm.
- Feed the yoke through a 3 mm circular haunch at each inner corner instead of a sharp step.
- Replace four 20.25 mm² turns with three 27 mm² turns. Slot copper remains 81 mm².
- Drive 1,280 A-turn RMS: 426.667 A in three turns, at 15.802 MA/m².

The turn exchange is copper-neutral in section. At equal ampere-turn and rise time, its ideal
resistance and inductance ratios are 0.5625 and 0.5625, copper loss is unchanged, and inductive
voltage falls to 0.75 of the four-turn case. Those scaling identities are not a circuit result;
A6b still integrates nonlinear coenergy independently.

The calculated four-face active primary is 15.733 kg: 8.069 kg stationary core plus the retained
7.664 kg copper. This adds stationary iron relative to A3g's 11.829 kg package but remains far
below Gen1's 40.96 kg active primary. CAD and circuit gates must independently confirm it.

## Frozen formal meshes

1. **Base:** 0.15 mm local spacing in a 90 × 65 mm domain.
2. **Fine:** 0.075 mm local spacing in the same domain.
3. **Expanded boundary:** base local spacing in a 120 × 95 mm domain.

All material, source, blade, haunch-tangent and sample boundaries are inserted explicitly. The
nonlinear and linear solver tolerances are identical to the completed A6 method.

## Bands declared before execution

| ID | Band | Failure action |
|---|---|---|
| A6b-1 | Base-to-fine mean field change <=2%. | Refine again; no physics disposition. |
| A6b-2 | Base-to-fine coenergy change <=4%. | Refine again; no inductance claim. |
| A6b-3 | Expanded-boundary mean field changes <=2%. | Enlarge air domain. |
| A6b-4 | Fine mean tooth-slice field is 0.72–0.86 T RMS. | Reject MMF or geometry. |
| A6b-5 | Four-slot integrated-flux imbalance <=5%. | Reject the series-flux manifold. |
| A6b-6 | Active-height field coefficient of variation <=15%. | Reject uniform-sheet input. |
| A6b-7 | Inferred magnetic-ligament field <=1.45 T. | Reduce MMF or change ligament fraction. |
| A6b-8 | Stationary-core peak field <=1.55 T. | Enlarge or reshape the manifold. |
| A6b-9 | Fine per-cell inductance is 0.68–1.05 times A3g's four-turn value. | Reject the turn exchange or redo drive bounds. |
| A6b-10 | Source-current residual <=1e-10 of one side. | Reject source mapping. |
| A6b-11 | Final nonlinear solution change <=1e-4. | Reject unconverged solve. |

Paired lower and upper limits remain executable separately, giving 13 stored Boolean bands.

## Explicit non-bands

- The B-H curves remain screening assumptions, not selected-lot supplier data.
- The circular haunch is meshed in 2D; it is not a lamination drawing or manufacturing process.
- This is not transient induction, axial force, end effect, current-crowding or thermal evidence.
- Three turns are sectional copper accounting, not a routed lead/insulation CAD package.
- Passing does not restore A3g's source-energy result; circuit closure must use A6b inductance.
- The primary mass is analytical geometry accounting and excludes structure, cooling and leads.

## Required output

Commit all mesh counts, nonlinear histories, field/flux per blade, peaks by material, coenergy,
inductance, convergence differences, every band and three indexed figures. Pass advances only to
Gen2.1 circuit and CAD closure. Failure changes the manifold again or ends this Fluxbridge branch.
