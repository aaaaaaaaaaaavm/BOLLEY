# A9e: sectional-selector realization lower bound

**What I know at declaration:** NOT RUN  
**Evidence class:** topology and supplier-conduction lower bound downstream of A9d  
**Purpose:** find out what the ideal cell selector omitted by A9/A9b costs in series resistance and installed semiconductor count before I attempt a detailed PCB, busbar or control design.

## Geometry and duty I keep

I retain the selected Gen3 machine:

- 27 cells per face and four face channels;
- repeating ABC phase order;
- nine active cells at once, three cells per phase;
- 108 installed cell positions across the four faces;
- one-cell handoff every 45.3 mm; and
- A9b's reference current-squared duty and 0.1514456332038457 s shot time.

I retain A9d's supplier resistance data and its real-electronics energy budget. I do not add a new
energy cap.

## Realization S1: shared face bridge plus per-cell series selector

One three-phase bridge feeds each face. Every installed cell must be independently connectable so
the three active cells per phase can move by one cell at each handoff.

For this lower bound I represent each independently isolatable cell by two back-to-back MOSFET
banks so current can be blocked in both directions while off. Each bank contains N identical
Infineon IPT015N10N5 devices in ideal equal parallel sharing, using the published 1.5 mOhm maximum
25 C Rds(on).

A phase current crosses three selected cell positions. The selector-only effective phase-path
resistance is therefore:

`R_selector = 3 cells * 2 banks * 1.5 mOhm / N`.

For every A9d bridge candidate that already passes its own conduction lower bound, I solve the
smallest integer N that leaves shared-bridge plus selector conduction within the unchanged 900 J
reference cap. I report the resulting installed selector MOSFET count as
`108 cell positions * 2 banks * N`.

This is a lower bound. It omits selector switching loss, package and bus resistance, gate drive,
current-sharing error, cooling and clearance.

## Realization S2: local bridge per ABC module

I group the 27 cells on a face into nine consecutive ABC modules. I install one three-phase bridge
at every module, so four faces contain 36 local bridges. Three modules per face are active at once.
This removes a separate series selector but duplicates bridge conduction in the three active
modules.

Using the onsemi NXV08H400XT1 combined-half-bridge resistance from A9d, I solve the minimum number
of parallel modules per phase in every local bridge that keeps 25 C bridge conduction inside the
same 900 J reference cap. I report installed APM17 module count and module-only mass.

This realization changes A9's electrical partition but not its one-cell spatial handoff. It remains
a lower bound because switching, bus, gate drive, local capacitance and cooling are absent.

## Disposition

I introduce no arbitrary switch-count or mass threshold. The run reports whether either realization
can meet the existing energy cap at all and what its minimum supplier-hardware burden is.

Neither realization can close P11, P38 or P39 without a complete switching/control/package model.
If the required counts are large, I will treat that as evidence that the sectional architecture,
not a missing component choice, is the next redesign target.
