# A3b1 — shared-pole stator throat bound

**What I knew at declaration:** NOT RUN  
**Evidence class:** analytical FLUX-CONSERVATION UPPER BOUND from ASSUMPTION topology, anchored
to named EXTERNAL MATERIAL DATA  
**Purpose:** I wanted to decide whether the exact A5b five-web stationary sketch deserves nonlinear FEA.

## The question I asked

Can the four-fin quad-comb's 2 mm shared stationary pole webs turn the required gap flux into a
conventional radial back yoke without impossible pole field or an interface-width violation?

## The topology I froze

- Four 2.0 mm moving slots separated by five 2.0 mm stationary pole webs.
- Alternating pole polarity across the face so every fin sees transverse flux.
- Two outer webs carry one fin flux each.
- Three interior webs carry the sum of two adjacent fin fluxes each.
- Gap-face height is the A5b 6.0 mm fin height.
- Flux turns radially through each web into one back yoke.
- A5b's required ideal gap field and 255 N gate are not changed.

For uniform leakage-free flux, a pole throat obeys

$$B_{pole}\,w_{pole}=m\,B_{gap}\,h_{fin},$$

where multiplicity $m=1$ at an outer pole and $m=2$ at an interior shared pole. Axial overlap
cancels from both sides of the area balance.

## The material anchor I used

The preferred pole field is 1.7 T and the deliberately optimistic hard ceiling is 2.0 T. The
1.7 T anchor follows thyssenkrupp powercore A catalogue polarization data; neither value is a
selected B-H curve:
<https://www.thyssenkrupp-steel.com/en/products/electrical-steel/electrical-steel-non-grain-oriented/powercore-a/powercore-a.html>.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A3b1-1 | Outer throat field at the required gap field is <=1.7 T preferred and <=2.0 T hard. | Reject the drawn pole throat. |
| A3b1-2 | Interior shared-throat field is <=1.7 T preferred and <=2.0 T hard. | Reject the shared-pole topology. |
| A3b1-3 | Ideal channel force at the gap field permitted by a 2.0 T interior throat is >=255 N. | Reject before FEA. |
| A3b1-4 | A resized shared-pole array at 1.7 T occupies <=25% of usable face width. | Reject the conventional shared-yoke layout. |
| A3b1-5 | The same footprint band passes even at an optimistic 2.0 T. | Reject the conventional shared-yoke layout. |

Preferred and hard field checks are stored separately, producing seven executable bands.

## What I explicitly did not claim

- This bound assumes uniform, leakage-free flux and no local corner concentration.
- It does not cover an axially multiplexed, individually returned or superconducting stator.
- No winding window, voltage, current, thermal or structural result is present.
- Failure rejects the exact shared-pole stator, not every possible reluctance launcher and not the
  already-modelled quad-comb payload mass.

## Output I required

I required the result to report outer/interior throat fields, the throat-limited gap field and force,
required pole widths at 1.7 T and 2.0 T, resulting footprint fractions, all band outcomes and a
disposition.
