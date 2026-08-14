# A3f — Fluxbridge passive cage and package rescue

**What I knew at declaration:** NOT RUN  
**Evidence class:** homogenized PASSIVE-CAGE + LUMPED MAGNETIC/CIRCUIT MODEL from assumptions  
**Purpose:** I wanted to determine whether a small passive payload modification can remove the Gen1 winding
contradiction without importing a sled, permanent magnets or onboard power.

## Why I gate exists

A5c found that Gen1's four aluminium fins fit the magnetic slots, but the A3e winding does not.
The exact CAD overlap is 3,987.375 mm³ per face. More fundamentally, twenty 20 mm² turns require
400 mm² of bare copper in a nominal 6 mm² inter-cell section. Gen1 is rejected.

The replacement changes the payload interface rather than hiding more launcher copper around it.
Each 1 mm blade becomes a passive **Fluxbridge cage**:

- an amorphous soft-magnetic matrix carries transverse flux;
- 0.75 mm copper rungs on a 2 mm pitch perforate the matrix;
- root and tip buses short the rungs into a ladder cage;
- the cage is electrically passive and receives no spacecraft power; and
- four blades per face preserve independent force-centroid control.

I treat this as a concept under test, not a novelty or flight-compatibility claim.

## The model I froze

- Four faces, four blades per face, 336 mm active length.
- 1.00 mm gross blade, 5.50 mm active cage height, 6.25 mm total projection.
- 0.20 mm nominal clearance on each side in a 1.40 mm slot.
- Copper bar fraction 0.375; magnetic ligament fraction 0.625.
- Homogenized copper sheet thickness 0.375 mm.
- 0.62 T equivalent sheet field; 50% primary tooth duty.
- 57 cells at 16 mm pitch; 48 mm electrical wavelength; 0.912 m primary.
- 8 mm primary tooth and 8 mm winding slot.
- Four turns per cell in 10.5 mm² copper; two coil sides share each 8 × 18 mm slot.
- 48 V nominal DC link and prebias before release.
- Bare 4 kg reference and 6 kg qualification payloads; calculated interface mass is added.

I froze the complete input in `cad/fluxbridge_parameters.json`.

The cage uses the same low-slip thin-sheet relation as A3d, but substitutes its equivalent copper
sheet conductance. Tooth duty converts equivalent field to tooth field. The magnetic ligament
field divides tooth flux by the remaining 0.625 axial magnetic fraction. The shot integration must
include payload work, cage loss, moving-matrix loss, stationary-core loss, primary copper loss and
inverter loss at all 441 CG points for both payload cases.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A3f-1 | Face footprint <=21 mm; projection <=6.5 mm; clearance >=0.20 mm/side. | Reject interface geometry. |
| A3f-2 | Interface increment <=0.30 kg preferred and <=0.40 kg absolute. | Above preferred: disposition; above absolute: reject. |
| A3f-3 | Magnetic-ligament field <=1.45 T. | Increase ligament fraction or reject 2605SA1 screen. |
| A3f-4 | Rated MMF <=1600 A-turn. | The payload modification has not rescued the winding. |
| A3f-5 | Phase current <=400 A and primary current density <=40 A/mm². | Add turns/copper or reject. |
| A3f-6 | Two coil sides occupy <=65% of the 8 × 18 mm winding slot. | Reject before CAD. |
| A3f-7 | Active primary copper + steel <=12 kg. | Reject the compact-primary claim. |
| A3f-8 | Required DC link <=60 V and nominal 48 V margin >=10%. | Redesign bus or winding. |
| A3f-9 | Worst source energy <=1.20 kJ reference and <=1.80 kJ qualification. | Reject the energy case. |
| A3f-10 | Peak DC power <=20 kW for both cases. | Reduce duty or redesign source. |
| A3f-11 | Primary copper rise <=3 K/shot; cage copper rise <=20 K/shot. | Add copper/cooling or reduce cadence. |
| A3f-12 | Cage current density <=180 A/mm² and required slip <=7 m/s. | Increase cage conductance or field. |
| A3f-13 | Worst secondary-only shot efficiency >=50%. | Reject the passive cage operating point. |
| A3f-14 | Terminal frequency <=350 Hz. | Increase wavelength or revise drive. |
| A3f-15 | A 1% opposed-field mismatch leaves <=100 N net normal force. | Reject centring tolerance. |

Paired limits are stored separately and will produce more than fifteen executable bands.

## What I explicitly did not claim

- Homogenizing discrete copper bars as a sheet is not cage FEA.
- Supplier ribbon values do not prove properties after perforation, lamination, bonding or vibration.
- Magnetic attraction, slot harmonics, cogging, bar current crowding, end-bus resistance, fringing
  and six-degree-of-freedom tip-off require independent models.
- A 0.20 mm nominal gap is not a tolerance stack.
- I do not treat this as launch-provider approval, a manufacturing release or proof of legal novelty.
- Gate, housing, inverter, DC link, cooling, sensors, cabling and structure remain outside active
  electromagnetic mass.

## Output I required

Report moving-interface mass by material, cage conductance/slip/current/heat, magnetic fields/MMF,
winding window/current/R/L/voltage, primary mass, full energy partition at every CG point, frequency,
normal mismatch, every band and a disposition. A passing result proceeds to field FEA and Gen2 CAD;
it does not proceed to flight hardware.
