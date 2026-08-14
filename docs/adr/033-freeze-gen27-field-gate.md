# ADR-033 — why I froze the selected Gen2.7 field gate

- **Date:** 2026-08-14
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A8b selected Fluxrelay point and A6g common field method

## What I decided

I froze A6h on exactly `n27_p45.3_I380_A10.4`: the retained five-lane transverse section at 380 A,
1,520 A-turn and 22.65 mm physical tooth depth. I replaced the inherited per-cell/A3g inductance
band with a +/-15% agreement band around A8b's 4.95297 uH three-cell phase-window surrogate.

I kept every physical field, peak, balance, mesh, boundary, source and nonlinear-closure limit from
A6g unchanged.

## Why I chose it

I scaled A8b's field peaks linearly from 375 A, but my selected point has only 1.04% surrogate
stationary-core margin. Its 45.3 mm pitch also changes cell coenergy and inductance through a
22.65 mm tooth depth. If I reused A6g, I would avoid both quantities that most directly threaten
my selection.

I energize three cells per phase, so I compare phase-window inductance—not one cell relative to my
old 30 mm A3g geometry.

## What follows

- I allowed A6h to reject the A8b point without reopening my 2,856-candidate search.
- I still require A7c to consume the solved field and inductance after any A6h pass.
- I allow only provisional Gen3 geometry after A6h; its installed-system mass can still make me
  reject the topology.
