# A6 — independent Gen2 transverse-field solve

**What I knew at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear magnetostatic finite-element model  
**Purpose:** I wanted to test whether A3g's lumped MMF and the A5d winding actually produce the required
four-slot series flux before transient/3D induction work is attempted.

## The model I froze

The solve uses the out-of-plane magnetic vector potential $A_x$ on the Gen2 $y$-$z$ tooth-centre
cross-section:

$$-\nabla\cdot(\nu\nabla A_x)=J_x.$$

I set the current source to the A3g nominal 321.402 A RMS in four turns. Two equal 81 mm² coil-side
regions carry opposite $J_x$, giving 1,285.607 A-turn with zero net source current. The model
includes:

- the 20 mm serpentine core, 4.5 mm outer legs, 1.8 mm separators and 3 mm back yoke;
- four 0.94 mm magnetic blade regions inside the 1.4 mm slots;
- the A5d lower-layer coil cross-section around the negative-$y$ outer leg;
- a nonlinear conservative stationary-core B-H assumption;
- a nonlinear 2605SA1 screening curve capped by its 1.56 T supplier saturation induction; and
- the 0.625 axial ligament fraction used to infer local ligament field from the homogenized tooth
  slice.

I use an RMS-equivalent magnetostatic slice, not a time-harmonic induction or force solve.
I froze the complete geometry, curves, meshes and bands in `cad/gen2_field_parameters.json`.

## The three meshes I declared before execution

1. **Base:** 0.15 mm local spacing in a 80 × 60 mm domain.
2. **Fine:** 0.075 mm local spacing in the same domain.
3. **Expanded boundary:** base local spacing in a 110 × 85 mm domain.

Every material, slot, coil and sample boundary is inserted explicitly into the tensor mesh. The
outer boundary holds $A_x=0$. Reluctivity is updated by relaxed Picard iteration to a relative
solution change below $10^{-4}$.

### Execution refinement declared before the first completed solve

The first execution attempt was stopped without producing results after the sparse-direct
factorization proved unsuitable for the declared 174,048 / 621,180 / 196,512-element mesh set.
No geometry, material curve, mesh, excitation, quantity definition or acceptance band changed.
The linear algebra method alone was replaced before any field result existed: conjugate gradient
to a relative residual of $10^{-9}$, preconditioned by a PyAMG smoothed-aggregation hierarchy.
A base-mesh diagnostic then exposed a nonlinear limit cycle at the original fixed 0.65 Picard
relaxation; that incomplete diagnostic was stopped without a result. Before any completed solve,
the hierarchy was set to rebuild at each nonlinear update and the fixed relaxation was replaced
by bounded vector Aitken relaxation (0.05–0.65, initially 0.65), with an 80-iteration ceiling.
Linear iterations, residuals and relaxation factors are required in the output. These are
execution corrections, not physical-model refinements.

## Quantities and definitions I used

- **Mean tooth-slice field:** mean magnitude of $B_y$ in each active Fluxbridge region over
  $1\le z\le5$ mm, then mean across four blades.
- **Slot imbalance:** maximum absolute deviation of a blade's integrated $B_y$ flux per axial
  depth from the four-blade mean, divided by that mean.
- **Height variation:** pooled coefficient of variation of $|B_y|$ over the same active regions.
- **Ligament field:** local axial-ligament estimate $B_{slice}/0.625$.
- **Per-cell inductance:** $2W/I^2$, where nonlinear magnetic coenergy $W$ is integrated over the
  cross-section and multiplied by the 15 mm tooth depth.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A6-1 | Base-to-fine mean field change <=2%. | Refine again; no physics disposition. |
| A6-2 | Base-to-fine coenergy change <=4%. | Refine again; no inductance claim. |
| A6-3 | Expanded-boundary mean field changes <=2%. | Enlarge air domain. |
| A6-4 | Fine mean tooth-slice field is 0.72–0.86 T RMS. | Reject A3g MMF/current or geometry. |
| A6-5 | Four-slot integrated-flux imbalance <=5%. | Reject the series-flux assumption. |
| A6-6 | Active-height $|B_y|$ coefficient of variation <=15%. | Reject the uniform-sheet force input. |
| A6-7 | Inferred magnetic-ligament field <=1.45 T. | Increase ligament fraction or reject material screen. |
| A6-8 | Stationary-core peak field <=1.55 T. | Increase core area or reject. |
| A6-9 | Fine per-cell inductance is 0.70–1.30 times A3g. | Recompute the drive and energy model. |
| A6-10 | Positive/negative source-current residual <=1e-10 of one side. | Reject mesh/source mapping. |
| A6-11 | Final nonlinear relative solution change <=1e-4. | Reject unconverged solve. |

Paired lower/upper limits are executable separately.

## What I explicitly did not claim

- The B-H curves are declared screening assumptions; the stationary steel is not selected and
  perforated/annealed Fluxbridge material has not been measured.
- The 2D slice cannot resolve axial tooth duty, copper rungs, end effects, phase harmonics, bar
  currents, slip, force, normal attraction or cogging.
- Dirichlet outer air is a numerical boundary, not a magnetic shield.
- Agreement with A3g would not be experimental validation.

## Output I required

Commit mesh sizes, nonlinear histories, field/flux per blade, peak fields by material, coenergy,
inductance, source-current closure, all convergence differences, every band, field maps and a
disposition. A passing A6 advances to transient discrete-cage analysis; a physics-band failure
supersedes the A3g operating point.

## What I recorded

**I completed the run on 2026-08-13. I recorded: 10/13 bands pass; A3g `p30_B0.56` is rejected.**

The base, fine and expanded meshes contain 174,048, 621,180 and 196,512 triangles. Mean-field,
coenergy and boundary differences are 0.786%, 0.295% and 1.637%, so the failure is not a mesh or
air-domain artifact. The fine solution gives 0.6568 T mean tooth-slice field, 3.2346 T stationary
core peak and 1.3945 times the A3g per-cell inductance. Those fail the frozen lower-field,
core-field and upper-inductance bands. Slot balance, height uniformity, ligament field, source
closure and nonlinear convergence pass.

The controlled output is [docs/GEN2_FIELD.md](../docs/GEN2_FIELD.md); complete values and nonlinear
histories remain in `analysis/results/gen2_field.json`. The failure action is a Gen2.1 stationary
return redesign. It is not a threshold change and it does not promote transient force work.
