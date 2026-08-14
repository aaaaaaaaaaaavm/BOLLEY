# A5b — four-fin, 6 mm quad-comb screen

**What I knew at declaration:** NOT RUN  
**Evidence class:** analytical MODEL OUTPUT from ASSUMPTION geometry checked against named
EXTERNAL GUIDANCE and MATERIAL DATA  
**Purpose:** I wanted to determine whether the smallest clean redesign after A3b0 deserves nonlinear 3D
electromagnetic analysis.

## Geometry I tested

Each face channel gains one fin and 1.0 mm of active height relative to A5a:

- four axially aligned fins per channel;
- 6.0 mm active height plus a 0.25 mm radial tip cap;
- the same 0.50 mm steel, 0.25 mm side covers and 0.50 mm per-side mechanical clearance;
- four 2.0 mm slots and five 2.0 mm stationary pole webs: 18.0 mm footprint;
- seven 48 mm teeth over 336 mm; and
- the same four face-centred force lines and frozen CG grid.

The fins remain aligned. Deliberately staggering them would reduce the number on a positive
overlap slope at once. Continuous commutation is instead assigned to multiple axial stator phases
on the launcher, which A5b does not yet size.

## Why I is the minimum clean change

A3b0 found that 21 ideal active edges require 2.017 T for 255 N. Four fins create 28 edges.
Increasing active height to 6.0 mm uses most of the preliminary 6.5 mm protrusion allowance without
widening the 0.75 mm effective side gap. The spacecraft still carries only passive steel and
aluminium; windings, switches, cooling and stored energy remain on the deployer.

Dimensions are frozen in `cad/quad_comb_parameters.json`.

## External anchors I used

Envelope values use Cal Poly CubeSat Design Specification Rev. 14.1. Launch-provider requirements
supersede it:
<https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS%2BREV14_1%2B2022-02-09.pdf>.

The 1.7 T design field is anchored to thyssenkrupp powercore A catalogue polarization data, not a
selected B-H curve:
<https://www.thyssenkrupp-steel.com/en/products/electrical-steel/electrical-steel-non-grain-oriented/powercore-a/powercore-a.html>.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A5b-1 | Total projection is <=6.5 mm. | Reject or shorten the fin. |
| A5b-2 | Nominal protrusion reserve is >=0.20 mm. | Reject the untoleranced maximum-envelope design. |
| A5b-3 | Distance from either rail edge to the comb root is >=8.5 mm. | Move/narrow the comb or reject. |
| A5b-4 | Assumed corner-rail contact remains >=75%, with no fin crossing a rail. | Reject the layout. |
| A5b-5 | The 18 mm stationary footprint fits between both rail keep-outs. | Reject four-fin stator access. |
| A5b-6 | Comb footprint consumes <=25% of usable side-face width. | Reject or require a separately approved panel penalty. |
| A5b-7 | Moving interface increment is <=0.25 kg preferred and <=0.40 kg absolute. | Above preferred: reserve; above absolute: reject. |
| A5b-8 | A positive four-channel allocation exists at every frozen CG point. | Reject the face-centred force lines. |
| A5b-9 | Peak allocated channel force is <=255 N. | Increase channel rating or reduce the CG envelope. |
| A5b-10 | Nominal side clearance is >=0.50 mm. | Increase the slot or reject the tolerance stack. |
| A5b-11 | Tip cover is not thinner than the 0.25 mm side cover. | Restore cover or define a different capture system. |
| A5b-12 | Ideal edge-force bound at 1.7 T is >=255 N. | Reject before nonlinear FEA. |
| A5b-13 | Ideal force margin at 1.7 T is >=10%. | Add edge/height margin before nonlinear FEA. |
| A5b-14 | Required ideal field is <=2.0 T absolute. | Reject before nonlinear FEA. |

The preferred and absolute mass limits are recorded as separate executable bands, so the output
contains 15 Boolean bands.

## What I explicitly did not claim

- The energy-gradient result is the same optimistic gap-only upper bound used in A3b0. It is not
  nonlinear force evidence.
- No stationary return-yoke section, interior-web flux sharing, winding window or phase-coil
  arrangement is defined.
- No finite permeability, leakage, fringing, end effect, normal force, voltage, current, loss,
  heating or force-ripple result exists.
- No provider has accepted the side-face occupation, stator envelope or 0.25 mm nominal
  protrusion reserve.
- Root capture, strength, vibration, debris and wear remain open.

## Output I required

I required the result to include derived geometry, moving mass, all 441 force-allocation points, ideal
edge-force coefficient, force at 1.7 T, required ideal field, every band outcome and a disposition.
