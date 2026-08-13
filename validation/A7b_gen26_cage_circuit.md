# A7b — Gen2.6 Quintweb cage/circuit reclosure

**State at declaration:** NOT RUN  
**State after execution:** MODELLED — REJECT EXACT GEN2.6 CIRCUIT POINT  
**Evidence class:** post-field homogenized cage + lumped circuit/CG shot model  
**Purpose:** decide whether 25% more passive active area closes every A7a translator failure
without moving its thresholds.

## Frozen model

A7b repeats the A7a model and all its corners with these controlled substitutions only:

- A6g minimum three-mesh tooth field and maximum three-mesh phase inductance;
- five Fluxweb blades per face instead of four;
- 0.38823 kg interface with 0.14195 kg cage copper and 0.18378 kg magnetic matrix;
- four 20.25 mm2 turns at 375 A RMS and 1,500 A-turn;
- 15.857 kg active primary and the A3g four-turn phase resistance; and
- five-blade active area in force density, cage heat and normal-force calculations.

Every 21 by 21 CG point is evaluated for 4 kg reference and 6 kg qualification payloads. The same
four corners combine 90/100% cage conductance and 100/125% phase resistance. No development
A7b result was used to select another parameter.

## Bands declared before execution

All 19 A7a hard bands are unchanged, including:

- interface <=0.40 kg and active primary <=16.0 kg;
- current <=400 A, current density <=40 A/mm2 and slot fill <=60%;
- <=48 V with >=10% link margin;
- reference/qualification source energy <=900/1,500 J;
- source efficiency >=30%, secondary efficiency >=50% and peak power <=15 kW;
- primary/cage copper rise <=3/20 K;
- cage current density <=180 A/mm2, slip <=8 m/s and terminal frequency <=350 Hz; and
- 1% opposed-field mismatch leaves <=100 N net normal force.

The 0.25 kg target and 0.30 kg preference remain separate failed preferences.

## Explicit non-bands

- This is the same quasi-steady homogenized cage law that failed A7a, not transient FEA.
- Discrete rung current crowding, end buses, switching, finite ends and force ripple remain absent.
- The added blade has field evidence but no structural, tolerance or retained-mass CAD evidence.
- A pass cannot close P29 or validate the machine.

## Required output

Commit all four corners, both payload cases, all 3,528 CG/corner/payload point records, 19 bands
and both preference failures. A pass opens Gen3 CAD and transient-force work only.

### Execution correction declared before a completed run

The first command stopped before cage or shot calculation because the wrapper loaded only the
Gen2.6 child field-parameter file and did not resolve its inherited Gen2.5 magnetic fraction. No
A7b value was produced. The shared loader was corrected to resolve parent files recursively with
cycle detection. No geometry, field result, corner, model equation or band changed.

## Committed result

The corrected run produced all 3,528 declared records. Two nominal-resistance corners pass all
19 bands. The two 125% phase-resistance corners pass 18/19 and fail only reference source energy.

| Controlling quantity | Result | Band | Outcome |
|---|---:|---:|---:|
| 90% conductance / 125% resistance reference energy | 959.923 J | <=900 J | **FAIL** |
| 100% conductance / 125% resistance reference energy | 929.432 J | <=900 J | **FAIL** |
| Qualification source energy | 1,397.421 J | <=1,500 J | PASS |
| Minimum source efficiency | 32.289% | >=30% | PASS |
| Minimum secondary efficiency | 51.578% | >=50% | PASS |
| Maximum cage rise | 14.528 K | <=20 K | PASS |
| Maximum cage current density | 146.505 A/mm2 | <=180 A/mm2 | PASS |
| Maximum slip | 5.579 m/s | <=8 m/s | PASS |
| Maximum required DC link | 18.244 V | <=48 V | PASS |
| Maximum peak DC power | 12.354 kW | <=15 kW | PASS |

The five-lane translator closes all four A7a translator failures. The remaining robustness miss
tracks phase resistance only. Gen2.6 therefore retains A6g field evidence but is not promoted to
CAD or transient force as a closed operating point.

Artifact: `analysis/results/gen26_cage_circuit_points.csv.gz`  
Records: 3,528  
SHA-256: `f7dc7a03560ab90474276f8b6447f285cbec5cb6890eee4faa1d65949d4d8163`
