# ADR-030 — why I rejected the as-drawn Gen2.6 axial package

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A8a exact overlap and current-limited kinematic audit

## What I decided

I rejected the 900 mm stator / 336 mm cage package as the geometry behind a 900 mm constant-force
shot. I preserved the five-lane transverse-field evidence and sectional-excitation correction.

## Why I chose it

I found that the cage reaches zero overlap before the commanded travel ends. It produces only
0.72975 m of full-force-equivalent work and 10.702 m/s at 375 A. I could not reach my 11.8 m/s
band with either 400 A or the best axial placement.

I found 22.199 kg at the first complete three-phase cell count for a full-overlap extension, so I
could not simply make Gen2.6 longer without failing my 16 kg primary bound. In contrast, by
energising only intersected cells or tiles I reduce A7b phase resistance enough to close its
isolated hot-energy diagnostic.

## What follows

- I kept P36 open, but moved it from implicit to modelled.
- I blocked Gen3 CAD on a shorter, aft-positioned active cage and sectional-stator co-design.
- I required A8b to search installed mass and overlap together rather than optimise source energy alone.
- I retained my earlier A7a/A7b results as conservative circuit evidence, not full-stroke validation.
