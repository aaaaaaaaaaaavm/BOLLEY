# A3 — one-corner electromagnetic coupon

## The question I asked

Can a covered hybrid rail and one stator channel produce the qualification force for the full
pulse while current can still commutate at maximum speed?

## Bands I declared before FEA or hardware

| Quantity | Preferred | Fail / kill |
|---|---:|---:|
| Average axial force | >=255 N | <255 N |
| Pulse duration | 150 ms | cannot sustain 150 ms |
| DC-link voltage | <=200 V | >400 V |
| Force ripple | <=3% peak/mean | >8% peak/mean |
| Rail temperature rise per shot | <=10 C | >25 C |
| Unbalanced normal force | <=100 N | >250 N |

The coupon must include the aluminium cover, adhesive/capture geometry, nominal gap and worst
manufacturing gap. A bare steel result does not answer the question.

## Where I left it

NOT RUN. A nonlinear flux-linkage map is required before hardware.

