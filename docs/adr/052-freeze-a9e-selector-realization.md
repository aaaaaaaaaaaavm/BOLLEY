# ADR-052: freeze A9e as a selector-realization lower bound

Date: 2026-08-31

## Context

A9d found supplier-backed 25 C bridge partitions that fit the existing source-energy cap, but the
best low-mass bridge candidates leave little energy for the cell selector that A9 assumes ideally.
The selected Fluxrelay stator still has 108 installed cell positions and advances its nine-cell
active window by one cell at each handoff.

## Decision

Before the A9e executable exists, I freeze two realizations: a shared face bridge with a
bidirectional series selector at every cell, and a local three-phase bridge at every ABC module.

I solve only the minimum parallel semiconductor count needed to satisfy the existing 900 J
reference cap at the same 25 C supplier resistance data used by A9d. I do not set a new acceptable
part-count or mass threshold after seeing the answer.

## Consequence

A9e can show whether the ideal selector hides a large hardware burden. It cannot promote a selector
or close P11/P39 without switching, hot resistance, packaging, cooling and control evidence.
