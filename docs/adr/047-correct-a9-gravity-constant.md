# ADR-047: correct the A9 inherited gravity constant before execution

Date: 2026-08-31

## Context

ADR-046 froze A9 as an exact transient extension of A7c. The first A9 parameter file used
9.80665 m/s2 for gravity. A7c's actual shot model used 9.81 m/s2.

For the 4 kg reference case plus the selected 0.371364383889362 kg interface, the two constants
do not reproduce the same mechanical work over 0.90 m. A9 is supposed to inherit A7c rather than
replace its operating point.

## Decision

Before `analysis/sectional_drive.py` exists, I change only `gravity_m_s2` in
`analysis/sectional_drive_parameters.json` from 9.80665 to 9.81.

I do not change a geometry value, resistance, inductance, corner, fault condition or acceptance
band.

## Consequence

The original ADR-046 commit remains part of the record. A9 will execute from the corrected
parameter file and will state ADR-047 as a pre-execution correction. This is not a result-driven
change because no A9 executable model or result existed when I made it.
