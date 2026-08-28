# ADR-040: I correct the reference velocity to 11.8 m/s

- **Date:** 2026-08-28
- **Status:** accepted after A10

## Context

A10 computed an architecture-independent inconsistency in my numbered requirements. Starting from
rest, 8 g over 0.90 m reaches 11.8855 m/s. Exactly 12 m/s needs 8.1549 g or 0.9174 m.

## Decision

I change BOL-R-002 from 12.0 to 11.8 m/s. I retain the 8 g nominal acceleration ceiling and 0.90 m
powered-length limit.

## Why I chose this side of the trade

The 8 g limit protects the payload and the 0.90 m limit controls dispenser packaging. The old
12 m/s value was already described elsewhere as approximately 12 m/s. An exact 11.8 m/s target
preserves that duty without consuming every kinematic millimetre or asking the model to ignore a
requirement.

## Consequences

- I close P42 as a requirement correction, not as a design pass.
- Later Gen4, Gen5 and Gen6 comparisons use 11.8 m/s for the reference case.
- Earlier frozen results remain historical evidence at their declared inputs.
- I must propagate the 11.8 m/s target into A9 and any mission/orbit case before promotion.

