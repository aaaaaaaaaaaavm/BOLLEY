# ADR-049: freeze A9b as a residual-only correction

Date: 2026-08-31

## Context

ADR-048 preserves A9's 11/13 result. Its only failed bands are caused by a reported minimum force of
-1.4210854715202004e-14 N. The repository already has a declared 1e-9 residual floor in
`analysis/common.py` for should-be-zero constraint residuals.

## Decision

I freeze A9b before its executable wrapper exists.

A9b may only apply `snap_residual` to the A9 minimum channel force before the two force-sign bands
are evaluated. It may not change any A9 physical input, corner, handoff law, fault policy, time-step
resolution or acceptance band.

## Consequence

If A9b passes, I will retain Fluxrelay for supplier-backed electrical and packaging closure. If any
unsnapped quantity changes or another band fails, I will preserve that result and keep P38 open.

A9's original failed execution remains part of the record in either case.
