# ADR-044: I freeze the public chassis-mass envelope for Fluxframe

- **Date:** 2026-08-28
- **Status:** accepted as a pre-run declaration

## Context

Gen5 needs 121.36 g of real displaced bus mass. Spacecraft multifunctional-structure literature
shows why integration is worth testing, but it cannot tell me how much mass a selected 3U bus will
actually surrender.

## Decision

I first compare the threshold with sourced public 3U structure masses. I keep an upper-bound
datasheet value labelled as an upper bound. I freeze three arithmetic bands and three deliberately
open equivalence/acceptance bands before writing the calculator.

## Consequences

- A pass can show that sufficient gross chassis mass exists in the design space.
- A pass cannot award one gram of displaced mass to Fluxframe.
- My next Gen5 work must select a bus and produce drawings, a removed-parts ledger and coupled
  structural/thermal/electrical checks.

