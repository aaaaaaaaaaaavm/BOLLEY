# ADR-029 — audit the axial machine before Gen3 CAD

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7b failure localisation and Gen2 controlled axial dimensions

## Decision

Freeze A8a on the exact 900 mm stator and 336 mm cage intervals before changing the winding or
starting Gen3 CAD. Evaluate current-limited force as overlap disappears and separately test the
installed mass of a full-overlap extension.

## Why

The post-field shot model holds full cage area for 900 mm. The CAD places a finite 336 mm cage
inside a finite 900 mm stator. Those statements can both be true only if the axial intervals and
sectional commutation prove it.

A7b also charges all ten cells per phase while the concept says only overlapped tiles are
energised. A8a must quantify that correction without allowing an electrical improvement to hide a
stroke-length failure.

## Consequences

- A8a can reject the as-drawn package without reopening the A6g transverse field pass.
- A sectional resistance pass does not promote a longer or heavier primary.
- The next candidate must close axial engagement, installed mass and A7b energy together.
