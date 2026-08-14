# A3g — robust Fluxbridge pitch, field and copper optimisation

**What I knew at declaration:** NOT RUN  
**Evidence class:** constrained analytical design-space search using the A3f model  
**Purpose:** I wanted to replace A3f's first passing point with the lowest-energy point that remains physically
wound and passes at deliberately worse clearance, cage conductance and core-H corners.

## The search I froze

The payload-side Fluxbridge geometry, passive-cage materials, 8 g duty, 0.90 m powered stroke,
four-face force allocation and all A3f loss equations remain fixed.

I varied only:

- cell pitch from 16 to 30 mm using eight declared pitch/cell-count pairs;
- 50% tooth duty, so tooth and winding-slot widths each follow half the pitch;
- equivalent sheet field from 0.44 to 0.62 T RMS in 0.02 T steps; and
- copper area, set by a 60% two-sided gross slot fill with four turns per cell.

Electrical wavelength is three cell pitches. Mean turn length is frozen as
$2(p+14\ \mathrm{mm})$. Every cell count is divisible by three; active lengths remain between
0.90 and 0.94 m.

Every nominal candidate must also survive all eight combinations of:

- 0.20 and 0.25 mm clearance per side;
- 90% and 100% of nominal cage sheet conductance; and
- 100% and 150% of the conservative stationary-core H input.

I froze the complete search in `cad/fluxbridge_optimization.json`.

## The selection rule I declared before execution

1. Reject any candidate that fails any band at nominal or at any robustness corner.
2. Among surviving candidates, minimise the maximum qualification source energy across all CG
   points and robustness corners.
3. Break an exact tie with lower active primary mass, then lower equivalent field.

No weighted score and no post-result preference are permitted.

## Bands I declared before execution

| ID | Band at every declared corner | Failure action |
|---|---|---|
| A3g-1 | Active length is 0.90–0.94 m and cell count is divisible by three. | Reject geometry. |
| A3g-2 | Ligament field <=1.45 T and MMF <=1,800 A-turn. | Reject magnetic point. |
| A3g-3 | Phase current <=450 A and primary current density <=40 A/mm². | Reject winding point. |
| A3g-4 | Two coil sides occupy <=60% of the winding slot. | Reject winding point. |
| A3g-5 | Active primary copper + core <=12 kg. | Reject mass point. |
| A3g-6 | Required DC link <=48 V with >=10% margin on 48 V nominal. | Reject drive point. |
| A3g-7 | Source energy <=1.00 kJ reference and <=1.50 kJ qualification. | Reject energy point. |
| A3g-8 | Source-to-payload efficiency >=30%. | Reject efficiency point. |
| A3g-9 | Peak DC power <=15 kW. | Reject source point. |
| A3g-10 | Primary copper rise <=3 K and cage rise <=20 K per shot. | Reject thermal point. |
| A3g-11 | Cage current density <=180 A/mm² and slip <=8 m/s. | Reject cage point. |
| A3g-12 | Secondary-only efficiency >=50%. | Reject cage point. |
| A3g-13 | Terminal frequency <=350 Hz. | Reject drive point. |
| A3g-14 | One-percent field mismatch leaves <=100 N unbalanced normal force. | Reject centring point. |

Paired limits are executable separately. A candidate that passes nominal but fails one corner is
not feasible.

## What I explicitly did not claim

- This search cannot cure homogenization error, 3D leakage, cogging, bar current crowding or end
  effects because A3f does not contain them.
- Winding fill is a cross-sectional test, not a routed end-turn drawing.
- The selected supplier, insulation system, cooling method, switching hardware and structural
  frame remain unresolved.
- A numerically optimal candidate is not a manufacturing release or provider-approved interface.

## Output I required

Report every candidate and corner, rejection reasons, selected pitch/cell count/wavelength/field,
winding area and fill, magnetic circuit, active mass, both shot partitions, worst corner, all
bands and the exact deterministic selection key. A passing selection proceeds to Gen2 CAD and
independent field analysis.
