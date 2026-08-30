# A9b: sectional-drive residual reclosure

**What I know at declaration:** NOT RUN  
**Evidence class:** numerical reclosure of the committed A9 time-domain sectional-drive model  
**Purpose:** determine whether A9's two force-sign failures are entirely below the residual floor already declared in `analysis/common.py`.

## What I freeze

I inherit A9 unchanged:

- the exact selected Gen3 Fluxrelay geometry and A7c corners;
- 27 cells per face, nine active-cell equivalents and 18 one-cell handoffs;
- 380 A rated current and the A6h 4.8115568374163385 uH active-window inductance;
- cosine/sine current transfer over one cell pitch;
- zero regeneration credit for outgoing magnetic energy;
- 100 and 200 samples per handoff;
- the full 21 by 21 transverse-CG envelope;
- the single-failed-cell full-force recovery policy; and
- all 13 A9 physical acceptance bands.

I do not change the 900 J reference-energy cap, 1,500 J qualification-energy cap, 400 A current
cap, 48 V link cap, 15 kW power cap, 8 g acceleration cap or any departure-state limit.

## The only permitted correction

Before evaluating `healthy_axial_force` and `failed_cell_axial_force`, I apply
`analysis.common.snap_residual` to each reported minimum channel force.

`common.py` already declares `RESIDUAL_FLOOR = 1e-9` and documents that it is the same floor used by
the force-allocation constraint checks. A9's controlling residual is
-1.4210854715202004e-14 N, more than four orders of magnitude below that existing floor.

No new tolerance is introduced by A9b.

## Bands

A9b passes only if:

1. both A9 resolutions produce the same 13 Boolean outcomes after the declared residual snap;
2. all 13 unchanged A9 bands pass;
3. the fine-run controlling electrical and departure-state quantities are unchanged from the
   preserved A9 execution apart from force values snapped within the existing residual floor; and
4. every unsnapped minimum force with magnitude at or above 1e-9 N remains visible and is evaluated
   without alteration.

## What a pass means

A pass may move P38 to MODELLED only for the ideal-current-tracking selector effects represented by
A9. It does not close supplier switching loss or hot resistance (P11/P40), discrete-cage and 3D end
fields (P29), packaged mass (P39), EMC, structure, thermal cycling or six-degree-of-freedom
separation.

I will preserve A9's 11/13 failure record even if A9b passes.
