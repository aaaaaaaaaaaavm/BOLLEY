# ADR-048: preserve the first A9 execution before residual normalization

Date: 2026-08-31

## Context

I executed the committed A9 sectional-drive model from commit
`1e6aa19426fe665a2f49fcb1ba2deaa649967e9f` after the pre-run gravity correction in ADR-047.

The fine run passes 11 of 13 bands. The two failures are `healthy_axial_force` and
`failed_cell_axial_force`. Both are controlled by the same reported minimum qualification-channel
force: -1.4210854715202004e-14 N.

The force allocator is analytically nonnegative on the declared convex envelope. `common.py`
already defines `RESIDUAL_FLOOR = 1e-9` for should-be-zero constraint residuals and explains why
values below that floor are snapped to zero before they become reported evidence. A9 failed to use
that existing convention on its minimum force.

I preserve the first execution in
`analysis/results/sectional_drive_a9_failure.json`. I do not reinterpret it as a pass.

## Electrical result from the failed execution

The numerical residual does not control the electrical quantities. The fine run reports:

- 897.74844054099 J maximum reference source energy against 900 J;
- 1,308.4890522592157 J maximum qualification source energy against 1,500 J;
- 364.25099335409493 A maximum healthy phase current against 400 A;
- 386.34652118192486 A full-force failed-cell recovery current against 400 A;
- 14.149322762821571 V maximum healthy additive link demand against 48 V;
- 15.007623112182461 V failed-cell additive link demand against 48 V; and
- 11,768.693387674215 W maximum peak source power against 15 kW.

These are model outputs. They do not close P11, P29, P39 or P40.

## Decision

I will open A9b as a numerical reclosure only. A9b may apply the repository's already-declared
`snap_residual` convention to the should-be-zero minimum force before the unchanged physical bands
are evaluated.

A9b may not change the geometry, current command, handoff law, energy accounting, fault policy,
resolutions or acceptance thresholds.

## Consequence

A9 remains a published 11/13 execution. If A9b passes, that result establishes only that the two
A9 misses were representation noise below an existing residual floor. It does not erase this run
or create supplier, 3D-field, packaging, EMC or hardware evidence.
