# ADR-041: I promote two premise changes, not two machines

- **Date:** 2026-08-28
- **Status:** accepted

## Context

A10 passed the ideal pressure, acceleration, trim-energy and first mass-allocation screens. It also
left sealing deliberately open and used assumed Gen6 interface masses. Gen5 produced only a
required displaced-mass threshold.

## Decision

I promote Gen5 Fluxframe to a bus-specific net-mass gate and Gen6 Fluxpiston to seal, pressure,
structure and trim gates. I do not promote either to CAD or baseline status. Gen4 remains the only
selected machine and must still pass A9 plus packaged-system closure.

## Consequences

- I have a Gen5 target of at least 121.36 g displaced bus mass.
- I carry 30.942 and 33.333 kPa as ideal mean-pressure screens, not chamber specifications.
- I carry 15.188 J as a kinetic trim requirement, not an electrical-store size.
- I reject Strainrail at the current interface mass and retain burn-and-drop outside the mechanism
  generations.
- My next Gen6 gate begins with leakage/contact and pressure transient, not polished CAD.

