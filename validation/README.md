# Validation register

Validation starts before the result.

Each run sheet states inputs, evidence class, numerical bands and the action following a failure.
The committed run sheet is not edited to make a completed run pass. If a band was wrong, an ADR
may supersede it while preserving the original and stating that the answer was already known.

| Run | Question | Evidence | Initial state |
|---|---|---|---|
| [A1](A1_first_order_sizing.md) | Is the cooperative architecture dimensionally worth pursuing? | First-order model | NOT RUN |
| [A2](A2_force_allocation.md) | Can four positive rail forces place thrust through the allowed CG envelope? | Independent algebraic model | NOT RUN |
| [A3](A3_corner_coupon.md) | Can one covered-gap rail channel make the force at speed? | FEA, then measurement | NOT RUN |
| [A4](A4_magnetic_compatibility.md) | Is the passive rail magnetically tolerable? | Measurement | NOT RUN |
| [A5](A5_interface_fit.md) | Can the rail remain a valid mechanical interface? | Drawing review and fit check | NOT RUN |

`MODELLED` is not a synonym for `VALIDATED`. Only hardware evidence can close the central claim.

