# A6e — Gen2.4 Fluxrib nonlinear field gate

**What I knew at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear RMS-equivalent magnetostatic FEA  
**Purpose:** I wanted to decide whether one final, bounded cooperative-interface trade closes the A6d
magnetic-ligament miss without sacrificing copper duty, field floor or the absolute payload mass
limit.

## The correction I froze

A6d leaves only the moving magnetic ligament above its band. Gen2.4 makes two coupled corrections:

- active magnetic-rib width grows from 1.06 to 1.14 mm;
- 30 micrometre encapsulant remains on each side, giving 1.20 mm maximum finished rib width;
- copper rungs remain 0.75 mm axially wide and 1.00 mm thick;
- stationary slots grow from 1.52 to 1.60 mm, retaining 0.20 mm rib clearance per side;
- separators become 2.40 mm and outer legs 7.20 mm; the 28 mm face is unchanged; and
- primary excitation falls from 1,200 to 1,190 A-turn RMS, with the same three-turn, 81 mm2
  copper package.

The four-face payload increment becomes 0.30860 kg. This **misses** the 0.30 kg preferred screen
by 8.60 g and passes the unchanged 0.40 kg absolute limit by 91.40 g. The preference is not being
moved or hidden. Analytical active primary mass is 15.658 kg.

Two non-validation 0.30 mm development meshes compared 1,180 and 1,190 A-turn at the frozen
1.14 mm width. They returned approximately 0.729/0.734 T mean field and 1.372/1.369 T inferred
ligament peaks. These values selected the 1,190 A-turn point but cannot pass A6e. This run sheet,
all inherited formal meshes and every field band are frozen before formal output.

## Bands I declared before execution

A6e repeats all 13 A6d Boolean field bands unchanged. Physical field bands use the worst of base,
fine and expanded-boundary meshes:

- every mesh mean field must remain 0.72–0.86 T RMS;
- worst inferred magnetic-ligament peak must be <=1.45 T;
- worst stationary-core peak must be <=1.55 T;
- fine inductance must be 0.68–1.05 times A3g;
- slot imbalance must be <=5% and active-height CV <=15%; and
- the same 2% field, 4% coenergy, 2% boundary, 1e-10 source and 1e-4 nonlinear closure limits
  apply.

The known 0.30 kg preference miss is reported alongside the gate. It is not one of the 13
magnetic bands. The 0.40 kg absolute interface limit remains a hard prerequisite and is already
closed by frozen geometric accounting.

## What I explicitly did not claim

- The stepped rib has no structural, fatigue, debris, thermal-expansion or manufacturing proof.
- Its mass is geometric accounting, not a measured part.
- B-H inputs remain screening assumptions.
- This remains a magnetostatic slice, not transient induction or axial-force evidence.
- A field pass requires new CAD and cage/circuit analysis; Gen2 STEP files do not represent
  Gen2.4.

## Output I required

I required the repository to retain all three meshes, nonlinear histories, worst-mesh extrema, 13 bands and three indexed
figures. Pass promotes only to Gen2.4 circuit, transient cage and manufacturing-intent CAD closure.

## What I recorded

**I completed the run on 2026-08-13. I recorded: 12/13 magnetic bands pass; Gen2.4 is rejected.**

The base, fine and expanded meshes contain 209,000, 743,988 and 236,000 triangles. All declared
bulk numerical differences are below 0.30%. Worst mean field is 0.7376–0.7390 T, stationary peak
is 1.4449 T and fine inductance is 0.8736 times A3g. The controlling inferred ligament maximum is
1.5159 T, 4.55% above the unchanged limit. The 0.30860 kg interface also preserves its separate
8.60 g preferred-mass miss. The [controlled result](../docs/GEN24_FIELD.md) blocks promotion.
