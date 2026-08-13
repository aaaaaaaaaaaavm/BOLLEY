# ADR-004: Explicit moving flux path

**Status:** accepted at analytical-model level  
**Date:** 2026-08-13

## Context

A1 treated 0.50 mm of magnetic-equivalent material spread over the active faces as a mass
placeholder. That arithmetic never said how flux returned through the moving payload interface.
Building nonlinear FEA around that ambiguity would optimize a cross-section that had not earned
the right to exist.

A3a therefore compared an L-shaped corner return, an opposed through-flux fin/tab, and a
single-sided aluminium induction lane using the already-frozen A2 channel load and mass gates.

## Decision

- Reject the 50%-duty corner L-return **as configured**. It is no longer Bolley's primary
  electromagnetic topology.
- Promote the opposed through-flux steel fin/tab to a dimensioned CubeSat/dispenser cross-section
  fit check before nonlinear electromagnetic work.
- Retain the single-sided aluminium induction lane as the fallback if two-sided stator access
  cannot be made mechanically legal.
- Keep the A1 0.229 kg result frozen for traceability, but label it as an equivalent-thickness
  placeholder rather than a designed rail mass.

Neither surviving candidate becomes the baseline until its unresolved gate is closed.

## Evidence

At the A2 load, the 50%-duty corner tooth faces require an optimistic equal-component
Maxwell-stress field of 0.251 T. The L-return can carry only 0.126 T inside the 0.25 kg preferred
gate and 0.243 T inside the 0.40 kg hard gate under the declared 1.60 T core screen. The hard gate
is already below the ideal lower bound before leakage, saturation, cover gap and fringing.

The opposed fin screens at 0.114 kg and the induction lane at 0.184 kg including the same 75 g
non-active allowance. Both retain 100.8 cm² developed air-gap area per channel. These are mass and
geometry outputs, not force predictions.

## Consequences

- The next critical task is A5a: prove that stators can access both sides of the fin/tab while the
  spacecraft remains a valid 3U mechanical interface.
- If A5a passes, the fin/tab becomes the A3 nonlinear-FEA candidate.
- If A5a fails, the induction lane becomes the primary transient force/loss model.
- Four-channel force-centroid control survives because both candidates retain four independently
  addressable longitudinal force lanes.
- No claim of novelty, validation, low recurring cost or flight compatibility follows from this
  decision.

