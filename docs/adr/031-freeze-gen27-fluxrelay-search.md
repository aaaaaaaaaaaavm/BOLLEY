# ADR-031 — why I froze the Gen2.7 Fluxrelay co-design search

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7b hot-resistance localisation and A8a axial-package rejection

## What I decided

I searched an aft-shortened five-lane cage against a complete three-phase stator lattice with
cell-sectional excitation. I required symmetric 2.25 mm engagement guards, full 900 mm travel and
the unchanged 16 kg installed-primary / 0.40 kg interface limits.

I selected by the weakest continuous hard-band margin, not minimum energy or mass alone.

## Why I chose it

In A8a I found that sectional switching can close the A7b resistance diagnostic, but my naive
full-overlap extension reached 22.2 kg. I could reduce required primary length and payload mass by
shortening only the forward end of the passive cage, reduce installed cell count and active
frequency by widening pitch, and trade current-density margin for installed mass by reducing
conductor area. I had to evaluate those three changes together because each could break a
different frozen band.

## What follows

- I allowed A8b to promote only one selected analytical point, never the whole Fluxrelay family.
- I required a fresh nonlinear field solve because current could differ from A6g.
- I kept Gen3 CAD blocked until both field and selected-point cage/circuit reclosure pass.
