# ADR-046: freeze the selected Gen3 sectional-drive transient

Date: 2026-08-31

## Decision

I freeze A9 before `analysis/sectional_drive.py` exists.

A9 keeps the exact A8b/A6h/A7c/A5e selected Gen3 point and replaces only A7c's quasi-steady
prebiased active-window assumption with a time-domain sectional circuit/force model. The controlled
geometry, resistance/conductance corners and existing electrical requirements do not move.

The declaration is in [`validation/A9_sectional_drive.md`](../../validation/A9_sectional_drive.md)
and the controlled inputs are in
[`analysis/sectional_drive_parameters.json`](../../analysis/sectional_drive_parameters.json).

## Why this is next

P38, P40, P11 and P39 sit on one dependency chain. A7c leaves 6.588 J below the 900 J reference
energy limit. Before I spend more effort on structure or presentation, I need to know whether finite
current rise, handoff and end transitions consume that margin or demand current, voltage or power
outside the limits already attached to the selected point.

I do not set a new force-ripple percentage. The transient has to survive the existing electrical,
acceleration and exit-state limits instead.

## Consequence

No A9 result exists in this decision. If the later model misses a band, I keep the miss. A passing
model can narrow P38 but cannot close supplier evidence, 3D cage current distribution, packaging,
EMC, structure or hardware validation.
