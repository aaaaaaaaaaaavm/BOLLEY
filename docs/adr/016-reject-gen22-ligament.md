# ADR-016 — reject Gen2.2 on the remaining moving-ligament peak

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6c worst-of-three-mesh nonlinear field result

## Decision

Reject Gen2.2 despite 12/13 passing bands. Retain its 1,200 A-turn three-turn primary and R4
Fluxmanifold: the stationary return is now comfortably inside its limit. Do not reduce MMF again,
because the worst mean field is only 2.39% above its floor.

Move the next correction to the cooperative payload interface. Thicken only the magnetic ribs;
retain copper rung width and conductance. Widen the stationary slots by the same amount so nominal
side clearance is not spent.

## Consequences

- The next design pays a few grams on the payload instead of adding launcher mass or current.
- The passive change needs new CAD, mass, structural and transient-cage checks even if field passes.
- A6c remains failed; no threshold changes.
