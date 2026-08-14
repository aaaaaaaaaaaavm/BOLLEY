# ADR-035 — why I froze the selected-point A7c reclosure

- **Date:** 2026-08-14
- **Status:** Accepted
- **Decider:** Adityavardhan Mishra
- **Evidence:** A8b selected point and passing A6h field result

## What I decided

I froze A7c on exactly `n27_p45.3_I380_A10.4`. I retain A8b's geometry, winding, active-window
resistance, four robustness corners, two payload cases, 21 by 21 CG grid and all 29 hard bands. I
replace only the field peaks and phase-window inductance with their fresh A6h values.

## Why I chose it

A8b's hot reference energy uses 99.50% of my 900 J band, so even a small field or inductance change
deserves an exact reclosure. Reopening the search after A6h would let me fit the answer. A7c instead
asks whether the point I already selected survives the independent field result.

## What follows

- A pass opens provisional Gen3 CAD and transient sectional-drive modelling only.
- A failure rejects the exact selected point; I will not repair it by changing A7c's bands.
- Hardware, structural, axial-end and switching evidence remain open in either outcome.
