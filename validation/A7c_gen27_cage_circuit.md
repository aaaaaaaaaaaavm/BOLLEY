# A7c — selected Gen2.7 Fluxrelay cage/circuit reclosure

**What I knew at declaration:** NOT RUN  
**Evidence class:** post-field homogenized cage + lumped sectional circuit/CG shot model  
**Purpose:** I want to replace A8b's field and inductance surrogates in the exact selected point
without reopening the search or relaxing its bands.

## The point I froze

I allow only `n27_p45.3_I380_A10.4` into A7c. I retain its 27 cells per face, 45.3 mm pitch,
318.6 mm five-lane cage, 10.4 mm2 four-turn winding, 380 A phase current, 1.2231 m installed
primary, 0.37136 kg interface and conservative nine-cell active window.

I replace only these A8b surrogates:

- tooth and equivalent-sheet field come from A6h's minimum three-mesh mean field;
- moving and stationary material checks use A6h's worst three-mesh peaks; and
- active-window phase inductance becomes A6h's fine 4.81156 uH result.

I retain A8b's active-window phase resistance and installed/energized mass split.

## The corners I declared before execution

I repeat the four A8b corners: 90/100% cage-sheet conductance crossed with 100/125% active-window
phase resistance. At every corner I evaluate both 4 kg reference and 6 kg qualification payloads
over the same 21 by 21 transverse-CG grid, for 3,528 retained point records.

## The bands I kept

I keep all 29 A8b hard bands. I replace only the names of the four field-surrogate bands with the
fresh A6h field values. The controlling limits remain:

- 0.20–0.336 m cage length, 2.25 mm endpoint guards and a whole three-phase cell lattice;
- interface <=0.40 kg and all installed active primary <=16.0 kg;
- phase current <=400 A, MMF <=1,600 A-turn, current density <=40 A/mm2 and slot fill <=60%;
- solved mean field 0.72–0.86 T, moving material <=1.45 T and stationary core <=1.55 T;
- required link <=48 V with >=10% margin;
- reference/qualification source energy <=900/1,500 J;
- source efficiency >=30%, secondary efficiency >=50% and peak power <=15 kW;
- primary/cage copper rise <=3/20 K, cage current density <=180 A/mm2, slip <=8 m/s and terminal
  frequency <=350 Hz; and
- 1% opposed-field mismatch leaves <=100 N unbalanced normal force.

The 0.25/0.30 kg interface figures remain failed preferences, not substitute pass bands.

## What I explicitly do not claim

- I still homogenize the passive ladder; discrete rungs, end buses and current crowding are absent.
- I still use a quasi-steady prebiased shot law; switching, cell handoff, force ripple and finite
  axial ends are absent.
- A7c cannot validate force, structure, containment, thermal cycling, release or flight behavior.
- A pass opens only provisional Gen3 CAD and a transient sectional-drive gate.

## The output I require

I require all four corner summaries, both payload cases, every 21 by 21 CG record, all 29 Boolean
bands, the exact A6h field/inductance trace and a deterministic disposition. I will not change the
selected geometry, model equations, corners or thresholds after seeing the result.

## What I recorded

I completed A7c on 14 August 2026 without changing the selected point, model, corners or bands.
Every one of the four robustness corners passes all **29/29** hard bands.

| Controlling quantity | Result | Band | Outcome |
|---|---:|---:|---:|
| 90% conductance / 125% resistance reference energy | 893.412 J | <=900 J | PASS |
| Same-corner qualification energy | 1,302.169 J | <=1,500 J | PASS |
| Minimum source efficiency | 34.559% | >=30% | PASS |
| Minimum secondary efficiency | 51.074% | >=50% | PASS |
| Maximum cage rise | 15.593 K | <=20 K | PASS |
| Maximum cage current density | 151.777 A/mm2 | <=180 A/mm2 | PASS |
| Maximum slip | 5.693 m/s | <=8 m/s | PASS |
| Maximum required DC link | 13.049 V | <=48 V | PASS |
| Maximum peak DC power | 11.676 kW | <=15 kW | PASS |

The fresh A6h reclosure lowers my controlling A8b reference-energy estimate by 2.054 J. The exact
point now has 6.588 J, or 0.732%, of model margin on the 900 J reference band. I promote it only to
provisional A5e Gen3 CAD and A9 transient sectional-drive modelling. I do not use this pass as
permission to claim hardware force, thermal or release performance.

Artifact: `analysis/results/gen27_cage_circuit_points.csv.gz`  
Records: 3,528  
SHA-256: `6ebc692f4dbff50ca04c8d7f1f21ed7929a57febbc44209a0f779253d5d60116`
