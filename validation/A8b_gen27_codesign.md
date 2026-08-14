# A8b — Gen2.7 Fluxrelay axial/electrical co-design

**State at declaration:** NOT RUN  
**Evidence class:** coupled deterministic design-space search using A6g field surrogates and the
A7b cage/circuit equations  
**Purpose:** find whether the five-lane interface can close full axial engagement, installed mass
and the hot-energy corner together.

## Frozen correction

Fluxrelay retains the Gen2.6 transverse cross-section and changes only the axial/electrical
architecture:

- the five active lanes stay anchored 2.25 mm from the aft payload face and may shorten at the
  forward end;
- the stator must retain 2.25 mm nominal overlap guard after 900 mm travel;
- each candidate contains a whole three-phase cell lattice;
- only cells intersected by the cage are energised; installed cells remain in the 16 kg mass; and
- active-window resistance, inductance, loss and copper temperature use the conservative maximum
  simultaneous cell count.

The finite grid contains 3 cell counts, 17 pitches, 4 rated currents and 14 conductor areas:
**2,856 candidates** before geometric rejection. The four A7b conductance/resistance corners and
both 21 by 21 CG grids are evaluated for every candidate that passes the precheck.

## Bands declared before execution

The search preserves the A7b hard bands and adds the missing axial/installed-field conditions:

- active cage length 0.20–0.336 m, inside 340.5 mm with 2.25 mm guards at both travel ends;
- total cell count divisible by three;
- interface <=0.40 kg and installed active primary <=16.0 kg;
- current <=400 A, MMF <=1,600 A-turn, primary current density <=40 A/mm2 and slot fill <=60%;
- A6g current-scaled mean field 0.72–0.86 T, moving material <=1.45 T and stationary core
  <=1.55 T;
- <=48 V with >=10% link margin;
- reference/qualification source energy <=900/1,500 J;
- source efficiency >=30%, secondary efficiency >=50% and peak power <=15 kW;
- primary/cage rise <=3/20 K, cage current density <=180 A/mm2, slip <=8 m/s and terminal
  frequency <=350 Hz; and
- 1% opposed-field mismatch leaves <=100 N unbalanced normal force.

The 0.25/0.30 kg interface targets remain preferences, never substitutes for 0.40 kg.

## Selection rule

Among candidates passing every hard band, minimise the largest normalized continuous-band demand.
Tie-break on lower installed active-primary mass, then lower hot-corner reference energy, then
candidate ID. Exact geometry Booleans do not create a zero-margin selection artefact.

## Explicit non-bands

- A6g field values are linearly scaled with current. A pass must be followed by a fresh nonlinear
  field gate.
- Per-cell inductance is not forced below A6g's old series-chain band; the active-window phase
  inductance and direct DC-link calculation control the sectional drive.
- Axial end fields, cell handoff, inverter count, force ripple and switching are absent.
- The retained cage remains homogenized and the installed-mass model excludes structure,
  containment, cooling and power electronics.

## Required output

Commit every candidate, all evaluated corner summaries, CG count, hard-band vector, continuous
demand vector, feasible set and deterministic selection. A pass freezes one point for A6h field,
A7c selected-point reclosure and only then Gen3 CAD.

## Recorded result

**Run completed 2026-08-13. Result: 77/2,856 candidates pass every declared hard band; promote
one selected analytical point to A6h and A7c.**

The deterministic minimax selection is `n27_p45.3_I380_A10.4`: 27 cells per face channel,
45.3 mm pitch, 380 A rated phase current and 10.4 mm2 conductor area per turn. It produces a
1.2231 m installed stator, a 318.6 mm cage, 2.25 mm guards at both travel endpoints and a
maximum sectional window of nine cells / three cells per phase.

The selected point uses 15.9081 kg installed active primary and adds 0.37136 kg to the payload.
Active-window phase resistance is 0.78725 times A7b. The hot 90%-conductance / 125%-resistance
reference corner uses 895.467 J and the worst qualification corner uses 1,305.163 J. The three
tightest continuous demands are reference energy 0.99496, installed active-primary mass 0.99426
and predicted stationary-core peak 0.98965.

The current-scaled stationary peak is 1.53395 T and is not a fresh field result. A8b therefore
closes its coupled analytical question but does not release hardware or final CAD. A6h nonlinear
field and A7c selected-point reclosure remain mandatory.

Every candidate is retained in deterministic gzip JSON at
`analysis/results/gen27_codesign_candidates.json.gz`, SHA-256
`2ad36b89d32acd9c6fe76b1644d1f53de2f9e4de23c263eed554cb2c0808b378`.
