# ADR-025 — why I froze the five-lane Gen2.6 Quintweb

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7a failure localisation, five-lane mass accounting and non-validation field
  development meshes

## What I decided

I froze five Fluxweb blades per face on a 31 mm R4 stationary return. I used four 20.25 mm2 turns
at 375 A for 1,500 A-turn. I scaled payload capture allowance with blade count and kept the 0.40
kg absolute interface limit unchanged.

I revised only A6g's inductance upper band from 1.05 to 1.40 times A3g before the formal run. The
four-turn topology restores inductance by construction, while A7a demonstrates substantial link
voltage headroom; A7b must still close the actual circuit.

## Why I chose it

A7a's four failures all improve when force per conductive area falls. A fifth blade adds 25%
active area without thickening the proven Fluxweb section. The complete interface is 0.38823 kg,
and the stationary primary remains below 16 kg analytically.

## What follows

- Only 11.77 g remains before the absolute payload mass limit; CAD can reject the candidate.
- A6g repeats the formal worst-mesh field gate before any cage or CAD promotion.
- A field pass must be followed immediately by A7b on all A7a corners and CG points.
