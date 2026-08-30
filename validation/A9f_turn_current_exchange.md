# A9f: turn/current exchange for a local-bridge Fluxrelay stator

**What I know at declaration:** NOT RUN  
**Evidence class:** scaled electromagnetic/circuit architecture screen with supplier-backed 25 C bridge resistance  
**Purpose:** test whether the selector burden exposed by A9e is caused by the selected 4-turn/380 A electrical partition rather than by Fluxrelay's passive-secondary geometry itself.

## What remains fixed

I keep the selected Gen3 mechanical and magnetic geometry, 1,520 A-turn rated MMF, 27-cell lattice,
318.6 mm passive cage, four face channels and 0.90 m powered travel.

I do not change the 900 J reference-energy cap, 1,500 J qualification-energy cap, 400 A phase-current
cap or 48 V link. I restore A7c's inherited 10% healthy DC-link margin recorded in ADR-053. Fault
link demand remains at most 48 V.

## Search I declare

I evaluate integer turn counts from 4 through 13 inclusive.

For N turns per cell:

- phase current is 1,520/N A;
- conductor area per turn is 10.4*(4/N) mm2;
- phase resistance and phase inductance scale with (N/4)^2;
- total slot copper, current density, MMF and ideal winding I2R loss remain unchanged;
- A9b healthy and fault link-voltage demand scale with N/4; and
- supplier bridge conduction scales with current squared.

The field-equivalence statement is a screen, not new field evidence. A selected point must return to
nonlinear field and CAD/winding checks because the turn packing and current distribution have
changed.

## Electrical realization

I use the A9e local-bridge arrangement: one three-phase bridge at every ABC module, 36 installed
bridges and three active modules per face.

For each turn count I choose the smallest integer number of parallel onsemi NXV08H400XT1 modules
per phase per local bridge that:

1. keeps current in each supplier-characterized internal path at or below 160 A;
2. keeps reference source energy at or below 900 J after replacing the generic 97% inverter loss
   with 25 C module conduction; and
3. keeps qualification source energy at or below 1,500 J.

The turn candidate then also has to satisfy:

4. phase current <=400 A;
5. healthy required link <=48 V with at least 10% margin by the A7c definition; and
6. failed-cell required link <=48 V.

## Selection rule

Among candidates that pass every band I first minimize installed supplier power-module mass. If
several turn counts require the same module count, I minimize the largest normalized demand among:

- reference source energy / 900 J;
- healthy required link / (48/1.10 V);
- failed-cell required link / 48 V; and
- phase current / 400 A.

A remaining tie goes to fewer turns.

I declare that rule before execution so I cannot select whichever turn count looks nicest later.

## What a pass cannot establish

- The N-turn winding has not been drawn, routed or field-solved.
- Supplier hot Rds(on), switching loss, gate drive, DC-link capacitance, busbar, cable and cooling
  remain absent.
- Module-only mass is not packaged electrical mass.
- Local bridge faults, timing skew and EMC remain open.
- No hardware exists.

A pass may select one electrical architecture point for fresh field, winding-CAD, switching and
packaged-mass closure. It cannot close Gen4 by itself.
