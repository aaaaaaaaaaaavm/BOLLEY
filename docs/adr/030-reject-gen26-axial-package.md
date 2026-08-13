# ADR-030 — reject the as-drawn Gen2.6 axial package

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A8a exact overlap and current-limited kinematic audit

## Decision

Reject the 900 mm stator / 336 mm cage package as the geometry behind a 900 mm constant-force
shot. Preserve the five-lane transverse field evidence and sectional-excitation correction.

## Why

The cage reaches zero overlap before the commanded travel ends. It produces only 0.72975 m of
full-force-equivalent work and 10.702 m/s at 375 A. Neither 400 A nor the best axial placement
reaches the 11.8 m/s band.

A full-overlap extension reaches 22.199 kg at the first complete three-phase cell count, so simply
making Gen2.6 longer fails the 16 kg primary bound. In contrast, energising only intersected cells
or tiles reduces A7b phase resistance enough to close its isolated hot-energy diagnostic.

## Consequences

- P36 remains open and is now modelled rather than implicit.
- Gen3 CAD is blocked on a shorter, aft-positioned active cage and sectional stator co-design.
- A8b must search installed mass and overlap together; it cannot optimise source energy alone.
- Earlier A7a/A7b results remain conservative circuit evidence, not full-stroke validation.
