# ADR-005: why I promoted a low-profile four-face comb-fin

**Status:** superseded by [ADR-006](006-edge-bound-redesign.md)  
**Date:** 2026-08-13

## What led me here

ADR-004 promoted an opposed through-flux fin only if two-sided stator access could be made inside
a credible CubeSat/dispenser cross-section. A single 15 mm fin would either occupy an awkward
corner return or demand a deep side protrusion.

A5a split that magnetic width into three shallow fins per broad face and moved the four force
lines from the corners to the centres of the four side faces. Fixed slotted stators surround the
fin sides; axial motion requires no opening jaw or following launcher member.

## What I decided

I promoted the **three-fin, four-face comb** as the exact geometry for A3b nonlinear electromagnetic
analysis and a launch-provider/dispenser drawing review.

- Three covered fins per channel.
- 5.0 mm active height and 5.5 mm total projection from the rail plane.
- 1.0 mm covered moving thickness in a 2.0 mm stationary slot.
- 14.0 mm stationary comb footprint per broad face.
- Seven 48 mm pitches over 336 mm active length.
- Four face-centred, independently controlled channels.

I retain mechanically continuous hard-anodized aluminium for the standard corner rails.

## Evidence I used

All 11 A5a executable bands pass against the frozen qualification force and preliminary CDS Rev.
14.1 guidance:

- calculated moving increment: 121.2 g;
- developed area per channel: 100.8 cm²;
- peak force over 441 CG points: 229.07 N;
- required developed shear: 22.73 kPa;
- protrusion from rail plane: 5.50 mm;
- rail-edge-to-comb clearance: 43.0 mm; and
- projected share of usable side-face width: 16.9%.

These are geometry, mass and allocation outputs. They are not force, strength or compatibility
evidence.

## What follows

- The rejected corner L-return does not receive FEA effort.
- A3b must model the 0.25 mm cover and 0.50 mm mechanical gap on both sides, nonlinear steel,
  leakage, axial fringing, normal-force imbalance and the 150 ms current transient.
- A selected provider must confirm that its custom dispenser can supply stator/back-iron volume
  around the 14 mm comb without compromising containment or the contact rails.
- Fin-root capture, vibration, wear and debris containment become explicit structural gates.
- The single-sided aluminium induction lane remains the fallback if electromagnetic or provider
  review fails.
- Passing A5a does not establish novelty. The prior-art search remains open.
