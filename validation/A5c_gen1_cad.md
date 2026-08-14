# A5c — Gen1 parametric CAD package

**What I knew at declaration:** NOT RUN  
**Evidence class:** PARAMETRIC CAD geometry and automated manifest checks  
**Purpose:** I wanted to turn the A3e architecture into inspectable native geometry without allowing a render
to become a dimensional source.

## The coordinate frame I froze

- $+x$: firing direction toward the muzzle.
- $y$: lateral.
- $z$: vertical.
- Origin: aft payload face at the retained/breech position.

The payload leaves in $+x$. Any assembly or figure showing departure through the gate at negative
$x$ is wrong.

## Objects I required

1. Fluxfoil interface kit: four continuous fins on each of four faces.
2. 3U payload envelope proxy with 8.5 mm corner rails.
3. One complete 57-cell, three-phase serpentine stator cassette.
4. Track and open 160 mm frame envelope.
5. Independent retained-state gate geometry.
6. A 96 mm / six-cell one-face A3 coupon.
7. Full four-face assembly.

Each object must be exported as STEP master geometry and derived STL. Source is
`cad/build_gen1.py`; dimensions are frozen in `cad/gen1_parameters.json`.

## Bands I declared before generation

| ID | Band | Failure action |
|---|---|---|
| A5c-1 | Payload body envelope is exactly 340.5 × 100 × 100 mm; normal rails are 8.5 mm. | Reject the payload proxy. |
| A5c-2 | Fluxfoil projection is <=6.5 mm. | Reject the interface. |
| A5c-3 | Four 1.0 mm fins align concentrically in four 2.0 mm slots, leaving >=0.50 mm nominal clearance per side. | Reject the stator/interface fit. |
| A5c-4 | Stator face footprint is <=21 mm and active length is exactly 912 mm. | Reject the Gen1 cassette. |
| A5c-5 | The muzzle opening is >=130 × 130 mm and the full frame envelope is <=160 × 160 mm. | Reject the launcher envelope. |
| A5c-6 | No payload/interface solid intersects a stator core or coil solid at nominal position. | Reject the nominal fit. |
| A5c-7 | The assembly contains four stator faces and departure is in +x through the muzzle. | Reject arrangement. |
| A5c-8 | At least six STEP masters and six derived STLs are generated. | Reject incomplete package. |
| A5c-9 | At least five renders are generated from the model, each indexed by source and evidence class. | Reject incomplete repository presentation. |
| A5c-10 | Every committed CAD artifact has size, SHA-256, solid count, volume and bounding box in `cad/BUILD.json`. | Reject untraceable exports. |

## What I explicitly did not claim

- CAD volume does not override analytical material mass.
- Coil packs are envelopes, not individual turns, insulation, potting or terminals.
- Lamination stack, fasteners, tolerances beyond the nominal slot, cooling, harnesses, sensors and
  gate actuation are absent.
- The payload proxy is not a spacecraft design and no launch provider has accepted the fins.
- Interference at nominal dimensions is not a tolerance-stack analysis.

## Output I required

I required the result to include native and derived files, a machine-readable build manifest, dimension and
BOM documents generated from the same parameter file, render source files, individual band
outcomes and a list of every detail still needing a modeller or manufacturer.
