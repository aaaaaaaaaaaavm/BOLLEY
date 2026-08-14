# ADR-036 — why I promoted the A7c selected point

- **Date:** 2026-08-14
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7c four-corner selected-point cage/circuit reclosure

## What I decided

I accepted A7c's four-corner 29/29 result and promoted exactly `n27_p45.3_I380_A10.4` to
provisional A5e Gen3 CAD and an A9 transient sectional-drive gate.

## Why I chose it

The controlling 90%-conductance / 125%-resistance reference shot uses 893.412 J, leaving 6.588 J
below my unchanged 900 J band. The worst qualification shot is 1,302.169 J. Every field, geometry,
mass, voltage, energy, efficiency, thermal, current-density, slip, frequency and normal-force band
passes at all four corners.

The pass is narrow. A7c has 0.732% model margin on reference energy, and my 125% resistance corner
is not a supplier-backed tolerance. I therefore allow geometry and transient work, not a hardware
performance claim.

## What follows

- A5e must resolve discrete Fluxrelay geometry and a packaged mass ledger; it may reject the point.
- A9 must resolve current rise, cell handoff, force ripple, failed-cell behavior and exit timing.
- I keep P38, P39 and all hardware, provider, structure and thermal-cycle evidence open.
