# A6d — Gen2.3 Fluxrib nonlinear field gate

**State at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear RMS-equivalent magnetostatic FEA  
**Purpose:** decide whether a 14.23 g cooperative-interface change closes A6c without sacrificing
copper rung duty, field floor or stationary-return margin.

## Frozen correction

A6c leaves only the moving magnetic ligament above its band. MMF cannot fall materially without
crossing the field floor. Gen2.3 therefore thickens only the magnetic portion of each passive
Fluxbridge blade:

- active magnetic-rib width grows from 0.94 to 1.06 mm;
- 30 µm encapsulant remains on each side, giving 1.12 mm maximum finished rib width;
- copper rungs remain 0.75 mm axially wide and 1.00 mm thick—conductive duty is not traded away;
- stationary slots grow from 1.40 to 1.52 mm, preserving 0.20 mm rib clearance per side;
- separators become 2.48 mm and outer legs 7.24 mm; the 28 mm face is unchanged.

This is a stepped-thickness passive cage: magnetic ribs are locally thicker than copper rungs.
The active-height copper ladder, buses, 1,200 A-turn primary, R4 manifold and three-turn winding
are unchanged.

Magnetic matrix mass rises 14.23 g. The total four-face payload increment becomes 0.29912 kg,
still below the original 0.30 kg preferred screen. Analytical active primary mass is 15.704 kg.

A non-validation 0.30 mm development mesh was used only to choose the rib width. It cannot pass
A6d. This run sheet, inherited fine/base/expanded meshes and all bands are frozen before output.

## Bands declared before execution

A6d repeats all 13 A6c Boolean bands unchanged. Field range, slot imbalance, active-height CV,
ligament peak, stationary-core peak, source closure and nonlinear closure use the worst of base,
fine and expanded meshes. In particular:

- every mesh mean field must remain 0.72–0.86 T RMS;
- worst inferred magnetic-ligament peak must be <=1.45 T;
- worst stationary-core peak must be <=1.55 T;
- fine inductance must be 0.68–1.05 times A3g; and
- the same 2% field, 4% coenergy and 2% boundary convergence limits apply.

## Explicit non-bands

- The stepped rib has no structural, fatigue, debris, thermal-expansion or manufacturing proof.
- Its mass is geometric accounting, not a measured part.
- B-H inputs remain screening assumptions.
- This remains a magnetostatic slice, not transient induction or axial-force evidence.
- Passing requires new CAD and cage/circuit analysis; Gen2 STEP files do not represent Fluxrib.

## Required output

Commit all three meshes, histories, worst-mesh extrema, 13 bands and three indexed figures. Pass
promotes only to Gen2.3 circuit, transient cage and manufacturing-intent CAD closure.
