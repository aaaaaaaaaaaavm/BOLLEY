# ADR-054: freeze A9f as a turn/current exchange

Date: 2026-08-31

## Context

A9e shows that implementing the selected 4-turn/380 A sectional machine with ordinary high-current
semiconductor selection creates a large series-loss and installed-device burden. At the same time,
A9b uses only a fraction of the available 48 V link.

## Decision

Before the A9f executable exists, I freeze an integer 4-to-13 turn search at fixed 1,520 A-turn MMF
and fixed slot copper. The search trades current for voltage and evaluates a local three-phase
bridge at every ABC module using supplier-backed 25 C module resistance.

I restore the inherited 10% healthy DC-link margin omitted by A9/A9b. Selection minimizes installed
power-module mass first and weakest normalized electrical margin second.

## Consequence

A passing selected point may replace the 4-turn/380 A electrical partition as a Gen4 development
candidate. It does not inherit A6h field or A5e winding-CAD evidence without a fresh target-specific
reclosure.
