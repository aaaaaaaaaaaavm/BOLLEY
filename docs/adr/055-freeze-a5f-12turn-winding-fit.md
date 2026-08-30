# ADR-055: freeze the A5f 12-turn winding fit

Date: 2026-08-31

## Context

A9f selected a 12-turn, 126.66666666666667 A winding point because it reduces the local-bridge power-module lower bound while preserving 1,520 A-turn and the existing copper amount. A5e only represented each coil as a homogeneous copper ring equivalent to four 10.4 mm2 turns. It did not resolve insulation or individual conductors.

The A9f electrical selection therefore has no right to inherit A5e's winding-fit result.

## Decision

I freeze A5f before creating its calculator or detailed winding CAD.

I keep the A5e core, cage, pitch, inner coil spans and clearance bands. I search a twelve-conductor rectangular-wire envelope using the dimensional and Grade 2 insulation rules recorded in `cad/gen3_12turn_winding_parameters.json`.

I use IEC 60317-0-2:2020 only for the general rectangular-wire geometry rules in the screen. I do not treat the standard as proof that a supplier will make the selected wire. The public manufacturer example in the parameter file establishes only that custom rectangular dimensions are a normal product class, not that this exact winding is available or qualified.

## Consequence

A5f can reject the 12-turn electrical selection on geometry before I spend work on a fresh package. A pass promotes the point only to detailed winding CAD, field bookkeeping reclosure and packaged electrical work.

The 4-turn Gen3 point remains the controlled baseline while A5f is unresolved.
