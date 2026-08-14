# ADR-032 — why I promoted one Gen2.7 Fluxrelay analytical point

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A8b coupled deterministic design-space result

## What I decided

I promoted only `n27_p45.3_I380_A10.4` to fresh nonlinear field analysis and selected-point
cage/circuit reclosure. I retained 27 cells per face channel, 45.3 mm pitch, 380 A, 10.4 mm2
conductors, a 318.6 mm five-lane cage and individual cell-sectional excitation.

I did not promote the other 76 feasible analytical candidates, and I do not call the selected
point a hardware or field pass.

## Why I chose it

In A8b I found my first package that closed the exact contradiction from A8a while preserving every
A7b energy, cage, CG, voltage and thermal band. I counted all 1.2231 m of primary material against
the 16 kg installed limit but charged only the conservative nine-cell active window with pulse loss.

My selected point minimises its weakest normalized hard-band demand. Reference energy controls at
0.99496, installed primary mass at 0.99426 and the current-scaled stationary-core peak at 0.98965.
I considered that balance more defensible than choosing the lightest or lowest-energy point independently.

## What follows

- I required A6h to replace the current-scaled A6g field surrogate with fresh nonlinear meshes.
- I required A7c to consume the A6h field and inductance result without refitting A8b's geometry or bands.
- I allowed provisional Gen3 CAD fit work from this point, but no promotion before A6h and A7c pass.
- I recorded that my 0.371 kg spacecraft interface misses both mass preferences while remaining
  28.64 g below the 0.40 kg absolute limit.
- I kept cell handoff, switching, force ripple, end effects, structure and power electronics open.
