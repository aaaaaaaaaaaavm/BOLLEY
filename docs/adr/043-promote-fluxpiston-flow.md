# ADR-043: I promote Fluxpiston gas quantity, not seal physics

- **Date:** 2026-08-28
- **Status:** accepted

## Context

A11 passed all eight executable frozen bands across 30 clearance/temperature points. The worst
declared point uses 6.009 g nitrogen per shot, while the ideal campaign store is 3.531 L at 20 bar
and 330 K before tank and regulator allowances.

## Decision

I retain the full-face pressure architecture and open a dynamic regulator/chamber/blowdown gate. I
also require contact, lateral leakage-force, rarefied-flow and exit-plume work. I do not select a
seal and I do not open Gen6 CAD.

## Consequences

- Gas quantity no longer kills Gen6 at first order.
- The 0.50 mm non-contact gap remains a flow-area control, not a manufacturing choice.
- The short trim section carries at most 14.8125 J of payload kinetic correction in A11.
- Pressure-control response and the 5.57% reference headroom become the next numerical risks.
- Band 9 remains OPEN until a physical model and representative test exist.

