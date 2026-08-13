# ADR-018 — reject the 1.06 mm Gen2.3 magnetic rib

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6d worst-of-three-mesh nonlinear field result

## Decision

Reject the exact 1.06 mm magnetic rib: it improves the controlling peak but still reaches
1.4766 T. Retain the R4 primary, copper rung geometry and stepped-rib concept. Permit the next rib
to cross the earlier 0.30 kg preferred interface mass, provided it remains below the 0.40 kg
absolute limit and the mass preference is recorded as a failure rather than silently removed.

## Consequences

- The interface preference becomes an explicit trade, not an invisible threshold change.
- A wider rib requires another matching stator-slot update and formal worst-mesh solve.
- Gen2.3 CAD and transient work remain blocked.
