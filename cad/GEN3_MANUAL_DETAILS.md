# Gen3 details I still need to model

I use this as my Gen3 CAD handoff ledger. I do not let a clean render imply that I have solved a
detail that is absent from the source.

| ID | Missing detail | Input I need | Artifact that closes it |
|---|---|---|---|
| C1 | Individual four-turn conductor path | Conductor profile, bend radius, insulation build and transposition rule | Routed coil part + winding drawing |
| C2 | Inter-layer and turn insulation | Insulation class, creepage/clearance and hipot target | Insulator parts + stack drawing |
| C3 | Sectional phase leads and terminals | Cell grouping, switch partition, cable size, strain relief and service access | Harness/terminal assembly |
| C4 | Laminated primary stack | Selected steel, sheet thickness, stacking factor and clamp method | Lamination drawing + stack BOM |
| C5 | Fluxrelay ribbon lay-up | Ribbon grade, anneal/orientation, cutting method and adhesive | Ply book + process specification |
| C6 | Copper rung/backstrap/bus joint | Foil stock, joining process and resistance target | Detail drawing + joint coupon |
| C7 | Lane root capture | Spacecraft panel load path, fasteners, adhesive and fail-safe retention | Interface assembly + stress report |
| C8 | Lane encapsulation and edge radius | Vacuum dielectric, process, thickness capability and debris controls | Encapsulation drawing + material declaration |
| C9 | Four-face cassette adjustment | Runout metrology, shimming range and datum transfer | Adjustment mechanism + alignment procedure |
| C10 | Stator housing and fragment containment | Magnetic loads, launch loads and accepted safety factors | Structural assembly + FEA |
| C11 | Cooling and shot cadence | Winding loss history, allowable temperature and host heat sink | Thermal network + cooling parts |
| C12 | Position/current sensing | Accuracy, latency, redundancy and EMC constraints | Sensor mounts + harness |
| C13 | Gate actuator and latch | Ascent loads, inhibits, release time and no-fire policy | Released/retained mechanism assembly |
| C14 | Fasteners and locking | Materials, preload, locking and galvanic isolation | Fastener schedule |
| C15 | Tolerance and datum scheme | Manufacturing capability and worst-case 0.20 mm gap budget | GD&T drawing set + stack calculation |
| C16 | Cell service and assembly sequence | Tool access, replaceable cassettes and inspection points | Exploded assembly + work instruction |
| C17 | Packaged mass allocation | Structural, cooling, wiring, sensor and inverter mass estimates | Installed-system mass ledger |

I can model these parts when I have their real inputs. I will not add ornamental bolts, arbitrary
cooling passages or imaginary connector bodies to make Gen3 look more finished than it is.
