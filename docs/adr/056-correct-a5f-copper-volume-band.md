# ADR-056: correct the A5f copper metric before execution

Date: 2026-08-31

## Context

ADR-055 froze A5f with the statement that the twelve-turn winding must retain the A5e copper amount. The first A5f run sheet tested 41.6 mm2 of bare copper cross-section per coil side. That is necessary, but it does not test the same quantity as A5e's copper-volume consistency band.

A twelve-turn nested winding can keep 41.6 mm2 of cross-section and still use more copper if its mean turn length grows. A9f assumed the A5e mean-turn geometry while scaling resistance and inductance by turn count. A5f must therefore test conductor path length and total copper volume, not cross-section alone.

No A5f calculator or result exists at this commit.

## Decision

Before writing `analysis/gen3_12turn_winding_fit.py`, I add the inherited 0.5% copper-volume band explicitly.

I retain the frozen 40.1 mm axial and 8.8 mm transverse inner spans for A5f. I do not redesign them inside the same run. The A5e target is 4,933.76 mm3 of copper per cell, equivalent to 41.6 mm2 times the 118.6 mm mean turn length.

I keep the cross-section check as a separate identity and add total detailed-turn copper volume as the physical acceptance quantity.

## Consequence

A5f may now fail even when all twelve conductor envelopes fit. If it fails only on copper volume, I will preserve that result and open a separate winding-path redesign rather than changing A5f geometry after seeing the answer.
