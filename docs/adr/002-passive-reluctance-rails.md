# ADR-002: active stator, passive reluctance rails

**Status:** superseded in part by [ADR-004](004-explicit-flux-path.md)  
**Date:** 2026-08-13

## Context

Once a small payload modification is allowed, the secondary can be conductive, magnetic, wound
or permanently magnetised. The choice decides mass, spacecraft compatibility and launcher
complexity.

## Decision

Use a segmented long-primary reluctance machine with the windings on the launcher and passive
soft-magnetic poles embedded in four spacecraft rails.

## Rejected alternatives

- **Permanent-magnet rails:** synchronous and controllable, but add mass, continuous field and
  magnetic integration risk.
- **Powered payload coils:** remove slip but create electrical connectors, heat and inhibits on a
  spacecraft that should remain powered off in the dispenser.
- **Bare aluminium or copper induction rails:** mechanically simple and magnetically quiet when
  off, but narrow secondaries amplify end effects and deposit slip loss in the payload.
- **Launcher-owned magnetic sled:** already explored by VOLLEY; its mover mass is the problem this
  decision exists to remove.

## Consequences

The passive translator is cheap and unpowered. The costs move into nonlinear commutation,
attractive normal force, covered-gap force density and possible remanence. Those are now the
first kill tests.
