# ADR-009: Build Gen1 around the serpentine series-flux stator

**Status:** accepted for Gen1 CAD and field-FEA entry  
**Date:** 2026-08-13

## Context

A3d proved only that the passive aluminium interface survives an assumed 0.60 T travelling field.
A3e put an explicit magnetic loop, winding and pulse circuit behind that input. Its transverse
flux path crosses all four foil slots in series and returns through only two widened outer legs,
so no interior web must turn the sum of two fin fluxes.

## Decision

Freeze the A3e serpentine stator as Bolley Gen1:

- four independently driven face channels;
- three axial phases over a 48 mm wavelength;
- nineteen 16 mm cells in series per phase and 0.912 m active length;
- a 20 mm transverse slot/core footprint;
- 20 turns per cell in 20 mm² copper;
- 0.60 T RMS in the foil slots and 1.20 T RMS in the return legs/yoke; and
- a 120 V nominal DC link.

## Evidence

All 15 A3e lumped-model bands pass over 441 CG points for both frozen payload cases:

- 40.96 kg active electromagnetic mass: 36.77 kg copper and 4.19 kg electrical steel;
- 3945 A-turn and 197.2 A RMS at the rated point;
- 106.6 V maximum model-required DC link;
- 821.4 J and 7.52 kW worst reference-shot source draw;
- 1209.8 J and 11.08 kW worst qualification-shot source draw; and
- 36.4% modelled source-to-payload efficiency.

## Consequences

- The source energy is materially below VOLLEY's current 2.85 kJ gross shot, but the comparison
  is not yet like-for-like: Bolley excludes housing, control and DC-link losses that do not yet
  have hardware behind them.
- CAD must preserve the four-slot series flux path, 20 mm face footprint, 0.50 mm per-side foil
  clearance and 0.912 m three-phase length.
- Finite-element field closure is still critical. Leakage or end effects can erase the result.
- A 1.15 kN symmetric normal load per stator side becomes a structural design load even though its
  ideal net on each fin is zero.
- The 40.96 kg result is an active-material estimate, not launcher dry mass.
