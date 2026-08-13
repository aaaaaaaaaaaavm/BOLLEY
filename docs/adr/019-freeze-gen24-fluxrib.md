# ADR-019 — freeze the Gen2.4 bounded-mass Fluxrib

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6d failure localisation, geometric mass accounting and two non-validation
  development meshes

## Decision

Freeze 1.14 mm active magnetic ribs, unchanged 1.00 mm copper rungs, 1.20 mm finished rib width
and 1.60 mm matching stator slots. Reduce the three-turn primary point slightly to 1,190 A-turn.
Accept an 8.60 g miss against the 0.30 kg interface preference while retaining the 0.40 kg
absolute limit unchanged.

## Why

This is a bounded payload-side purchase: 9.49 g more magnetic matrix than Gen2.3 buys peak-flux
margin at the exact remaining failure, while the 10 A-turn reduction protects the core and the
field floor. No copper rung, payload power, launcher footprint or electronics change is added.

## Consequences

- The interface preference remains a recorded failure even if the magnetic gate passes.
- A6e must pass the unchanged worst-of-three-mesh field gate before any promotion.
- A pass requires a new stepped-rib CAD package, circuit closure and transient force evidence.
