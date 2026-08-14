# ADR-023 — why I froze the Gen2.5 post-field cage reclosure

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6f passing field result and Gen2.5 copper/mass accounting

## What I decided

I ran A7a with the minimum A6f tooth field, maximum A6f phase inductance, 0.345 mm equivalent cage
copper and the frozen three-turn 400 A primary. I evaluated both payload masses at every declared
CG point over conductance and hot-resistance corners before CAD promotion.

## Why I chose it

The field rescue consumed 8% of cage conductance. That cost belongs in slip, heating, efficiency
and source energy before a polished model can make the design look settled. The 900 J reference
kill criterion controls, not A3g's looser optimisation allowance.

## What follows

- The known 0.25/0.30 kg mass misses remain visible; 0.40 kg remains hard.
- The 16 kg stationary-primary bound supersedes A3g's 12 kg optimisation preference after the R4
  return redesign; the mover itself remains absent.
- A7a remains analytical and cannot substitute for a discrete transient field/circuit solve.
