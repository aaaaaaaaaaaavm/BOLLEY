# ADR-021 — why I froze the Gen2.5 layered Fluxweb

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6e local-peak diagnosis, geometric mass/conductance accounting and non-validation
  development meshes

## What I decided

I replaced the uniformly perforated passive rib with a layered 1.12 mm Fluxweb. I preserved 0.20
mm of magnetic material beneath each 0.92 mm copper rung while retaining full magnetic width
between rungs. I used a 1.58 mm matching stator slot and returned to 1,200 A-turn at three turns.

## Why I chose it

A6e showed that uniform width buys poor local-peak margin. Fluxweb spends material on axial
magnetic continuity instead: effective magnetic duty rises from 62.5% to 69.2%, while cage sheet
conductance falls only 8%. The complete interface is 0.31059 kg, only 1.98 g above Gen2.4 and still
89.41 g below the absolute mass limit.

## What follows

- The 0.30 kg interface preference remains failed; it is not redefined.
- A6f must pass the unchanged worst-of-three-mesh magnetic gate.
- A field pass is conditional on a new transient cage/thermal screen for the 8% conductance loss.
- The layered joint and discrete axial geometry require new CAD and eventual coupon manufacture.
