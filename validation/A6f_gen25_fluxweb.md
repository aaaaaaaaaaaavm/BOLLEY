# A6f — Gen2.5 Fluxweb nonlinear field gate

**What I knew at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear RMS-equivalent magnetostatic FEA  
**Purpose:** I wanted to decide whether sharing the blade thickness between a continuous magnetic backstrap
and the copper ladder removes A6e's local flux concentration without increasing the external
envelope again.

## The correction I froze

Gen2.5 replaces the uniformly perforated Fluxrib with a layered **Fluxweb**. Along each 2.00 mm
axial cage period:

- the 1.25 mm magnetic ligament uses the full 1.12 mm active blade width;
- the 0.75 mm copper-rung region retains a 0.20 mm magnetic backstrap beneath 0.92 mm of copper;
- the axial-average magnetic width is therefore 0.775 mm, or 69.196% of the active blade width;
- the equivalent copper sheet falls from 0.375 to 0.345 mm, retaining 92% of A3g conductance;
- 30 micrometre encapsulation on each side gives 1.18 mm maximum finished width; and
- a 1.58 mm stator slot preserves 0.20 mm nominal side clearance.

The four-face interface becomes 0.31059 kg: 0.14703 kg magnetic matrix, 0.11356 kg copper and
0.05000 kg capture/encapsulation allowance. This misses the unchanged 0.30 kg preference by
10.59 g but passes the 0.40 kg absolute limit by 89.41 g. Relative to Gen2.4, the material exchange
adds only 1.98 g.

The R4 stationary return, 28 mm face, three-turn 81 mm2 primary copper and 1,200 A-turn excitation
are frozen. Phase current is exactly 400 A RMS. Analytical active primary mass is 15.669 kg.

Non-validation 0.30 mm meshes compared 1.10 and 1.12 mm Fluxweb sections and then restored the
1.12 mm candidate from 1,190 to 1,200 A-turn. The selected development point returned about
0.739 T mean field and 1.386 T inferred ligament peak. These outputs selected the point but cannot
pass A6f. This run sheet, inherited formal meshes and every band are frozen first.

## Bands I declared before execution

A6f repeats all 13 A6e magnetic bands unchanged. Physical bands use the worst result from base,
fine and expanded-boundary meshes:

- every mesh mean field must remain 0.72–0.86 T RMS;
- worst inferred magnetic-material peak must be <=1.45 T;
- worst stationary-core peak must be <=1.55 T;
- fine inductance must be 0.68–1.05 times A3g;
- slot imbalance must be <=5% and active-height CV <=15%; and
- the same 2% field, 4% coenergy, 2% boundary, 1e-10 source and 1e-4 nonlinear closure limits
  apply.

The known 0.30 kg preference miss is reported alongside the gate. The 0.40 kg absolute limit is a
hard prerequisite and is closed by frozen geometric accounting.

## What I explicitly did not claim

- The axial magnetic/copper pattern is homogenized into a 2D transverse slice. The backstrap,
  discrete rung edges, end buses and three-dimensional flux crowding are not resolved.
- The 8% conductance reduction has no new transient cage-current, heating or force proof.
- Backstrap-to-rung bonding, electrical isolation, lamination cutting, fatigue, debris, thermal
  expansion and manufacture remain unproven.
- Mass is geometric accounting; B-H curves are screening assumptions; neither is measurement.
- A field pass requires new discrete CAD, circuit closure and transient force evidence.

## Output I required

I required the repository to retain all three meshes, nonlinear histories, worst-mesh extrema, 13 bands and three indexed
figures. A pass promotes only to the Gen2.5 cage/circuit, CAD and transient-force gates.

## What I recorded

**I completed the run on 2026-08-13. I recorded: 13/13 magnetic bands pass; Gen2.5 advances conditionally.**

The base, fine and expanded meshes contain 210,650, 747,114 and 237,770 triangles. Worst mean
field is 0.7383–0.7513 T, inferred magnetic-material peak is 1.4009 T, stationary-core peak is
1.4652 T and fine inductance is 0.8743 times A3g. Base-to-fine mean-field change is 1.758%, below
the frozen 2% band but not by enough to treat the model as final. The interface remains 0.31059 kg
and the 0.30 kg preference remains failed. The [controlled result](../docs/GEN25_FIELD.md) opens
the cage/circuit, CAD and transient-force gates only.
