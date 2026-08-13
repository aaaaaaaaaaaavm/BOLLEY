# ADR-001: accept a cooperative payload interface

**Status:** accepted  
**Date:** 2026-08-13

## Context

VOLLEY's 4 kg reference payload rides a 9.445 kg sled. Only 29.8% of the moving mass is the
customer spacecraft. The sled creates the brake, return, magnetic-dwell, bank, packaging and
host-attitude problems that dominate the current system.

Preserving an entirely unmodified spacecraft is valuable, but it is not free.

## Decision

Bolley may add a passive, launcher-specific rail interface to the spacecraft. The Phase 0 target
is no more than 0.25 kg and the hard limit is 0.40 kg.

No spacecraft power, permanent magnet, pressure system, pyrotechnic or launch-time software is
accepted as part of this decision.

## Consequences

- Almost all moving kinetic energy belongs to the delivered spacecraft.
- There is no launcher mover to arrest or return.
- Tip-off can be controlled through distributed force rather than a single pusher.
- The product no longer fits every CubeSat without cooperation.
- Hybrid rails require structural, magnetic and provider qualification.
- An unmodified-payload mode remains a separate fallback, not a hidden requirement on this design.

