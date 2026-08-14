# A3b0 — ideal tooth-edge force bound

**What I knew at declaration:** NOT RUN  
**Evidence class:** analytical UPPER BOUND from ASSUMPTION geometry, anchored to named EXTERNAL
MATERIAL DATA  
**Purpose:** I wanted to kill an impossible comb before nonlinear FEA, winding design or hardware work.

## The question I asked

Can the exact A5a three-fin channel reach the frozen 255 N average-force gate even in an ideal
gap-dominated reluctance model?

## Why I run precedes A3b

The A5a developed-area result divided force by both long fin faces. In a tooth-overlap switched-
reluctance machine, axial work comes from the change in overlap area at each active tooth edge.
Whole-face shear is therefore not a force proof. A geometry that fails the ideal energy-gradient
bound cannot be rescued by a more detailed solver.

## The topology and derivation I froze

- Three fins per channel and seven 48 mm teeth per fin over 336 mm.
- One increasing-overlap edge per energized tooth and fin: 21 simultaneous ideal edges.
- Active fin height $h=5.0$ mm.
- Effective gap on each side $g=0.25$ mm aluminium cover + $0.50$ mm clearance = $0.75$ mm.
- Two equal air gaps are in series; steel reluctance is set to zero.
- Every active edge is allowed to reach the same flux density at once.

For overlap area $A=h x$ and two equal gaps,

$$L = \frac{N^2\mu_0 A}{2g}, \qquad
F = \frac{1}{2}i^2\frac{dL}{dx}, \qquad
B = \frac{\mu_0Ni}{2g}.$$

Substitution gives the optimistic edge bound

$$F_{edge}=\frac{B^2gh}{\mu_0}.$$

## The material reality anchor I used

thyssenkrupp Steel lists minimum magnetic polarization of 1.70 T at 10,000 A/m for powercore A
M270-50A. A3b0 uses 1.7 T as its preferred design field and a deliberately generous 2.0 T as the
hard upper-bound ceiling. Neither number substitutes for a selected batch's B-H curve.

Source: <https://www.thyssenkrupp-steel.com/en/products/electrical-steel/electrical-steel-non-grain-oriented/powercore-a/powercore-a.html>.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A3b0-1 | Ideal force at the optimistic 2.0 T ceiling is >=255 N. | Reject the exact three-fin geometry before FEA. |
| A3b0-2 | Required ideal flux density is <=1.7 T preferred. | Mark the geometry saturation-sensitive and redesign before hardware. |
| A3b0-3 | Required ideal flux density is <=2.0 T absolute. | Reject the exact three-fin geometry. |

The hard disposition uses A3b0-1 and A3b0-3. The preferred band exposes designs that nominally
clear the mathematical force gate but leave no credible room for steel drop or leakage.

## What I explicitly did not claim

- I do not treat this as FEA and does not model finite steel permeability, saturation shape, leakage,
  fringing, end effects or tooth-to-tooth coupling.
- It applies no winding window, ampere-turn, voltage, current, inverter, thermal or normal-force
  constraint.
- It does not prove that every tooth can be energized simultaneously at maximum speed.
- Passing would only earn nonlinear 3D analysis. Failure is decisive because every omitted effect
  makes useful force lower, not higher.

## Output I required

I required the result to report the force coefficient, force-versus-field sweep, field required for 255 N,
ideal force at 2.0 T, band outcomes and the minimum integer fin count at 1.7 T and 2.0 T.
