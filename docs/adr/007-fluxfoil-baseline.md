# ADR-007: Promote passive aluminium Fluxfoil to the Gen1 lane

**Status:** superseded at 0.50 T by [ADR-008](008-fluxfoil-operating-point.md)  
**Date:** 2026-08-13

## Context

The cooperative payload premise remains valuable, but two distinct reluctance geometries have now
failed for different physical reasons:

1. A3b0 rejected the three-fin moving comb because 21 tooth edges miss 255 N even at an ideal
   2.0 T gap field.
2. A5b recovered ideal edge margin with four taller fins, but A3b1 found the conventional shared
   stationary return impossible as drawn: 4.78 T outer and 9.57 T interior pole throats.

The single-sided aluminium induction lane was retained by A3a specifically for this branch point.
Its missing moving flux return is a feature rather than an ambiguity: induced currents react
directly against a launcher-generated travelling field.

## Decision

Promote **Fluxfoil** to the Gen1 analytical lane:

- four continuous 6 mm aluminium fins on each broad face;
- symmetric launcher stators on both sides of every fin;
- 48 mm travelling-field wavelength with frequency chirped to payload velocity;
- four independently controlled face channels for force-centroid placement; and
- no steel, permanent magnets, windings, power or launch-time electronics on the spacecraft.

The former quad-comb envelope is deliberately reused. The moving segmented steel is replaced by
continuous aluminium, so the cooperative hardware becomes lighter and its remanence problem is
removed.

## Consequences

- The shared-pole reluctance stator does not receive nonlinear FEA or winding design.
- A3c must first close thin-sheet slip, reaction, current density, heating, frequency, normal-force
  mismatch and shot-energy screens.
- If A3c passes, the next design must produce its assumed field with an explicit core, winding and
  inverter. A thin-sheet pass is not allowed to become the README headline by itself.
- Fin root capture, provider acceptance and repeated wear remain common mechanical gates.
- The passive-aluminium interface substantially reduces static magnetic-compatibility risk, but a
  powered transient survey is still required.
- This decision makes no novelty or patentability claim.
