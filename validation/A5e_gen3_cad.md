# A5e — exact Gen3 Fluxrelay nominal CAD gate

**What I knew at declaration:** NOT RUN  
**Evidence class:** parametric CAD, exact nominal solid intersection, analytical volume check and
deterministic STEP/STL package  
**Purpose:** I want to prove that the exact A6h/A7c-passing point exists as traceable Gen3 geometry
before I spend effort on tolerance, structure or transient drive detail.

## The source I froze

- Selected point: `n27_p45.3_I380_A10.4`.
- Controlled dimensions: `cad/gen3_parameters.json`.
- Payload cage: five lanes per face, 318.6 mm active length, 2.25 mm aft start.
- Primary: 27 cells per face, 45.3 mm pitch, 1.2231 m installed length.
- Winding: four 10.4 mm2 turns per cell represented by a volume-matched 5.2 × 8.0 mm copper pack.
- Sectional window: nine cells, three per phase.

## The objects I require

1. Full four-face Fluxrelay interface on my 3U payload proxy.
2. Bar-resolved 100 mm lane coupon with fifty 2 mm web/rung periods and explicit side skins.
3. One complete 27-cell, three-phase stator cassette.
4. One distinct nine-cell sectional active-window cassette.
5. One two-cell winding/core/cage coupon resolving both alternating coil layers.
6. Track, open frame and retained-state gate.
7. Full four-face retained assembly and a 900 mm endpoint-engagement arrangement.
8. Eight STEP masters, eight derived STLs and at least ten indexed renders.

## The 17 bands I declared before generation

| ID | Band | What I do if it fails |
|---|---|---|
| A5e-1 | A6h and A7c remain passing upstream results. | Stop the CAD promotion. |
| A5e-2 | Payload proxy is 340.5 × 100 × 100 mm with 8.5 mm rails. | Reject my proxy. |
| A5e-3 | Finished Fluxrelay projection is <=6.5 mm. | Reject my interface. |
| A5e-4 | Five 1.18 mm lanes align with five 1.58 mm slots at >=0.20 mm nominal side clearance. | Reject lane/stator fit. |
| A5e-5 | Core face <=32 mm; active length 1,223.1 mm; 27 cells at 45.3 mm pitch. | Reject my cassette. |
| A5e-6 | Cage is 318.6 mm from x=2.25 mm and retains >=2.25 mm guard after 900 mm travel. | Reject my axial package. |
| A5e-7 | The sectional window contains exactly nine cells and three per phase. | Reject my sectional representation. |
| A5e-8 | Two-sided gross slot fill remains <=60%. | Reject my winding package. |
| A5e-9 | Alternating copper packs clear lane tips by >=0.50 mm and do not overlap adjacent coils or core. | Reject my route. |
| A5e-10 | Payload/interface intersects all four cores and coils by <=1e-6 mm3 nominally. | Reject nominal fit. |
| A5e-11 | Open muzzle is >=130 mm and the frame stays <=160 mm. | Reject launcher envelope. |
| A5e-12 | Four faces surround the payload and departure is +x. | Reject my arrangement. |
| A5e-13 | The coupon contains fifty periods, two cells, both coil layers, magnetic web and copper rungs. | Reject detail evidence. |
| A5e-14 | Interface stays <=0.40 kg and installed active primary stays <=16.0 kg. | Reject the selected point. |
| A5e-15 | At least eight STEP, eight STL and ten render artifacts exist. | Reject an incomplete package. |
| A5e-16 | Every master records hash, size, solids, volume and bounds. | Reject untraceable exports. |
| A5e-17 | CAD copper volume agrees with A8b installed copper volume within 0.5%. | Reject mass/geometry inconsistency. |

## What I explicitly do not claim

- My 0.20 mm nominal lane clearance is not a tolerance stack.
- Copper packs do not resolve individual turns, insulation, impregnation, leads or terminals.
- Full-length lanes remain homogenized; only the coupon resolves webs, rungs and side skins.
- Structure, containment, fasteners, cooling, sensors, cabling, power electronics and gate
  actuation remain absent.
- My 92 g active-material margin is not an allowance for those missing systems.
- A pass is not a manufacturing release or launch-provider acceptance.

## The output I require

I require reproducible source, STEP/STL masters and archives, a build manifest, exact intersections,
ten inspected views, dimensions, BOM, all 17 Boolean bands and my manual-detail ledger. A pass may
open tolerance, structure and A9 work only.
