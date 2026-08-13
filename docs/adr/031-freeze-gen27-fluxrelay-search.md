# ADR-031 — freeze the Gen2.7 Fluxrelay co-design search

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7b hot-resistance localisation and A8a axial-package rejection

## Decision

Search an aft-shortened five-lane cage against a complete three-phase stator lattice with
cell-sectional excitation. Require symmetric 2.25 mm engagement guards, full 900 mm travel and the
unchanged 16 kg installed-primary / 0.40 kg interface limits.

Select by the weakest continuous hard-band margin, not minimum energy or mass alone.

## Why

A8a showed that sectional switching can close the A7b resistance diagnostic, but a naive
full-overlap extension reaches 22.2 kg. Shortening only the forward end of the passive cage reduces
required primary length and payload mass. Widening pitch reduces installed cell count and active
frequency. Reducing conductor area spends current-density margin on installed mass. These three
changes must be evaluated together because each can break a different frozen band.

## Consequences

- A8b may promote only a selected analytical point, never the whole Fluxrelay family.
- A fresh nonlinear field solve is mandatory because current may differ from A6g.
- Gen3 CAD remains blocked until field and selected-point cage/circuit reclosure both pass.
