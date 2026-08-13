# A2 — four-corner force allocation

## Question

Across +/-20 mm transverse CG offsets, can four axial rail forces remain positive, sum to the
commanded thrust and place their force centroid at the payload CG?

## Bands declared before the run

The sweep uses the 6 kg qualification mass plus the screened rail increment and evaluates a
21 x 21 CG grid.

| Band | Pass condition | Failure action |
|---|---|---|
| 1 | Minimum commanded rail force >=0 N. | The allocation law cannot cover the declared envelope. |
| 2 | Maximum rail force <=255 N. | Increase channel rating or restrict CG envelope before A3. |
| 3 | Force-sum error <=1e-9 N. | Correct the implementation. |
| 4 | Reconstructed force-centroid error <=1e-9 m. | Correct the implementation. |
| 5 | Maximum single-channel fraction <=0.52 of total thrust. | Revisit rail geometry or allocation. |

This run tests algebra, not sensors, structural compliance, electromagnetic cross-coupling or
control bandwidth.

## Script

`python analysis/force_allocation.py --write`

