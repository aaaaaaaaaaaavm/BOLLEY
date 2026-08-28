# Provenance and evidence boundary

I publish Bolley as an authored engineering record. This page states what actually supports it.

## Current evidence

- The algebraic and dynamic screens are model outputs from controlled Python inputs.
- A6 through A6h are nonlinear two-dimensional field solutions on declared meshes. They are FEA,
  but they are still simulations and do not replace a measured field or force map.
- A5c, A5d and A5e are parametric CAD and exact nominal intersection checks. They do not contain a
  complete tolerance, structural, thermal or manufacturing definition.
- A7c is a circuit and energy model. It contains no selected supplier bridge, measured winding
  resistance, switching waveform or EMC test; A9 handoff and fault work remains open.
- A10 through A12 are retained architecture explorations. Their results remain evidence about
  those declared models, not validation of Fluxframe or Fluxpiston hardware.

## Independent checks that exist

I retain separate analytical and nonlinear-field paths where the repository actually has them,
including A6h field closure against the earlier circuit surrogate and A7c's circuit reclosure on
the solved inductance. These are internal model-to-model checks. P25 and P29 remain open precisely
because the selected cage still lacks an independent transient three-dimensional field solution.

## What does not exist

I have not built, fired, measured, qualified or flown Bolley. I have no supplier quotation,
launch-provider acceptance, bus-vendor acceptance, environmental qualification, wear campaign,
force coupon, thermal-vacuum result or independent third-party review.

## Corrections remain visible

The repository retains failed magnetic returns, the Gen1 winding-window collision, the axial
engagement contradiction, repeated local-saturation failures and the rejected single-inlet
Fluxpiston control family. I use [`HISTORY.md`](../HISTORY.md), [`DECISION_LOG.md`](../DECISION_LOG.md)
and the validation sheets as the correction record rather than presenting the latest design as
the first design.

## Honest citation

Any citation or presentation should call Bolley a model-only design study and should identify the
specific commit or release used. The current citation metadata is in [`CITATION.cff`](../CITATION.cff).
