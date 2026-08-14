# ADR-029 — why I audited the axial machine before Gen3 CAD

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7b failure localisation and Gen2 controlled axial dimensions

## What I decided

I froze A8a on the exact 900 mm stator and 336 mm cage intervals before changing the winding or
starting Gen3 CAD. I evaluated current-limited force as overlap disappeared and separately tested
the installed mass of a full-overlap extension.

## Why I chose it

In my post-field shot model I held full cage area for 900 mm, while in CAD I placed a finite 336
mm cage inside a finite 900 mm stator. I could reconcile those statements only by explicitly
solving the axial intervals and sectional commutation.

I also charged all ten cells per phase in A7b while stating that I would energise only overlapped
tiles. I used A8a to quantify that correction without letting an electrical improvement hide a
stroke-length failure.

## What follows

- I allowed A8a to reject the as-drawn package without reopening my A6g transverse-field pass.
- I did not let a sectional-resistance pass promote a longer or heavier primary.
- I required my next candidate to close axial engagement, installed mass and A7b energy together.
