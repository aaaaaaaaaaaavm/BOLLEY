# ADR-038 — why I promoted the nominal Gen3 geometry

- **Date:** 2026-08-14
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A5e exact Gen3 CAD and fit gate

## What I decided

I accepted A5e's 17/17 result and promoted exactly `n27_p45.3_I380_A10.4` to tolerance,
structure and A9 transient sectional-drive work.

## Why I chose it

My new build represents the selected 318.6 mm cage, 27-cell 1.2231 m primary and nine-cell active
window directly instead of stretching the historical Gen2 package. Exact nominal intersections are
zero, winding volume agrees with A8b to numerical round-off, the lane and coil clearances remain
positive, and the cage retains its 2.25 mm engagement guard after 900 mm travel. Every STEP/STL
master is hashed and packaged reproducibly.

The pass is deliberately narrow in meaning. The 91.896 g active-material margin does not contain
structure, insulation, cooling, wiring or power electronics, and a 0.20 mm nominal lane gap is not
a tolerance stack.

## What follows

- I require A9 to resolve current rise, cell handoff, commutation ripple, failed-cell behavior and
  exit timing before I release coupon drawings.
- I require a separate tolerance and structural package before I call any part manufacturable.
- I keep P1–P16, P20–P21, P25, P27, P29–P30, P35 and P38–P40 open according to their existing
  close conditions.
