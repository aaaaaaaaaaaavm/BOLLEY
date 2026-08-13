# Validation register

Validation starts before the result.

Each run sheet states inputs, evidence class, numerical bands and the action following a failure.
The committed run sheet is not edited to make a completed run pass. If a band was wrong, an ADR
may supersede it while preserving the original and stating that the answer was already known.

| Run | Question | Evidence | Initial state |
|---|---|---|---|
| [A1](A1_first_order_sizing.md) | Is the cooperative architecture dimensionally worth pursuing? | First-order model | NOT RUN |
| [A2](A2_force_allocation.md) | Can four positive rail forces place thrust through the allowed CG envelope? | Independent algebraic model | NOT RUN |
| [A3a](A3a_flux_path_screen.md) | Which explicit moving flux/conductor path deserves nonlinear analysis? | Analytical topology screen | NOT RUN |
| [A3](A3_corner_coupon.md) | Can one covered-gap rail channel make the force at speed? | FEA, then measurement | NOT RUN |
| [A4](A4_magnetic_compatibility.md) | Is the passive rail magnetically tolerable? | Measurement | NOT RUN |
| [A5a](A5a_comb_fin_envelope.md) | Can a low-profile three-fin face channel fit preliminary CubeSat guidance and preserve control? | Analytical interface screen | NOT RUN |
| [A3b0](A3b0_edge_force_bound.md) | Can that exact comb meet force even in an ideal tooth-edge energy bound? | Analytical upper bound | NOT RUN |
| [A5b](A5b_quad_comb_envelope.md) | Does a four-fin, 6 mm redesign recover ideal force margin without breaking the interface? | Analytical interface/force screen | NOT RUN |
| [A3b1](A3b1_stator_throat_bound.md) | Can the quad-comb's shared stationary poles carry and return its required flux? | Analytical flux-conservation bound | NOT RUN |
| [A3c](A3c_fluxfoil_induction.md) | Can a passive four-fin aluminium sheet carry the pulse without excessive slip, heating or normal imbalance? | Analytical thin-sheet model | NOT RUN |
| [A5](A5_interface_fit.md) | Can the rail remain a valid mechanical interface? | Drawing review and fit check | NOT RUN |

`MODELLED` is not a synonym for `VALIDATED`. Only hardware evidence can close the central claim.
