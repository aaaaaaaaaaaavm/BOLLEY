# ADR-014 — why I rejected the exact Gen2.1 geometry but retained Fluxmanifold

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6b three-mesh nonlinear field solution

## What led me here

A6b puts the radius-fed return and copper-neutral turn exchange through 745,030 fine-mesh
triangles. Eleven of thirteen bands pass. Mean field, inductance, bulk-core field, balance,
uniformity and all numerical convergence checks are on the correct side. Only the inferred moving
ligament peak (1.4820 T) and local return-haunch peak (1.5595 T) miss.

## What I decided

I rejected the exact Gen2.1 dimensions, not the Fluxmanifold topology. I preserved the three-turn
winding and passive cage. For Gen2.2, I reduced the 1,280 A-turn endpoint, added return-haunch area,
and retained the A6b field floor and both 1.45/1.55 T limits.

## What follows

- A6b remains a failed result even though both misses are small.
- A passing Gen2.2 must show margin on the fine and expanded meshes, not only nominal base.
- Circuit and CAD closure remain blocked until the correction passes independently.
