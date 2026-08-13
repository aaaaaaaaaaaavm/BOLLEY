# ADR-006: Reject three fins; screen a taller four-fin comb

**Status:** accepted for A3b1 stator-topology screening  
**Date:** 2026-08-13

## Context

ADR-005 promoted the A5a three-fin comb because its interface envelope, moving mass and
four-channel allocation passed. A5a also reported 22.73 kPa by dividing peak channel force by the
two long faces of every fin.

A3b0 corrected the physical interpretation before FEA. In a tooth-overlap switched-reluctance
machine, axial force follows the energy gradient at active overlap edges. The ideal two-gap bound
for the exact three-fin geometry is 250.67 N at 2.0 T, below the frozen 255 N gate. It needs 2.017 T
even with zero steel reluctance and no leakage, fringing, end effect or current limit.

## Decision

Reject the exact three-fin comb before nonlinear FEA. Preserve A5a as an interface result, but do
not use its whole-face developed-shear statistic as an axial force prediction.

Screen one minimal cooperative-payload change in A5b:

- four aligned fins per face instead of three;
- 6.0 mm active height instead of 5.0 mm;
- 0.25 mm radial tip cover, giving 6.25 mm nominal projection;
- unchanged 0.25 mm side covers and 0.50 mm side clearances; and
- aligned moving teeth, with continuous electrical phasing assigned to launcher-side stators.

The redesign is called the **Bolley quad-comb**. A5b subsequently passed all 15 frozen bands, so
the geometry advances to A3b1. That promotion applies to the passive moving interface only; the
2 mm stationary web sketch has not yet proved it can carry the required flux.

## Consequences

- ADR-005 is superseded as an electromagnetic-model-entry decision.
- The CubeSat modification grows slightly, but remains passive and face-centred.
- No current, voltage or thermal optimism is used to repair a geometry shortfall.
- A5b must preserve the rail keep-outs, 25% face-width limit, 0.25 kg preferred mass and a nominal
  protrusion reserve while clearing the ideal force bound at the material anchor.
- A5b success earns only a nonlinear 3D model with an explicit C/U-core return path and winding
  window. It does not validate the machine.
- If A5b fails, the next decision is between a five-fin interface, a smaller effective gap and the
  single-sided induction fallback—not a relaxed force threshold.
