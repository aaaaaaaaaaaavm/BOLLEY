# ADR-003: Phase 0 duty

**Status:** accepted  
**Date:** 2026-08-13

## Decision

Freeze the first design screen at:

- 4 kg reference payload;
- 6 kg qualification sizing payload;
- 8 g nominal longitudinal acceleration;
- 0.90 m powered length;
- 0–12 m/s command range for the reference payload; and
- no more than 2 deg/s/axis release tip-off.

## Why not inherit 16.388 m/s

VOLLEY's 16.388 m/s is a result of its selected force and track, not a customer requirement. The
strong mission case is a commanded velocity differential for same-plane phasing. Twelve metres
per second reaches that regime while shortening the stator, bank pulse and qualification step.

The modular track may grow after the first tile and rail coupon work. Velocity is not increased on
paper to compensate for a force-density failure.

## Consequences

At 8 g over 0.90 m, ideal kinematics give approximately 11.89 m/s independent of mass. The 6 kg
case changes force, channel sizing and energy, not that velocity, until a lower payload acceleration
limit is imposed.

