# ADR-017 — why I froze the Gen2.3 Fluxrib interface

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6c failure localisation, mass accounting and non-validation development mesh

## What I decided

I froze a stepped-thickness Fluxbridge blade: 1.06 mm active magnetic ribs, unchanged 1.00 mm
copper rungs, and 30 µm encapsulation per side. I widened the launcher slot to 1.52 mm so the
thicker ribs retained 0.20 mm nominal clearance. I kept the passing Gen2.2 R4 primary and 1,200
A-turn point.

## Why I chose it

This spends material exactly where A6c fails. It does not increase current, launcher footprint,
copper resistance or payload electronics. The change adds 14.23 g and keeps the complete passive
interface at 0.29912 kg.

## What follows

- A6d must pass the stronger worst-mesh field gate before promotion.
- A passing field still requires new discrete CAD and transient cage analysis.
- The stepped rib creates a real structural and encapsulation detail that hardware must qualify.
