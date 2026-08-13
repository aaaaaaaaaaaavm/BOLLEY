# Open problems

This is the live defect and evidence register. Closing an item requires a linked result,
measurement, supplier document or decision record. Confidence is not closure.

| ID | Problem | Close condition | Priority | State |
|---|---|---|---|---|
| P1 | Required reluctance force has not been produced across the proposed covered rail gap. | One-corner coupon meets A3 bands. | CRITICAL | OPEN |
| P2 | Phase current may not rise quickly enough at roughly 250 Hz pole passage. | Nonlinear electromagnetic/circuit model and pulse test meet A3 voltage and current bands. | CRITICAL | OPEN |
| P3 | The aluminium wear skin increases effective magnetic gap and may erase the force margin. | 3D FEA includes skin, adhesive, tolerances and fringing. | CRITICAL | OPEN |
| P4 | Normal attraction and channel mismatch can overload the guide rails. | Worst-fault side-load model plus four-channel hardware test. | CRITICAL | OPEN |
| P5 | Exit-end fringing can create a final force impulse and tip-off. | Six-degree-of-freedom test meets 2 deg/s/axis. | CRITICAL | OPEN |
| P6 | Embedded steel or soft-magnetic composite may disturb payload magnetometers. | Unpowered remanence survey and powered transient test meet A4. | HIGH | OPEN |
| P7 | Rail inserts may delaminate or fret through ascent vibration and repeated shots. | Structural qualification and 100-cycle wear test. | HIGH | OPEN |
| P8 | Rail heating from hysteresis and eddy current is unknown. | Coupled loss/thermal model checked by instrumented coupon. | HIGH | OPEN |
| P9 | No independent retention gate has been selected or sized. | Gate design passes ascent, no-fire and commanded-release tests. | HIGH | OPEN |
| P10 | The four-channel force-allocation law assumes known payload CG and calibrated channel force. | CG declaration error and force-sensor uncertainty close inside the tip-off budget. | HIGH | OPEN |
| P11 | No capacitor, inverter, switch or cable has a supplier-backed pulse rating for this duty. | Quoted and datasheet-backed electrical BOM passes the shot. | HIGH | OPEN |
| P12 | The proposed hybrid rail has not been accepted by a dispenser or launch provider. | Written interface disposition or mission-specific waiver. | HIGH | OPEN |
| P13 | The recurring-cost advantage is entirely unquoted. | Supplier quotations and integration labour model. | MEDIUM | OPEN |
| P14 | Host recoil and campaign attitude restoration have not been re-derived without the sled return. | Host-specific momentum and cadence assessment. | MEDIUM | OPEN |
| P15 | Patent and literature searches are incomplete. | Professional search or documented decision not to pursue protection. | MEDIUM | OPEN |
| P16 | No bus vendor has agreed that 0.15–0.25 kg of passive rail hardware is commercially acceptable. | At least one written customer or bus-vendor response. | MEDIUM | OPEN |
| P17 | The unmodified-payload four-finger fallback remains only a sketch. | Separate requirements and one-corner actuator screen. | LOW | DEFERRED |

## Register discipline

- `OPEN` means unresolved.
- `MODELLED` means a model has narrowed the problem but hardware evidence is absent.
- `CORRECTED` means a previous result was wrong and the replacement is traceable.
- `CLOSED` requires the stated close condition.
- `DEFERRED` means deliberately outside the active baseline, not solved.

