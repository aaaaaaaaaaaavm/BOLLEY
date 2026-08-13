# Gen2 details not yet modelled

This is the CAD handoff ledger. A blank space in the current model is not permission for a
fabricator to improvise it.

| ID | Missing detail | Required input | Close artifact |
|---|---|---|---|
| C1 | Individual four-turn conductor path | Selected conductor profile, bend radius and insulation build | Routed coil part + winding drawing |
| C2 | Inter-layer electrical separation | Insulation class, creepage/clearance and hipot target | Insulator part + stack drawing |
| C3 | End leads and terminals | Phase connection, cable size, strain relief and service access | Harness/terminal assembly |
| C4 | Laminated primary stack | Selected steel, sheet thickness, stacking factor and clamp method | Lamination drawing + stack BOM |
| C5 | Fluxbridge ribbon lay-up | Ribbon grade, anneal/orientation, cut method and adhesive | Ply book + process specification |
| C6 | Copper rung/bus joint | Foil/bar stock, joining process and resistance target | Detail drawing + joint coupon |
| C7 | Blade root capture | Spacecraft panel load path, fasteners, adhesive and fail-safe retention | Interface assembly + stress report |
| C8 | Blade encapsulation | Vacuum-compatible dielectric, thickness and edge radius | Encapsulation drawing + material declaration |
| C9 | Four-face cassette adjustment | Runout metrology and shimming range | Adjustment mechanism + alignment procedure |
| C10 | Stator housing and containment | Magnetic loads, launch loads, fragment containment | Structural assembly + FEA |
| C11 | Cooling | Shot cadence, allowable winding temperature and heat sink | Thermal network + cooling parts |
| C12 | Position/current sensing | Sensor type, accuracy, redundancy and EMC constraints | Sensor mounts + harness |
| C13 | Gate actuator and latch | Ascent loads, inhibits, release time and no-fire policy | Released/retained mechanism assembly |
| C14 | Fasteners and locking | Materials, preload, locking and galvanic isolation | Fastener schedule |
| C15 | Tolerance and datum scheme | Manufacturing capability and worst-case gap budget | GD&T drawing set + stack calculation |
| C16 | Assembly/service sequence | Tool access, replaceable cassettes and inspection points | Exploded assembly + work instruction |

The parametric source can be extended to these parts once their engineering inputs exist. Producing
ornamental fasteners or arbitrary cooling passages before those inputs would create false detail,
not readiness.
