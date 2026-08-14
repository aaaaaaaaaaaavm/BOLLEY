# ADR-037 — why I froze the exact Gen3 CAD gate

- **Date:** 2026-08-14
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A8b selected geometry plus passing A6h and A7c results

## What I decided

I froze A5e on exactly `n27_p45.3_I380_A10.4`. I require the 318.6 mm five-lane cage, 27 cells at
45.3 mm, the nine-cell active window and copper volume for four 10.4 mm2 turns to appear in native
parametric source, STEP/STL masters, renders and exact intersection checks.

## Why I chose it

My retained Gen2 CAD is 900 mm long, four-lane and 30 mm pitch. Stretching its render would hide the
axial and winding changes that made Fluxrelay pass. Gen3 must therefore be a new controlled build,
not a renamed archive.

## What follows

- I allow A5e to reject the selected point on fit, route, traceability or copper-volume grounds.
- A nominal pass opens tolerance, structure and A9 only.
- I keep packaged mass, hardware and provider acceptance open even if every CAD band passes.
