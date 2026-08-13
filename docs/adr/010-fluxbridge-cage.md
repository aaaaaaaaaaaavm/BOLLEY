# ADR-010: Reject the Gen1 winding and screen a passive Fluxbridge cage

**Status:** accepted for A3f screening; not accepted for hardware  
**Date:** 2026-08-13

## Context

A3e was electrically self-consistent but physically incomplete. A5c showed that its coil envelope
intersects the moving interface by 3,987.375 mm³ on every face. The analytical 20-turn winding also
asks a 0.5 × 12 mm inter-cell window to carry 400 mm² of bare copper before insulation.

The mismatch is not repaired by moving a coil in a render. The 8 mm series low-permeability path
that created the 3,945 A-turn requirement must be reduced first.

## Decision

1. Reject the A3e winding package and supersede ADR-009 for CAD promotion.
2. Preserve A3e and A5c as evidence; do not delete or rewrite their passed bands.
3. Screen a passive Fluxbridge cage as A3f.
4. Keep all power, switching and control on the launcher.
5. Treat the extra passive spacecraft mass and non-standard interface as explicit costs.

The Fluxbridge blade is a 1 mm perforated amorphous magnetic matrix containing shorted copper rungs
and end buses. It is the linear analogue of a passive squirrel cage compressed into the existing
four-fin interface. The magnetic ligament lowers reluctance; the copper ladder provides induced
current; four faces preserve force-centroid control.

## Consequences

- There are no permanent magnets, coils, batteries, commands or connectors on the CubeSat.
- Magnetic-interface mass, remanence, debris, structural capture and magnetometer compatibility
  become payload-side qualification items.
- The 0.20 mm nominal running gap is aggressive and must fail later if the complete tolerance stack
  cannot hold it.
- A targeted search found adjacent spring ejection, linear-motor launch and electromagnetic
  mechanisms, but it is not a professional patent search and no legal novelty claim is made.
- A3f must pass its frozen winding-window and energy bands before any Gen2 render is promoted.
