# ADR-027 — freeze the five-lane A7b reclosure

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A6g passing field result and A7a failure localisation

## Decision

Repeat A7a without changing its corners or 19 bands. Substitute only the five-blade area/mass,
A6g field and inductance, and four-turn Quintweb circuit quantities.

## Why

An area correction should be judged against the same result that demanded it. Reusing A7a's
complete CG and robustness definition prevents the fifth blade from earning promotion through a
looser energy, thermal or efficiency screen.

## Consequences

- The 0.25/0.30 kg mass preferences remain failed and the 0.40 kg limit remains hard.
- A7b can promote only to CAD and higher-fidelity transient work.
- A failure must change Quintweb or end the five-lane branch; thresholds remain fixed.
