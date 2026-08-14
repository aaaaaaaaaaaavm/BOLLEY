# ADR-018 — why I rejected the 1.06 mm Gen2.3 magnetic rib

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6d worst-of-three-mesh nonlinear field result

## What I decided

I rejected the exact 1.06 mm magnetic rib: it improved the controlling peak but still reached
1.4766 T. I retained the R4 primary, copper rung geometry and stepped-rib concept. I permitted the
next rib to cross the earlier 0.30 kg preferred interface mass, provided it remained below the
0.40 kg absolute limit and I recorded the mass preference as a failure rather than silently
removing it.

## What follows

- The interface preference becomes an explicit trade, not an invisible threshold change.
- A wider rib requires another matching stator-slot update and formal worst-mesh solve.
- Gen2.3 CAD and transient work remain blocked.
