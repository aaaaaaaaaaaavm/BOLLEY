# A9d: supplier-backed bridge lower-bound screen

**What I know at declaration:** NOT RUN  
**Evidence class:** supplier-datasheet electrical lower bound applied to committed A9b current/energy duty  
**Purpose:** determine whether a real semiconductor bridge can fit inside the loss allowance already hidden by A7c/A9b's generic 97% inverter-efficiency assumption before I spend effort on a selector, busbar, capacitor or cooling design.

## Source duty I freeze

I use A9b's exact controlling duty:

- 897.74844054099 J reference source energy;
- 1,308.4890522592157 J qualification source energy;
- 386.34652118192486 A failed-cell recovery phase-current ceiling;
- 194268.78171293653 A2 reference sum of squared face-channel phase currents; and
- 283151.22877176007 A2 qualification sum.

The shot remains 8 g over 0.90 m with g = 9.81 m/s2.

A7c and A9b divide modeled machine energy by 0.97 for a generic inverter efficiency. I remove that
generic factor before applying supplier-backed bridge conduction loss. I do not add supplier loss
on top of an already-counted 3% allowance.

## Supplier data I freeze

I screen two public supplier families.

`onsemi NXV08H400XT1`

- 80 V APM17-MDC module;
- the supplier states that the two phase outputs may be combined to use the module as one half bridge;
- intended applications include 48 V inverter and 48 V traction;
- maximum 25 C module-path resistance at 160 A is 1.32 mOhm high side and 1.25 mOhm low side;
- switching is characterized at 48 V and 400 A;
- module mass is 23.6 g.

Source: https://www.onsemi.com/download/data-sheet/pdf/nxv08h400xt1-d.pdf

`Infineon IPT015N10N5`

- 100 V OptiMOS 5 TOLL MOSFET for 48-72 V systems;
- 300 A maximum drain current at 25 C;
- 1,200 A maximum pulsed drain current;
- 1.5 mOhm maximum Rds(on) at 10 V and 25 C.

Source: https://www.infineon.com/part/IPT015N10N5

## Candidates

For the onsemi module I evaluate one through four modules in parallel per phase, on each of four
three-phase face channels. Within one module I use the supplier-described combined half bridge as
two equal parallel paths. This equal sharing is an explicit lower-bound assumption.

For the discrete Infineon part I evaluate one through eight equal parallel devices per switch in a
six-switch three-phase bridge on each face. Package, source inductance and sharing error are absent.

## Existing bands and necessary checks

I introduce no new system energy or bus-voltage requirement.

A candidate survives this lower-bound screen only if:

1. its supplier voltage rating is at least the existing 48 V bus;
2. the current per supplier-characterized path does not exceed the current datum used for the
   resistance calculation;
3. bridge conduction plus the A9b non-inverter reference energy remains no more than 900 J; and
4. bridge conduction plus the A9b non-inverter qualification energy remains no more than 1,500 J.

For the onsemi candidate I also report whether the supplier's 400 A / 48 V switching
characterization covers A9b's 386.34652118192486 A fault-current ceiling. For the Infineon discrete
candidate I report its 25 C current and pulse-current coverage separately.

I do not invent an acceptable mass or switching-loss percentage. I report the hardware lower-bound
mass/count and the energy left for every omitted electrical loss.

## What a pass cannot establish

This run omits semiconductor hot Rds(on), switching-frequency loss, gate drive, the nine-cell
selector network, busbar, cable, connectors, capacitor ESR, source impedance, cooling and control
latency. It cannot close P11 or P39.

A candidate that fails here is rejected because the omitted terms can only make its energy result
worse. A candidate that passes remains only a supplier-backed lower bound.
