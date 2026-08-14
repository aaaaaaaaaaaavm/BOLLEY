# ADR-034 — why I promoted the selected Fluxrelay field point

- **Date:** 2026-08-14
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6h worst-of-three-mesh nonlinear field result

## What I decided

I accepted A6h's 13/13 result for exactly `n27_p45.3_I380_A10.4`. I promoted that point to A7c
selected-point cage/circuit reclosure and provisional Gen3 CAD. I did not reopen or refit the A8b
search after seeing the field answer.

## Why I chose it

The three fresh meshes return 0.75503–0.75764 T mean field. Worst moving magnetic material is
1.34336 T and worst stationary core is 1.52843 T. The fine three-cell phase-window inductance is
4.81156 uH, 2.86% below my A8b surrogate and inside the frozen agreement band. Every field,
balance, convergence, boundary, source and nonlinear-closure band passes.

## What follows

- I require A7c to consume 4.81156 uH and the fresh A6h field extrema without changing the selected
  geometry, operating point or energy bands.
- I close P37 because A6h met its predeclared close condition.
- I allow provisional Gen3 CAD, but its packaged mass, tolerances and discrete geometry can still
  reject Fluxrelay.
- I do not treat this 2D RMS-equivalent solve as force, axial-end, switching, structural, thermal
  hardware or release evidence.
