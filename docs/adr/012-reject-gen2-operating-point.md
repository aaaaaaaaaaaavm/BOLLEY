# ADR-012 — reject the A3g Gen2 operating point after independent field solution

- **Date:** 2026-08-13
- **Status:** Accepted
- **Deciders:** Adityavardhan Mishra
- **Evidence:** A6 independently meshed 2D nonlinear transverse-field solution

## Context

A3g selected `p30_B0.56` with a lumped MMF, saturation and inductance model. A5d proved that the
associated winding and passive interface fit in nominal CAD. Neither result established that the
actual four-slot cross-section produced the target field or that its return iron remained inside
the declared screening curve.

A6 solved the transverse section on base, fine and expanded-boundary meshes. Numerical
convergence, field uniformity and four-slot flux balance pass. The fine mean field is only
0.6568 T, stationary-core peak is 3.2346 T and per-cell inductance is 1.3945 times A3g. These fail
three bands written before execution.

## Decision

Reject A3g `p30_B0.56` as the Gen2 operating point. Preserve A3g and A5d as optimisation and
packaging evidence, but do not use their drive, source-energy or thermal results as current
baseline values.

Retain the passive Fluxbridge cage and the A5d envelope as the starting point for Gen2.1. Redesign
the stationary return path first; do not attempt to recover field by current alone while the core
is already above its limit. Rerun independent field and circuit closure before transient cage
force, tip-off or thermal campaign work.

## Consequences

- Gen2 nominal CAD is a fit-controlled historical baseline, not a performance-qualified design.
- The four-blade Fluxbridge principle remains active because balance, uniformity and ligament
  field pass.
- Any Gen2.1 optimisation must include field-solver outputs rather than a lumped field target
  alone.
- A3g source-energy and inductance numbers are superseded for hardware sizing.
