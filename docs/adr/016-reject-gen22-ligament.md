# ADR-016 — why I rejected Gen2.2 on the remaining moving-ligament peak

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6c worst-of-three-mesh nonlinear field result

## What I decided

I rejected Gen2.2 despite 12/13 passing bands. I retained its 1,200 A-turn three-turn primary and
R4 Fluxmanifold because the stationary return was now comfortably inside its limit. I did not
reduce MMF again because the worst mean field was only 2.39% above its floor.

I moved the next correction to the cooperative payload interface. I thickened only the magnetic
ribs, retained copper rung width and conductance, and widened the stationary slots by the same
amount so I did not spend nominal side clearance.

## What follows

- The next design pays a few grams on the payload instead of adding launcher mass or current.
- The passive change needs new CAD, mass, structural and transient-cage checks even if field passes.
- A6c remains failed; no threshold changes.
