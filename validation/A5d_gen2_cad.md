# A5d — Gen2 Fluxbridge manufacturing-intent CAD gate

**State at declaration:** NOT RUN  
**Evidence class:** parametric CAD, exact nominal solid intersection and analytical volume checks  
**Purpose:** prove that A3g's selected stator can be represented with a real alternating-layer
winding, a discrete passive cage coupon and an unobstructed positive-x departure.

## Frozen coordinate frame and source

- $+x$: firing direction toward the 1000 mm muzzle station.
- $y$: lateral.
- $z$: vertical.
- Origin: aft payload face at the retained/breech position.
- Controlled dimensions: `cad/gen2_parameters.json`.
- Performance source: selected A3g candidate `p30_B0.56`.

## Required CAD objects

1. Homogenized full-length Fluxbridge interface kit on a 3U payload proxy.
2. Discrete 60 mm Fluxbridge coupon with 0.75 mm copper rungs at 2 mm pitch and continuous buses.
3. One complete 30-cell, three-phase stator cassette.
4. One two-cell winding/core/cage coupon resolving both alternating coil layers.
5. Track and 160 mm open frame.
6. Independent retained-state gate.
7. Full four-face retained assembly and positive-x departure arrangement.

The full-length blade may use split-thickness magnetic/copper envelopes because A3g itself is
homogenized. The coupon must resolve every copper rung and magnetic ligament. Both representations
must be labelled; neither may masquerade as the other.

## Bands declared before generation

| ID | Band | Failure action |
|---|---|---|
| A5d-1 | Payload body is 340.5 × 100 × 100 mm with 8.5 mm corner rails. | Reject payload proxy. |
| A5d-2 | Fluxbridge projection <=6.5 mm. | Reject interface. |
| A5d-3 | Four 1.0 mm blades are centred in four 1.4 mm slots with >=0.20 mm nominal side clearance. | Reject interface/stator fit. |
| A5d-4 | Core face footprint <=21 mm; active length 900 mm; 30 cells at 30 mm pitch. | Reject Gen2 cassette. |
| A5d-5 | Each two-sided winding slot contains two 9 × 9 mm coil packs inside 15 × 18 mm: <=60% gross copper fill. | Reject the winding package. |
| A5d-6 | Alternating coil layers have >=0.50 mm radial clearance to the Fluxbridge tip and do not overlap adjacent coils. | Reject winding route. |
| A5d-7 | Payload/interface has <=1e-6 mm³ nominal intersection with all four cores and coils. | Reject nominal fit. |
| A5d-8 | Muzzle opening >=130 × 130 mm; frame and all retained hardware <=160 × 160 mm. | Reject launcher envelope. |
| A5d-9 | The assembly contains four stator faces and departure is +x. | Reject arrangement. |
| A5d-10 | The discrete coupon contains 30 copper rung periods over 60 mm, root/tip buses and both coil layers. | Reject detail evidence. |
| A5d-11 | At least six STEP masters, six derived STLs and seven indexed renders are generated. | Reject incomplete package. |
| A5d-12 | Every export records size, SHA-256, solid count, volume and bounding box in a build manifest. | Reject untraceable exports. |
| A5d-13 | CAD coil-envelope volume agrees with A3g analytical copper volume within 0.5%. | Reject mass/geometry inconsistency. |

## Explicit non-bands

- A 0.20 mm nominal gap is not a tolerance stack.
- Coil packs do not resolve four turns, insulation, impregnation, leads or terminals.
- Full-length split layers are a homogenized model representation; only the coupon resolves bars.
- Fasteners, laminated sheet detail, cooling, sensors, harnesses and gate actuation are absent.
- CAD volume does not establish material allowables, vacuum compatibility, structural life or
  launch-provider acceptance.
- No generated export is a manufacturing release.

## Required output

Commit reproducible source, manifest, STEP/STL exports or an explicit regeneration policy, at
least seven inspected renders, a dimensions sheet, BOM, exact intersection volumes, all band
outcomes, a figure index and a manual-detail ledger. A5d passing promotes Gen2 geometry to field,
structure and tolerance analysis only.
