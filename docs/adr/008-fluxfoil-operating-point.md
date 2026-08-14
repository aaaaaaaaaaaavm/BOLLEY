# ADR-008: why I raised Fluxfoil field instead of relaxing efficiency

**Status:** accepted for explicit stator/circuit entry  
**Date:** 2026-08-13

## What led me here

A3c's 0.50 T thin-sheet model passed every geometry, mass, slip, reaction, current-density,
heating, skin-depth, frequency, power and normal-balance band. It failed the predeclared 70%
secondary-only shot-efficiency gate at the worst CG point, returning 66.2%.

## What I decided

I preserved the A3c result and screened a 0.60 T RMS travelling-field point as A3d. I changed no
payload-side dimension, material or acceptance band.

## What follows

- The change is entirely launcher-side.
- Slip heat should fall, but normal preload and magnetizing demand rise.
- A3d may advance only if it clears the original 70% band and every original A3c band.
- Further field increases above 0.60 T are not an allowed repair. A failure triggers geometric or
  topological redesign.

A3d subsequently passed all 19 frozen bands. The result promotes the operating point, not the
assumed field source: A3e must now close an explicit magnetic circuit, winding and pulse model.
