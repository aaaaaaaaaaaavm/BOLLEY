# ADR-042: I freeze the Fluxpiston controlled-leakage screen

- **Date:** 2026-08-28
- **Status:** accepted as a pre-run declaration

## Context

A10 made pressure small by using the whole CubeSat face, but it moved the sealing perimeter to the
spacecraft envelope. A perfect sliding seal would import friction, wear and tolerance risk. A
non-contact labyrinth imports continuous leakage instead.

## Decision

I screen intentional annular leakage before selecting seal hardware. I command the gas stage 0.25
m/s below the final target, retain electromagnetic trim for the remainder, and sweep clearance and
temperature before writing the calculator.

## Consequences

- I will know whether replenishing leakage is grams or hundreds of grams per shot.
- I will size only an equivalent supply orifice and reservoir volume, not claim a valve or tank.
- I keep contact friction, rarefied flow, thermal transients, contamination and plume impulse open.
- I do not draw Gen6 CAD from a passing ideal-gas calculation.

