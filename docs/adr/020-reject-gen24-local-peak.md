# ADR-020 — reject Gen2.4 on the unresolved local ligament peak

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6e worst-of-three-mesh nonlinear field result

## Decision

Reject the exact 1.14 mm Gen2.4 rib and preserve its 1.5159 T failure. Do not widen the rib again
and do not relax the 1.45 T band. Retain the R4 stationary primary, three-turn winding and the
1,190 A-turn operating point while changing the passive blade's internal magnetic/conductive
allocation.

## Why

Mean field, coenergy and boundary results converge within 0.30%, yet the inferred local maximum
rises with mesh refinement. Added uniform width has reached diminishing returns against a local
flux-entry concentration. The next useful degree of freedom is axial magnetic continuity beneath
the copper ladder, not another whole-rib mass increment.

## Consequences

- A6e remains failed at 12/13 magnetic bands; the 0.30 kg preference also remains missed.
- A continuous magnetic backstrap beneath each copper rung may trade some cage conductance for
  magnetic duty without increasing the external envelope.
- That material exchange needs a new field gate and then a fresh transient cage/thermal screen.
