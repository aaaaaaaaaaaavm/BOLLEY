# ADR-013 — freeze the Gen2.1 Fluxmanifold field candidate

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6 rejection plus explicitly non-validation development sweeps

## Context

A6 rejects Gen2 on low mean field, a saturated sharp-corner return and higher-than-modelled
inductance. Its passing slot-balance, uniformity and moving-ligament bands show that replacing the
passive cage would attack the wrong part of the design.

## Decision

Freeze **Fluxmanifold** for the next formal field gate: a 28 mm stationary face, 7.3 mm outer
legs, 7 mm back yoke and 3 mm circular return haunch feeding the same four passive cage blades.
Spread blade pitch to 4 mm while keeping the payload-side projection unchanged.

Use a copper-neutral turn exchange: three 27 mm² turns at 1,280 A-turn instead of four 20.25 mm²
turns. This preserves 81 mm² slot copper and nearly preserves A3g current density while reducing
the ideal inductive-voltage burden.

## Consequences

- Stationary primary mass rises from 11.829 to an analytical 15.733 kg; moving interface mass does
  not rise.
- A6b must pass the same field, ligament and stationary-core limits on three formal meshes.
- A passing field does not pass the winding, drive, structure, tolerance or transient force.
- The name Fluxmanifold describes this geometry inside Bolley; it is not a novelty or patent claim.
