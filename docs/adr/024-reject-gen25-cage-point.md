# ADR-024 — reject the exact Gen2.5 cage/circuit point

- **Date:** 2026-08-13
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A7a four-corner, two-payload, 3,528-point cage/circuit result

## Decision

Reject the exact Gen2.5 passive-cage operating point despite its A6f field pass. Preserve the
three-turn primary, R4 return and Fluxweb magnetic backstrap. Do not raise current or relax the
900 J, 20 K, 180 A/mm2 or 50% secondary-efficiency bands.

## Why

The 8% copper trade and lower field delivered by the resolved cross-section combine into four
translator-side failures. Worst cage rise is 22.74 K, current density is 183.30 A/mm2, secondary
efficiency is 45.66% and the hot/low-conductance reference shot is 905.1 J. Voltage, peak power,
slip and qualification energy all pass.

## Consequences

- A6f remains valid field evidence; A7a blocks CAD promotion of the exact Gen2.5 point.
- The next architecture screen should add passive active area before adding blade thickness:
  a fifth Fluxweb per face can reduce force density while remaining under the 0.40 kg limit.
- Any five-blade candidate must repeat the transverse field gate before cage reclosure and CAD.
