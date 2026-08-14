# A1 — first-order sizing

## The question I asked

Does the proposed rail area and mass clear a first-order screen strongly enough to justify an
electromagnetic model?

## Inputs I froze

Inputs come from `cad/parameters.json`. They are assumptions except for the named CubeSat
geometry/mass guidance and the published 35.16 kPa LSRM shear benchmark.

## Bands I declared before the run

| Band | Pass condition | Failure action |
|---|---|---|
| 1 | Ideal exit velocity is 11.8–12.0 m/s. | Reconcile duty inputs; do not interpret later bands. |
| 2 | Screened rail increment is <=0.25 kg preferred and <=0.40 kg absolute. | Above preferred: open mass defect. Above absolute: reject architecture. |
| 3 | 6 kg, worst-CG required shear is <=26 kPa. | Do not claim area feasibility; increase area or reject topology. |
| 4 | Worst-corner channel force is <=255 N. | Resize every channel before any coupon design. |
| 5 | Reference mechanical utilisation is >=94%. | Revisit the cooperative-interface premise. |
| 6 | Gross reference energy at the pessimistic 40% screen is <=900 J. | Reject energy claim or change architecture. |
| 7 | Pole-passage frequency is <=300 Hz at ideal reference velocity. | Change pitch or declare high-voltage commutation a critical failure. |

Passing A1 means only that dimensions do not immediately kill the concept.

## Script I used

`python analysis/baseline.py --write`

