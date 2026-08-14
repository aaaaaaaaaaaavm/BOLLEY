# ADR-028 — why I rejected the exact Gen2.6 hot-resistance point

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7b four-corner cage/circuit reclosure

## What I decided

I rejected the exact Gen2.6 circuit point while retaining the A6g field solution and five-lane
Quintweb translator. I moved the next correction to the stationary winding rather than adding
more spacecraft interface mass or changing a validation band.

## Why I chose it

Both nominal-resistance corners pass all 19 A7b bands. Both 125%-resistance corners fail only the
900 J reference-energy cap, at 929.432 J and 959.923 J. Cage rise, cage current density, slip and
secondary efficiency—all four translator failures from A7a—now pass.

Paired 90%-conductance corners isolate 266.583 J of nominal-resistance source energy. With the
rest of A7b fixed, phase resistance must fall to at most 82.02% of the current value to close the
hot corner. That diagnostic is not permission to overfill the slot or exceed the primary-mass
band; the correction must be frozen and rechecked as a physical winding geometry.

## What follows

- I preserved five blades per face and the A6g magnetic field evidence.
- I did not spend the remaining 11.77 g interface margin on a stationary-copper failure.
- Search turn length, slot geometry and conductor allocation before declaring Gen2.7.
- Gen3 CAD remains blocked until the corrected circuit point is frozen and reclosed.
