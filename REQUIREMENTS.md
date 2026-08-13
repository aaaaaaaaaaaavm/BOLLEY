# System requirements

These are Phase 0 requirements. A number without a verification route is not yet a requirement;
it is an aspiration wearing a unit.

| ID | Requirement | Verification | Status |
|---|---|---|---|
| BOL-R-001 | Accept a rail-guided 3U CubeSat with **4 kg reference mass** and **6 kg qualification mass**. | Fit check, mass-property inspection | OPEN |
| BOL-R-002 | Command 0–12 m/s for the 4 kg reference payload over no more than 0.90 m powered length. | Instrumented full-stroke test | OPEN |
| BOL-R-003 | Deliver at least 10 m/s to the 6 kg qualification payload without exceeding its agreed acceleration limit. | Instrumented full-stroke test | OPEN |
| BOL-R-004 | Nominal longitudinal acceleration shall not exceed 8 g in the Phase 0 baseline. | Model, then accelerometer | OPEN |
| BOL-R-005 | Release tip-off shall be no more than 2 deg/s per axis. | Six-degree-of-freedom separation test | OPEN |
| BOL-R-006 | The cooperative interface should add no more than 0.25 kg and shall add no more than 0.40 kg to a 3U payload. | Weighed prototype | OPEN |
| BOL-R-007 | Spacecraft-side hardware shall be passive: no powered coils, permanent magnets, pyrotechnics, pressure vessels or launch-time software. | Design inspection | OPEN |
| BOL-R-008 | The external sliding/contact surface shall remain hard-anodized aluminium and retain the applicable launch-provider rail geometry. | Drawing review and fit check | OPEN |
| BOL-R-009 | Gross stored-energy draw for the 4 kg, 8 g, 0.90 m shot shall be no more than 900 J. | DC-link power analyser | OPEN |
| BOL-R-010 | Peak launcher electrical power for the reference shot should be no more than 15 kW. | DC-link power analyser | OPEN |
| BOL-R-011 | No launcher propulsion member shall require capture after payload release. | Architecture inspection | SATISFIED BY CONCEPT |
| BOL-R-012 | An independent, fail-safe retention gate shall carry ascent loads and inhibit firing. | Structural test and fault injection | OPEN |
| BOL-R-013 | Commanded exit velocity dispersion shall initially be no more than 0.10 m/s at 3 sigma. | At least 30 hardware shots | OPEN |
| BOL-R-014 | The unpowered cooperative interface shall add no more than 50 microtesla above ambient outside the static payload envelope. | Three-axis magnetometer survey | OPEN |
| BOL-R-015 | One electromagnetic face channel shall tolerate the peak force required by the declared transverse centre-of-gravity envelope. | Pulse-force coupon | OPEN |
| BOL-R-016 | All externally retained parts shall remain attached through ascent, deployment and mission operation. | Structural analysis and qualification test | OPEN |

## Requirement sources

- The 6 kg 3U case, rail geometry, aluminium guidance, hard-anodized contact requirement and
  +/-20 mm transverse centre-of-gravity envelope come from the CubeSat Design Specification
  Rev. 14.1 as preliminary design guidance. Launch-provider requirements supersede it.
- The 2 deg/s tip-off threshold follows the tighter flown dispenser class used by VOLLEY.
- The mass, energy and power limits are Bolley programme decisions. They exist to prevent the
  new design from recreating VOLLEY's mass and bank problems under different names.

Any change to a numbered requirement needs an ADR and a note stating whether the change occurred
before or after the relevant result was seen.
