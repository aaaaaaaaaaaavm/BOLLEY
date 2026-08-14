# ADR-010: why I rejected the Gen1 winding and screened a passive Fluxbridge cage

**Status:** A3f model passed; accepted for optimisation, field FEA and Gen2 CAD—not hardware  
**Date:** 2026-08-13

## What led me here

A3e was electrically self-consistent but physically incomplete. A5c showed that its coil envelope
intersects the moving interface by 3,987.375 mm³ on every face. The analytical 20-turn winding also
asks a 0.5 × 12 mm inter-cell window to carry 400 mm² of bare copper before insulation.

The mismatch is not repaired by moving a coil in a render. The 8 mm series low-permeability path
that created the 3,945 A-turn requirement must be reduced first.

## What I decided

1. I rejected the A3e winding package and superseded ADR-009 for CAD promotion.
2. I preserved A3e and A5c as evidence; I did not delete or rewrite their passed bands.
3. I screened a passive Fluxbridge cage as A3f.
4. I kept all power, switching and control on the launcher.
5. I treated the extra passive spacecraft mass and non-standard interface as explicit costs.

The Fluxbridge blade is a 1 mm perforated amorphous magnetic matrix containing shorted copper rungs
and end buses. It is the linear analogue of a passive squirrel cage compressed into the existing
four-fin interface. The magnetic ligament lowers reluctance; the copper ladder provides induced
current; four faces preserve force-centroid control.

## What follows

- There are no permanent magnets, coils, batteries, commands or connectors on the CubeSat.
- Magnetic-interface mass, remanence, debris, structural capture and magnetometer compatibility
  become payload-side qualification items.
- The 0.20 mm nominal running gap is aggressive and must fail later if the complete tolerance stack
  cannot hold it.
- A targeted search found adjacent spring ejection, linear-motor launch and electromagnetic
  mechanisms, but it is not a professional patent search and no legal novelty claim is made.
- A3f must pass its frozen winding-window and energy bands before any Gen2 render is promoted.

## A3f result

A3f passed all 23 declared bands. The interface increment is 0.285 kg, the active primary is
9.37 kg, the winding slot is 58.3% full, and the reference/qualification shots require
1.126/1.651 kJ. The first passing point is only 26.9% source-to-payload efficient, so promotion
means optimisation and independent field closure—not freezing this operating point.
