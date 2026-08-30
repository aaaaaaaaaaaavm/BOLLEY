# A9c: hot-winding resistance ceiling

**What I know at declaration:** NOT RUN  
**Evidence class:** derived electrical margin from committed A7c/A9b model outputs plus a cited copper temperature coefficient  
**Purpose:** turn P40's narrow energy margin into an exact resistance and ideal-copper temperature ceiling before I choose a winding supplier or thermal state.

## What I freeze

I use the controlling 90% cage-conductance reference cases already committed in A7c:

- 839.74363610016 J at the 1.00 phase-resistance multiplier;
- 893.4120991772224 J at the 1.25 multiplier; and
- A9b's 897.74844054099 J controlling reference result after its nonregenerative selector overhead.

I keep BOL-R-009 unchanged at 900 J.

For the temperature conversion only, I use the IEC standard-copper temperature coefficient at
20 C, 0.00393 /C, reproduced in NIST's *Copper Wire Tables*. This external datum does not establish
the resistance or temperature of a manufactured Bolley winding.

## Calculation I require

1. Recover the A7c source-energy slope per unit phase-resistance multiplier from the committed 1.00x
   and 1.25x corners.
2. Recover the A9 selector source-energy overhead from A9b minus the A7c 1.25x result.
3. Solve for the maximum phase-resistance multiplier that makes the reference source energy exactly
   900 J.
4. Convert that multiplier to the temperature of ideal standard copper whose resistance at 20 C
   exactly equals the model resistance.
5. Report the remaining multiplier and temperature margins above the existing 1.25x A7c corner.

## Acceptance and disposition

I introduce no new performance band. The only physical limit in this run is the existing 900 J
reference-source-energy cap.

The run is numerically valid only if substituting the solved multiplier back into the same linear
energy equation reproduces 900 J to within 1e-9 J. A result below or equal to 1.25x means the A7c
hot corner already consumes the available resistance margin once A9 switching is included. A result
above 1.25x defines a supplier/measurement target; it does not close P40.

## What this cannot establish

- It does not establish winding temperature, manufacturing resistance tolerance, termination
  resistance or cable resistance.
- It does not establish whether the NIST coefficient remains the correct effective coefficient for
  the finished insulated conductor and its joints.
- It does not close semiconductor switching or selector loss. A9b still contains a generic 97%
  inverter-efficiency assumption.
- It does not create hardware evidence.

P40 remains OPEN until measured or supplier-bounded resistance and the real electrical chain stay
below 900 J.
