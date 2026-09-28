# Common core and winding geometry candidate

Study record · 17 September 2026

I retain the inherited 4 mm inner haunch and the existing twelve-turn winding. I raise both coil heights by 0.25 mm, then raise the back yoke and extend the outer legs to obtain a geometry-only candidate. The yoke-only R1 screen failed all cases at the unchanged 0.5 mm layout margin. The original arrangement is retained as a rejected case.

| Back-yoke rise (mm) | Lower clearance (mm) | Upper clearance (mm) | 0.5 mm assumed layout margin |
|---:|---:|---:|---|
| 0 | 0.550000 | 0.000000 | fail |
| 0.5 | 0.550000 | 0.000000 | fail |
| 1 | 0.550000 | 0.087041 | fail |
| 1.5 | 0.550000 | 0.394969 | fail |
| 2 | 0.550000 | 0.656162 | pass |
| 3 | 0.550000 | 0.991470 | pass |
| 4 | 0.550000 | 1.045000 | pass |

The smallest sampled passing rise is **2 mm**. Exact solid clearance is 0.550000 / 0.656162 mm for the lower/upper slices. The per-cell core volume increases by 607.926000 mm³. This has a mass and magnetic-path penalty; no installed mass advantage is claimed.

The resolved parameter file defines both the revised field geometry and the conductor envelopes used to generate the three STEP coupon references. Coordinates are transverse millimetres from the payload face, with axial depth equal to one tooth. These are straight conductor slices, not closed three-dimensional turns, full-face assemblies or terminal geometry.

New magnetic analysis is required for this exact geometry. A6h cannot be inherited. Previously reported A6i results are not available in this working copy; its reported failures are not replaced by this geometric clearance result. Hot drive, end effects, protection, thermal duty and the 0.20 mm payload lane gap remain open. No powered coupon is released.

Geometric verification: PASS.

[Original criteria](../validation/A6j_core_winding_reconciliation.md) · [R2 criteria](../validation/A6j_R2_winding_height.md) · [Rejected R1](../validation/results/A6j_R1_yoke_only_rejected.json) · [Results](../analysis/results/core_winding_reconciliation.json) · [Common parameters](../cad/core_winding_reconciled_parameters.json) · [STEP references](../cad/exports/core_reconciliation)
