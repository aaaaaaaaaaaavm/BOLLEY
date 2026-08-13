# ADR-011: Freeze the robust 30 mm / 0.56 T Gen2 operating point

**Status:** accepted for field FEA and Gen2 CAD—not manufacturing  
**Date:** 2026-08-13

## Context

A3f proved that the Fluxbridge package can pass, but its first 16 mm / 0.62 T point was only 26.9%
source-to-payload efficient. A3g searched 80 pitch/field combinations at eight declared degradation
corners each. Ten candidates survive every band.

## Decision

Freeze the deterministic A3g selection for Gen2:

- 30 mm cell pitch with a 15 mm tooth and 15 mm winding slot;
- 30 cells per face, ten cells per phase and 0.900 m active length;
- 90 mm electrical wavelength;
- 0.56 T equivalent sheet field, 0.792 T tooth field and 1.267 T magnetic-ligament field;
- four turns of 20.25 mm² copper per cell at 60% two-sided gross slot fill; and
- 48 V nominal DC link.

## Evidence

At the nominal input, the qualification shot requires 1.135 kJ and reaches 39.1%
source-to-payload efficiency. At the frozen worst corner—0.25 mm clearance per side, 90% cage
conductance and 150% stationary-core H—it requires 1.333 kJ and remains 33.3% efficient. Active
primary mass is 11.83 kg. All bands remain inside their limits.

## Consequences

- Gen2 becomes 2.46 kg heavier than the first A3f primary but uses 31.3% less nominal
  qualification source energy.
- The larger pitch halves coil count, widens the real winding slot and reduces terminal frequency.
- CAD must route two four-turn coil sides through each 15 × 18 mm slot at or below 60% gross fill.
- Field analysis must use 30 mm periodicity and the discrete 2 mm copper-bar cage; it may not reuse
  the A3f homogenized field as proof.
- This decision is automatically superseded if Gen2 CAD or field FEA fails its own frozen bands.
