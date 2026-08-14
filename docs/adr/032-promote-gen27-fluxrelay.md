# ADR-032 — promote one Gen2.7 Fluxrelay analytical point

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A8b coupled deterministic design-space result

## Decision

Promote only `n27_p45.3_I380_A10.4` to fresh nonlinear field analysis and selected-point
cage/circuit reclosure. Retain 27 cells per face channel, 45.3 mm pitch, 380 A, 10.4 mm2
conductors, a 318.6 mm five-lane cage and individual cell-sectional excitation.

Do not promote the other 76 feasible analytical candidates, and do not call the selected point a
hardware or field pass.

## Why

A8b is the first package to close the exact contradiction found by A8a while preserving every
A7b energy, cage, CG, voltage and thermal band. It counts all 1.2231 m of primary material against
the 16 kg installed limit but charges only the conservative nine-cell active window with pulse loss.

The selected point minimises its weakest normalized hard-band demand. Reference energy controls at
0.99496, installed primary mass at 0.99426 and the current-scaled stationary-core peak at 0.98965.
That balance is more defensible than choosing the lightest or lowest-energy point independently.

## Consequences

- A6h must replace the current-scaled A6g field surrogate with fresh nonlinear meshes.
- A7c must consume the A6h field and inductance result without refitting A8b's geometry or bands.
- Gen3 CAD may be parameterised from this point for fit inspection, but remains provisional until
  A6h and A7c pass.
- The 0.371 kg spacecraft interface misses both mass preferences while remaining 28.64 g below the
  0.40 kg absolute limit.
- Cell handoff, switching, force ripple, end effects, structure and power electronics remain open.
