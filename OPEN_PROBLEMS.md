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
| P10 | The four-channel force-allocation law assumes known payload CG and calibrated channel force. | CG declaration error and force-sensor uncertainty close inside the tip-off budget. | HIGH | MODELLED |
| P11 | No capacitor, inverter, switch or cable has a supplier-backed pulse rating for this duty. | Quoted and datasheet-backed electrical BOM passes the shot. | HIGH | OPEN |
| P12 | The proposed comb-fin reaction interface has not been accepted by a dispenser or launch provider. | Written interface disposition or mission-specific waiver. | HIGH | OPEN |
| P13 | The recurring-cost advantage is entirely unquoted. | Supplier quotations and integration labour model. | MEDIUM | OPEN |
| P14 | Host recoil and campaign attitude restoration have not been re-derived without the sled return. | Host-specific momentum and cadence assessment. | MEDIUM | OPEN |
| P15 | Patent and literature searches are incomplete. | Professional search or documented decision not to pursue protection. | MEDIUM | OPEN |
| P16 | No bus vendor has agreed that 0.35–0.40 kg of passive interface hardware is commercially acceptable. | At least one written customer or bus-vendor response on the selected 0.371 kg interface. | MEDIUM | OPEN |
| P17 | The unmodified-payload four-finger fallback remains only a sketch. | Separate requirements and one-corner actuator screen. | LOW | DEFERRED |
| P18 | The 0.50 mm equivalent-thickness mass screen does not define a closed moving flux path. | A3a identifies an explicit topology that passes area and interface-mass gates. | CRITICAL | MODELLED |
| P19 | The comb-fin requires launcher pole access on both sides of every fin, but no provider-approved 3U dispenser cross-section exists yet. | A5a geometry survives preliminary guidance, then a selected provider accepts stator, containment and rail-contact drawings. | CRITICAL | MODELLED |
| P20 | A face-centred comb-fin consumes spacecraft side-panel area and may conflict with solar cells or harness routing. | A5a area screen plus bus-specific panel layout review. | HIGH | OPEN |
| P21 | The comb-fin root, covers and segmented inserts have no structural load path or debris-containment proof. | Detailed capture design passes stress, vibration and fail-safe retention review. | CRITICAL | OPEN |
| P22 | A5a's whole-face developed-shear statistic is not the axial force law of a tooth-overlap reluctance machine. | A3b0 edge-force bound passes, followed by a nonlinear 3D flux-linkage/force map. | CRITICAL | OPEN |
| P23 | The A5b sketch gives each stationary pole only a 2 mm throat, while shared interior poles must return two fin fluxes. | A3b1 flux-conservation bound passes before yoke or winding design. | CRITICAL | OPEN |
| P24 | Fluxfoil's 0.50 T RMS travelling field has no explicit stator, winding, inverter or source behind it. | A3c passes, then a finite stator/circuit model closes field, voltage, current and loss. | CRITICAL | OPEN |
| P25 | Finite-length and finite-height induction end effects may erase the thin-sheet force margin. | Independent 2D/3D field solution and force coupon meet A3 bands. | CRITICAL | OPEN |
| P26 | Fluxfoil had no dimensioned series-flux stator, winding or pulse source behind the A3d field. | A3e closes a predeclared lumped circuit; field FEA and hardware remain separate gates. | CRITICAL | MODELLED |
| P27 | The A3e stator carries about 1.15 kN common-mode normal attraction on each side of a rated fin. | Gen1 structure holds worst gap/runout without contact; coupon measures net and common-mode loads. | CRITICAL | OPEN |
| P28 | A3e's winding intersects the moving interface and its bare-copper section exceeds the nominal inter-cell window by 66.7:1. | A replacement passes a predeclared winding-window gate and non-interfering CAD. | CRITICAL | CLOSED |
| P29 | The Fluxbridge perforated magnetic matrix and copper ladder are represented by homogenized permeability and sheet conductance. | Nonlinear transient field/circuit FEA and an instrumented cage coupon agree inside declared bands. | CRITICAL | MODELLED |
| P30 | The 0.20 mm nominal Fluxbridge gap has no manufacturing, thermal, vibration or runout tolerance stack. | Worst-case tolerance model and measured coupon runout preserve positive clearance. | CRITICAL | OPEN |
| P31 | A3g's two coil sides share a 15 × 18 mm slot only as a sectional fill calculation. | A5d routes both alternating layers with positive coil/core/foil clearance and matched copper volume. | CRITICAL | CLOSED |
| P32 | A6 finds only 0.6568 T mean blade field while the stationary return reaches 3.2346 T peak. | A Gen2.1 return geometry passes the same independent field, saturation and mesh bands. | CRITICAL | OPEN |
| P33 | A6 per-cell inductance is 1.3945 times A3g, invalidating the selected drive closure. | Recompute voltage, current, energy and loss from the passing Gen2.1 field/inductance result. | CRITICAL | OPEN |
| P34 | A6b's fine ligament and return-haunch peaks exceed their limits by 2.21% and 0.62%. | A predeclared Gen2.2 correction passes <=1.45 T moving ligament and <=1.55 T stationary peak on all formal checks. | CRITICAL | OPEN |
| P35 | Gen2.3's stepped-thickness magnetic ribs have no structural load path or manufacturable encapsulation detail. | Gen2.3 CAD, coupon drawing and structural test article preserve the 1.12 mm rib and copper continuity. | HIGH | OPEN |
| P36 | The 336 mm cage leaves the 900 mm stator during a claimed 900 mm full-force stroke, while A7b charges every series cell instead of only overlapped sections. | Axial overlap, sectional circuit and installed-length model close velocity, energy and primary-mass bands together. | CRITICAL | CLOSED |
| P37 | A8b scales A6g fields linearly from 375 to 380 A, leaving only 1.04% stationary-core peak margin. | Fresh A6h coarse/fine/alternate nonlinear meshes pass every field, peak and convergence band at the selected point. | CRITICAL | OPEN |
| P38 | The nine-cell active window has no switching handoff, force-ripple, fault or end-cell model. | A sectional-drive transient closes force ripple, DC-link, current sharing, failed-cell and exit-end bands. | CRITICAL | OPEN |
| P39 | The 15.908 kg primary leaves 92 g for the active-material band and excludes structure, cooling, wiring and power electronics. | A packaged Gen3 mass ledger either closes a declared installed-system allocation or rejects the selected topology. | CRITICAL | OPEN |

## Register discipline

- `OPEN` means unresolved.
- `MODELLED` means a model has narrowed the problem but hardware evidence is absent.
- `CORRECTED` means a previous result was wrong and the replacement is traceable.
- `CLOSED` requires the stated close condition.
- `DEFERRED` means deliberately outside the active baseline, not solved.
