# A6c — Gen2.2 Fluxmanifold-R4 nonlinear field gate

**What I knew at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear RMS-equivalent magnetostatic FEA  
**Purpose:** I wanted to test the smallest explicit correction to A6b while making peak-field disposition
conservative across all three formal meshes.

## The correction I froze

A6b misses only the moving-ligament and stationary-haunch peaks. Gen2.2 therefore changes two
controlled values and nothing else:

- MMF falls 6.25%, from 1,280 to 1,200 A-turn RMS: 400 A in three turns, 14.815 MA/m².
- The circular return haunch grows from 3 to 4 mm radius.

The blade centres, 28 mm face, 7.3 mm legs, 7 mm back yoke, three-turn 81 mm² slot copper, material
curves, domains, local spacings and solver tolerances are inherited unchanged from A6b. The larger
haunch adds 0.041 kg of stationary core; four-face active primary becomes 15.774 kg.

## Why I strengthened the band evaluation

A6 and A6b used base/fine/expanded meshes for numerical convergence but evaluated most physical
bands on the fine mesh. A6b showed that a point peak can be larger on the expanded coarse mesh.
A6c therefore evaluates field range, slot imbalance, height variation, ligament peak,
stationary-core peak, source closure and nonlinear closure on the worst value across **all three**
meshes. Fine-mesh inductance and the same convergence differences remain the relevant definitions.

This strengthening is declared before A6c runs. It does not alter either failed A6b band.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A6c-1 | Base-to-fine mean field change <=2%. | Refine again. |
| A6c-2 | Base-to-fine coenergy change <=4%. | Refine again. |
| A6c-3 | Expanded-boundary mean field changes <=2%. | Enlarge air domain. |
| A6c-4 | Every mesh mean tooth-slice field remains inside 0.72–0.86 T RMS. | Reject MMF or geometry. |
| A6c-5 | Worst mesh four-slot integrated-flux imbalance <=5%. | Reject manifold balance. |
| A6c-6 | Worst mesh active-height field CV <=15%. | Reject uniform-sheet input. |
| A6c-7 | Worst mesh inferred magnetic-ligament peak <=1.45 T. | Reduce MMF or change ligament. |
| A6c-8 | Worst mesh stationary-core peak <=1.55 T. | Enlarge or reshape manifold. |
| A6c-9 | Fine per-cell inductance is 0.68–1.05 times A3g. | Reject turn exchange or drive range. |
| A6c-10 | Worst mesh source-current residual <=1e-10. | Reject mapping. |
| A6c-11 | Worst mesh final nonlinear solution change <=1e-4. | Reject unconverged solve. |

Paired lower/upper limits produce the same 13 executable Boolean bands as A6b.

## What I explicitly did not claim

All A6b non-bands remain. In particular this is not transient cage force, a routed winding,
thermal evidence, tolerance closure, hardware validation or selected-lot material evidence.

## Output I required

Commit full histories and mesh metrics, explicit worst-mesh extrema, all bands and three indexed
figures. Pass promotes Gen2.2 only to circuit, CAD and transient-force closure—not to hardware.

## What I recorded

**I completed the run on 2026-08-13. I recorded: 12/13 bands pass; Gen2.2 is rejected.**

The base, fine and expanded meshes contain 209,000, 743,988 and 236,000 triangles. All numerical
differences are below 0.32%. Worst-mesh mean field remains 0.7372–0.7395 T and worst stationary
core peak falls to 1.4113 T. The only failure is the 1.5306 T inferred ligament peak against the
1.45 T limit. [The controlled result](../docs/GEN22_FIELD.md) preserves the worst-mesh extrema.

I moved the failure action to a spacecraft-side magnetic-rib cross-section change under a new gate.
I kept the A6c limits unchanged and blocked circuit, CAD and transient promotion.
