# ADR-058: freeze the A5g path-corrected winding

Date: 2026-08-31

## Context

A5f showed that the A9f twelve-turn wire envelopes can fit nominally, but their fixed A5e inner opening makes the mean turn too long and exceeds the inherited copper-volume band.

The failed quantity is path length. I do not need more copper or a different electrical point to test the obvious correction.

## Decision

Before creating `analysis/gen3_12turn_path_fit.py`, I freeze A5g with the transverse inner opening fixed at 8.8 mm and solve only the inner axial opening required to restore the 118.6 mm A5e mean turn length for each wire candidate.

All A5f electrical inputs, wire-width range, insulation envelope, core, cage, pitch and radial layering remain controlled. The A5e 0.5% copper-volume band and 60% fill band remain unchanged.

## Consequence

A5g can promote one nominal winding path only to detailed BRep CAD and package reclosure. If the required inner axial opening intersects the same-cell or neighbouring core, or if the radial stack no longer fits, the twelve-turn branch is rejected again rather than rescued inside the same run.
