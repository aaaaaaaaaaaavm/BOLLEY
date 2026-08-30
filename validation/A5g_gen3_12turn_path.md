# A5g Gen3 12-turn path-corrected winding

Date frozen: 2026-08-31

State: DECLARED, NOT RUN

## Question

A5f rejected the 12-turn point because four nested turns around the fixed 40.1 x 8.8 mm inner opening increase mean turn length and copper volume. The wire envelopes themselves had feasible nominal-fit points.

A5g changes one geometric quantity. I keep the 8.8 mm inner transverse opening and solve the inner axial opening required to restore A5e's 118.6 mm mean turn length for each frozen wire-width candidate. I do not change current, MMF, copper cross-section, insulation screen, stator core, cage, pitch or radial layer count.

## Controlled inputs

- 12 turns per cell;
- 126.66666666666667 A RMS;
- 1,520 A-turn RMS;
- 3.466666666666667 mm2 bare copper per turn;
- 41.6 mm2 bare copper per coil side;
- 118.6 mm target mean turn length;
- 4,933.76 mm3 target copper volume per cell;
- four nested in-plane turns by three radial layers;
- 8.8 mm fixed inner transverse opening;
- 45.3 mm cell pitch;
- 22.65 mm tooth axial width;
- the same 2.00 to 2.80 mm bare-width search and Grade 2 insulation envelope as A5f.

For four nested in-plane turns with gross insulated conductor thickness `T`, their mean centreline length is

`2 * (inner_axial + 8.8 + 8*T)`.

I therefore solve

`inner_axial = 59.3 - 8.8 - 8*T`

for every candidate. This is a path-length closure, not another free optimization variable.

## Selection rule

Among candidates passing every hard band, I select in this order:

1. minimum total gross insulated conductor-envelope area per coil side;
2. maximum smaller radial clearance between alternating coil layers and between the upper layer and back yoke;
3. maximum minimum axial separation to the same-cell and neighbouring core;
4. smaller nominal bare width.

I will not change this rule after execution.

## Hard bands

| Band | Criterion | Source |
|---|---:|---|
| Turns | exactly 12 | A9f |
| Excitation | exactly 1,520 A-turn RMS | A6h/A9f |
| Copper current density | <= 40 A/mm2 | inherited A8b/A5e |
| Bare cross-section identity | <= 1e-12 relative error from 41.6 mm2 | A9f |
| Detailed copper volume | <= 0.5% relative error from 4,933.76 mm3 | inherited A5e |
| Mean turn length | <= 0.5% relative error from 118.6 mm | A5e geometry identity |
| Gross insulated slot fill | <= 60% | inherited A5e |
| Coil to Fluxrelay | >= 0.5 mm | inherited A5e |
| Same-cell core axial separation | >= 0 mm | nominal non-interference |
| Neighbouring-core axial separation | >= 0 mm | nominal non-interference |
| Inter-layer radial clearance | >= 0 mm | nominal non-interference |
| Upper coil to back yoke | >= 0 mm | nominal non-interference |
| Same-layer axial clearance | >= 0 mm | nominal non-interference |

## Evidence boundary

A5g remains an analytical winding-envelope screen. A pass permits detailed BRep winding CAD and source-window bookkeeping; it does not prove supplier availability, winding manufacture, bend strain, insulation life, lead routing, bridge packaging, hot resistance, switching loss, cooling or vibration survival.

The 4-turn Gen3 CAD baseline remains authoritative until a later detailed-CAD gate promotes a replacement.
