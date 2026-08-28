# A10, my Gen4-Gen6 architecture screen

**State: RUN. My immutable bands produced 7 PASS, 2 FAIL, 1 OPEN and 2 REPORT results.**

I froze this screen after VOLLEY's requirement-attribution result showed that Bolley deletes an
11% mover while retaining a 28.1% pulse obligation. I am not reopening A6h, A7c or A5e. I am asking
which next generation attacks the system term that now controls the architecture.

The controlled inputs are in [`analysis/gen456_parameters.json`](../analysis/gen456_parameters.json).
The calculation script and result do not exist in this declaration commit.

## Frozen bands

| Band | Test I will run | Pass condition | Meaning of failure |
|---|---|---|---|
| 1 | Kinematic consistency of 12 m/s, 0.90 m and 8 g | The maximum constant-acceleration velocity is at least 12 m/s | My numbered requirements contradict one another before any architecture is compared |
| 2 | Gen5 displaced-mass threshold | I report the exact bus mass Fluxframe must replace to meet 0.25 kg net added mass | I will not award an unevidenced multifunctional mass credit |
| 3 | Fluxpiston reference pressure | Required mean pressure is at most 50 kPa over a 0.01 m2 effective face | The full-face piston does not buy the expected low-pressure regime |
| 4 | Fluxpiston qualification pressure | Required mean pressure is at most 50 kPa for 6 kg at 10 m/s | The qualification case needs a materially different pressure architecture |
| 5 | Longitudinal force | Both pressure cases remain at or below 8 g nominal acceleration | Gen6 solves energy by violating my load requirement |
| 6 | Short electromagnetic trim energy | +/-0.25 m/s at either target needs at most 25 J of kinetic-energy correction | The “trim-only” motor is still a bulk launcher in disguise |
| 7 | First interface-mass allocation | Pressure cup plus short passive trim secondary is at most 0.25 kg | Gen6 immediately misses the preference before seals, fasteners or structure are added |
| 8 | Spacecraft passivity | No spacecraft power, software, permanent magnet, pyrotechnic or pressure vessel is required | Gen6 leaves Bolley's premise |
| 9 | No outgoing launcher mover | No launcher propulsion member follows the payload into orbit | Gen6 recreates the capture problem |
| 10 | Seal evidence | I report sealing/leakage as OPEN rather than infer it from ideal pressure work | An ideal gas calculation is being mistaken for a pressure mechanism |
| 11 | Burn-and-drop timing | I report the thrust-arc time at 0.10, 0.25 and 0.50 m/s2 without calling it free | The mission-level comparator is hidden from the mechanism trade |
| 12 | Strainrail specific energy | Required stored energy is at most 350 J/kg of current interface mass | The passive structural store uses material-limit arithmetic rather than a buildable margin |

## Disposition rule

I will not select a winner by counting passes. A concept can advance only if it changes the
controlling requirement and its failures open finite, testable next gates. Gen6 may advance as an
architecture candidate with band 10 intentionally OPEN; it may not be described as closed until a
leakage/contact model and then a test exist.

## Result and disposition

I ran the declared calculation without changing these bands. Band 1 rejected the original
12 m/s / 0.90 m / 8 g triplet: the ceiling is 11.8855 m/s. I corrected BOL-R-002 to 11.8 m/s in a
post-result ADR while retaining the stroke and acceleration limits.

Fluxframe needs 121.36 g of evidenced displaced bus mass to meet the 0.25 kg preference. I promote
it only to a selected-bus net-mass gate. Fluxpiston needs 30.942 kPa mean pressure for the 4 kg,
11.8 m/s screen and 33.333 kPa for 6 kg at 10 m/s. Its +/-0.25 m/s trim-energy ceiling is 15.188 J.
I promote it only to leakage/contact, pressure-transient, aft-face structure, trim and 6-DOF exit
gates. Band 10 remains OPEN by construction.

Strainrail fails at 749.9 J/kg against my frozen 350 J/kg screen. Burn-and-drop remains a reported
mission comparator whose 24–120 s thrust arcs all spend 12 m/s of host delta-v.

The controlled result is
[`analysis/results/gen456_architecture_screen.json`](../analysis/results/gen456_architecture_screen.json)
and my generated reading is
[`docs/GEN456_ARCHITECTURE_SCREEN.md`](../docs/GEN456_ARCHITECTURE_SCREEN.md).
