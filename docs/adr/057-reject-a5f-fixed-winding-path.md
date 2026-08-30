# ADR-057: reject the A5f fixed winding path

Date: 2026-08-31

## Context

A5f tested the A9f 12-turn point inside A5e's fixed 40.1 x 8.8 mm inner coil opening. The individual insulated turns can fit nominally, but their nested centreline paths are longer than A5e's homogeneous 118.6 mm mean-turn model.

The best geometry-feasible copper-volume point is still 4.3851175613739635% above the A5e per-cell copper volume. The unchanged band permits 0.5%.

## Decision

I reject the fixed-inner-span twelve-turn winding. I preserve A9f as an electrical selection only and keep the 4-turn Gen3 winding as the controlled CAD baseline.

I will next test a path-length correction that keeps the 8.8 mm transverse opening and solves the inner axial opening required to restore the 118.6 mm mean turn length for each candidate wire envelope. That is a new geometry question and needs a new declaration before its calculator exists.

## Consequence

A5f's failure remains evidence. I do not widen the copper-volume band and I do not add the extra copper to A9f after the fact. Any path-length-corrected winding must independently pass nominal core, neighbouring-cell, radial-clearance and slot-fill checks before I build detailed CAD.
