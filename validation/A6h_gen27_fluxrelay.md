# A6h — selected Gen2.7 Fluxrelay nonlinear field gate

**What I knew at declaration:** NOT RUN  
**Evidence class:** independently meshed 2D nonlinear RMS-equivalent magnetostatic FEA  
**Purpose:** I wanted to replace A8b's linear current-scaled field and inductance surrogates before
I allowed the selected Fluxrelay point to enter A7c or Gen3 CAD.

## The selected point I froze

I allowed exactly one A8b candidate into A6h: `n27_p45.3_I380_A10.4`.

- Retain Gen2.6's 31 mm five-lane transverse section, nonlinear material assumptions and three
  formal meshes.
- Change phase current from 375 to 380 A and MMF from 1,500 to 1,520 A-turn.
- Change conductor area from 20.25 to 10.4 mm2 per turn while retaining the same 81 mm2 smeared
  field-source window; physical current density is checked by A8b, not hidden in the field source.
- Change the out-of-plane tooth depth from 15.0 to 22.65 mm, exactly half the selected 45.3 mm
  cell pitch.
- Evaluate three energized cells per phase, matching A8b's conservative nine-cell moving window.

I changed no transverse core, slot, gap, passive-blade, B-H, solver or mesh dimension.

## Bands I declared before execution

I retained the physical and numerical A6g bands:

- every mesh mean field 0.72–0.86 T RMS;
- moving magnetic-material peak <=1.45 T and stationary-core peak <=1.55 T;
- slot imbalance <=5% and active-height coefficient of variation <=15%; and
- 2% field, 4% coenergy, 2% boundary, 1e-10 source and 1e-4 nonlinear closure limits.

I replaced the legacy per-cell/A3g inductance band before the run. The A8b active-window phase
inductance is 4.95297 uH; I require A6h to return 0.85–1.15 times that value on the fine mesh. I
treat this as a surrogate-agreement gate, not a DC-link calculation. I reserve voltage, energy and
heat for A7c.

## What I explicitly did not claim

- The five passive lanes and axial bar pattern remain homogenized.
- A 2D tooth slice cannot resolve axial end fields, cell handoff, force ripple or current crowding.
- The 15.908 kg installed active-material figure excludes structure, cooling, wiring and power
  electronics.
- Passing does not validate force or release performance and does not make the CAD flight-ready.

## Output I required

I required the repository to retain all three meshes, nonlinear histories, worst-mesh extrema,
the fine active-window phase inductance, all 13 Boolean bands and three indexed figures. A pass
opens only A7c and provisional Gen3 geometry.
