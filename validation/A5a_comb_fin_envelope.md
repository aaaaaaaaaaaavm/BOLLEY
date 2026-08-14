# A5a — low-profile comb-fin envelope screen

**What I knew at declaration:** NOT RUN  
**Evidence class:** analytical MODEL OUTPUT from ASSUMPTION inputs checked against EXTERNAL
GUIDANCE  
**Purpose:** I wanted to determine whether the A3a opposed-flux idea can become four mechanically accessible
side channels without sacrificing the normal CubeSat contact rails.

## Geometry I tested

Each of the four broad spacecraft faces receives one narrow longitudinal aluminium root strip.
Three covered, segmented steel fins project from each strip. A stationary slotted stator surrounds
the two sides of every fin; the spacecraft slides axially through those slots. The four corner
rails remain continuous, aluminium and mechanically separate from the electromagnetic features.

Splitting one 15 mm fin into three 5 mm fins preserves the two-sided developed air-gap area while
keeping the protrusion low. This is called the **Bolley comb-fin** in this run.

## External guidance I used

The screening values come from Cal Poly's CubeSat Design Specification Rev. 14.1, not from a
selected launch provider:

- components on the applicable side faces: no more than 6.5 mm beyond the rail plane;
- rail width to first protrusion: at least 8.5 mm on each face;
- at least 75% rail contact; and
- dispenser-contacting aluminium surfaces: hard anodized.

Source: <https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS%2BREV14_1%2B2022-02-09.pdf>.

Rev. 14.1 explicitly says launch-provider requirements supersede the CDS. A pass here is therefore
only permission to approach a dispenser provider and run nonlinear analysis.

## Assumptions I fixed

- Four face-centred force channels at the conservative A2 force-line radius of 45.75 mm.
- Three fins per face, 5.0 mm active height, 0.50 mm radial tip cover.
- 0.50 mm segmented steel core, 0.25 mm aluminium cover on each active side.
- 0.50 mm mechanical clearance on each side of the covered fin.
- 2.0 mm stationary pole-web width; three slots and four webs occupy 14.0 mm.
- 336 mm active length, 48 mm pitch and 50% axial tooth duty.
- 50 g shared root/capture/fastener allowance in addition to calculated steel and cover mass.
- Qualification total force remains the frozen A1 value. No benefit is taken from the lower
  moving mass.
- A face-centred four-channel allocation minimizes the maximum positive channel force at every
  point in the frozen +/-20 mm transverse CG grid.

Dimensions are frozen in `cad/comb_fin_parameters.json` and the drawing
`cad/a5a_comb_fin_cross_section.svg`.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A5a-1 | Total fin protrusion from the rail plane is <=6.5 mm. | Reject or shorten the fin; recompute force area. |
| A5a-2 | Distance from either rail edge to the comb root is >=8.5 mm. | Move/narrow the comb or reject this interface. |
| A5a-3 | Assumed corner-rail contact remains >=75%, with no fin crossing a rail. | Reject the layout. |
| A5a-4 | The 14 mm stationary comb footprint fits between both 8.5 mm rail keep-outs. | Reject three-fin stator access. |
| A5a-5 | Fin/root projected width consumes <=25% of the usable side-face width. | Reject or accept a separately approved panel-area penalty. |
| A5a-6 | Calculated moving interface increment is <=0.25 kg preferred and <=0.40 kg absolute. | Above preferred: reserve; above absolute: reject. |
| A5a-7 | A positive four-channel allocation exists across every frozen CG grid point. | Reject face-centred force lines. |
| A5a-8 | Peak channel force is <=255 N. | Increase channel rating or reduce CG envelope. |
| A5a-9 | Developed required air-gap shear is <=26 kPa. | Add active area or reject. |
| A5a-10 | Nominal clearance on both fin sides is >=0.50 mm. | Increase the slot or reject the tolerance stack. |

## What I explicitly did not claim

- CDS guidance does not prove compatibility with an existing dispenser.
- The calculation does not prove fin strength, root fastener strength, vibration life or debris
  containment.
- It does not predict flux, force ripple, normal-force cancellation, coil space or stator thermal
  behavior.
- Solar-cell layout and harness routing remain spacecraft-specific even if the projected-width
  screen passes.

## Output I required

I required the result to include every derived cross-section dimension, component mass, usable-face
fraction, all 441 force-allocation points, centroid closure error, peak channel load, shear and
individual band results. The generated summary must distinguish CDS guidance from provider
acceptance.

