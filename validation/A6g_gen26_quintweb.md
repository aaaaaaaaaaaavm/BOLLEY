# A6g — Gen2.6 Quintweb nonlinear field gate

**State at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear RMS-equivalent magnetostatic FEA  
**Purpose:** determine whether a fifth layered blade can add the passive active area A7a needs
without losing the transverse field solution or exceeding the absolute payload mass limit.

## Frozen correction

Gen2.6 **Quintweb** retains the Gen2.5 blade section and adds one blade per face:

- five blade centres at -8, -4, 0, 4 and 8 mm;
- 1.12 mm active magnetic web, 0.20 mm backstrap, 0.92 mm copper rungs and 1.58 mm slots;
- 25% more active cage area than Gen2.5;
- 31 mm stationary face, 6.71 mm outer legs, four 2.42 mm separators, 7 mm yoke and R4 haunch;
- four 20.25 mm2 turns at 375 A RMS, giving 1,500 A-turn with the same 81 mm2 slot copper; and
- 15.857 kg analytical active primary mass.

Payload material scales from sixteen to twenty blades. Magnetic matrix is 0.18378 kg, cage copper
0.14195 kg and the capture/encapsulation allowance is conservatively scaled from 0.0500 to
0.0625 kg. Total interface increment is 0.38823 kg. The 0.25 kg target and 0.30 kg preference fail
by 138.23 and 88.23 g; the 0.40 kg absolute limit passes by only 11.77 g.

Non-validation 0.30 mm meshes rejected the original 28 mm/1,200 A-turn five-lane point, then
compared 30, 31 and 32 mm return faces at 1,500 A-turn. The selected 31 mm point returned about
0.740 T mean field, 1.253 T moving-material peak, 1.447 T core peak and 1.296 times A3g per-cell
inductance. Those development values chose the point but cannot pass A6g.

## Bands declared before execution

A6g retains the same worst-of-three-mesh physical rules and 13 Boolean bands used by A6f, with
one predeclared drive-informed change: maximum per-cell inductance becomes 1.40 times A3g instead
of 1.05. A7a found only 15.37 V required against a 48 V link, and the four-turn Quintweb circuit
must be reclosed after this solve. All other limits remain:

- every mesh mean field 0.72–0.86 T RMS;
- moving magnetic-material peak <=1.45 T and stationary-core peak <=1.55 T;
- per-cell inductance >=0.68 times A3g;
- slot imbalance <=5% and active-height CV <=15%; and
- 2% field, 4% coenergy, 2% boundary, 1e-10 source and 1e-4 nonlinear closure limits.

## Explicit non-bands

- The five axial cage patterns remain homogenized in a transverse 2D slice.
- The 31 mm stationary face and five slots have no routed winding or assembly CAD.
- Passing does not close A7a; five-lane cage energy, temperature and current need A7b.
- The 11.77 g absolute mass margin is accounting, not a weighed retained assembly.
- Structure, tolerance, debris, magnetic compatibility, switching and force remain open.

## Required output

Commit all three meshes, nonlinear histories, worst-mesh extrema, 13 bands and three indexed
figures. A pass opens five-lane cage/circuit reclosure and Gen3 CAD only.
