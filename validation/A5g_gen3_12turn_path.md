# A5g Gen3 12-turn path-corrected winding

Date frozen: 2026-08-31

State: MODELLED, PASS

## Question

A5f rejected the 12-turn point because four nested turns around the fixed 40.1 x 8.8 mm inner opening increase mean turn length and copper volume. The wire envelopes themselves had feasible nominal-fit points.

A5g changes one geometric quantity. I keep the 8.8 mm inner transverse opening and solve the inner axial opening required to restore A5e's 118.6 mm mean turn length for each frozen wire-width candidate. I do not change current, MMF, copper cross-section, insulation screen, stator core, cage, pitch or radial layer count.

## Result

Fifty-four of 81 candidates pass every declared band. The frozen selection rule chooses 2.31 x 1.5936227286879734 mm bare rectangular copper, with a maximum Grade 2 insulation envelope of 2.48 x 1.7636227286879733 mm.

The selected point is:

- inner axial opening: 36.39101817049621 mm;
- inner transverse opening: 8.8 mm;
- outer axial span: 50.5 mm;
- outer transverse span: 22.908981829503787 mm;
- coil radial height: 7.4399999999999995 mm per alternating layer;
- inter-layer clearance: 0.6850000000000005 mm;
- upper-layer to back-yoke clearance: 0.6850000000000005 mm;
- same-cell tooth axial clearance: 6.870509085248106 mm per side;
- neighbouring-core axial clearance: 8.724999999999994 mm;
- same-layer axial clearance: 40.099999999999994 mm;
- gross insulated slot fill: 25.74707500895467%;
- mean turn length: 118.6 mm;
- copper volume: 4,933.759999999999 mm3 per cell;
- copper-volume relative error: -2.220446049250313e-16.

All thirteen A5g bands pass. I promote this nominal path only to detailed BRep winding CAD. The 4-turn A5e CAD remains the controlled build until that downstream gate passes.

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

For four nested in-plane turns with gross insulated conductor thickness `T`, their mean centreline length is `2 * (inner_axial + 8.8 + 8*T)`. I therefore solve `inner_axial = 59.3 - 8.8 - 8*T` for every candidate.

## Selection rule

Among candidates passing every hard band, I select in this order:

1. minimum total gross insulated conductor-envelope area per coil side;
2. maximum smaller radial clearance between alternating coil layers and between the upper layer and back yoke;
3. maximum minimum axial separation to the same-cell and neighbouring core;
4. smaller nominal bare width.

## Hard bands

| Band | Criterion | Selected result |
|---|---:|---|
| Turns | exactly 12 | PASS |
| Excitation | exactly 1,520 A-turn RMS | PASS |
| Copper current density | <= 40 A/mm2 | PASS, 36.53846153846154 A/mm2 |
| Bare cross-section identity | <= 1e-12 relative error from 41.6 mm2 | PASS |
| Detailed copper volume | <= 0.5% relative error from 4,933.76 mm3 | PASS |
| Mean turn length | <= 0.5% relative error from 118.6 mm | PASS |
| Gross insulated slot fill | <= 60% | PASS |
| Coil to Fluxrelay | >= 0.5 mm | PASS |
| Same-cell core axial separation | >= 0 mm | PASS |
| Neighbouring-core axial separation | >= 0 mm | PASS |
| Inter-layer radial clearance | >= 0 mm | PASS |
| Upper coil to back yoke | >= 0 mm | PASS |
| Same-layer axial clearance | >= 0 mm | PASS |

## Evidence boundary

A5g remains an analytical winding-envelope screen. It does not prove supplier availability, winding manufacture, bend strain, insulation life, lead routing, bridge packaging, hot resistance, switching loss, cooling or vibration survival.
