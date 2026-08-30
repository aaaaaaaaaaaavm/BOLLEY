# ADR-051: freeze A9d as a supplier bridge lower-bound screen

Date: 2026-08-31

## Context

A9b's reference shot is 897.74844054099 J only because A7c/A9 use a generic 97% inverter
efficiency. The real electrical conversion chain has to fit inside the same 900 J system cap.

## Decision

Before the A9d executable exists, I freeze a necessary lower-bound screen using public supplier
data for one automotive 48 V MOSFET module family and one 100 V discrete MOSFET family.

I remove the generic 0.97 factor from A9b and add only supplier-backed 25 C bridge conduction. I
leave every omitted loss visible as remaining budget. A candidate must fit the existing voltage and
energy limits before switching, selector, cable, busbar, capacitor and cooling penalties are added.

## Consequence

A failure rejects that bridge partition. A pass only proves that its 25 C conduction lower bound is
not already fatal. P11, P39 and P40 remain open until the omitted terms and hot conditions are
closed.
