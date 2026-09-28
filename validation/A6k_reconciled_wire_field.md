# A6k: actual wires in the reconciled core

Adityavardhan Mishra · 17 September 2026

I freeze a fresh field run for A6j-R2 before implementing the adapter. Use its
selected common geometry, both alternating coil heights and the selected A5h
bare rectangular wire sections centered in their maximum-insulation envelopes.
Retain all inherited nonlinear material, mesh, solver and physical bands.
Use 12 turns at 1520/12 A RMS; each side must integrate to 1520 A-turn within
1e-8 relative. Per-cell and active-phase inductance comparators scale by nine
because the current is one third of the four-turn reference; this scaling is a
comparator, not a substituted field solution. Do not inherit any old field pass.

Run all three inherited meshes for both placements. Record each completed
placement immediately. Check mean-field/coenergy mesh convergence, outer-boundary
sensitivity, current closure and nonlinear convergence separately from physical
bands. If either placement fails a physical band, reject promotion of this exact
candidate to a powered coupon. If numerics fail, the field verdict is unresolved.
Retain all failures. Keep full resolved inputs and hashes of the adapter, engine,
common-geometry file, winding source and criteria. A transverse RMS-equivalent
magnetostatic slice does not close terminals, end force, dynamic current, hot drive,
thermal response, magnetic cleanliness or full three-dimensional behavior.
