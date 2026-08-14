# A3a — moving-interface flux-path screen

**What I knew at declaration:** NOT RUN  
**Evidence class:** analytical MODEL OUTPUT from ASSUMPTION inputs  
**Purpose:** I wanted to reject physically incomplete translator cross-sections before nonlinear FEA.

## The question I asked

Does any passive moving interface preserve the A2 force area while remaining inside the
spacecraft-side mass gates and providing a physically explicit magnetic or conductive path?

This run does **not** predict motor force. It screens three unit cells:

1. the original two-face corner rail with an L-shaped moving flux return;
2. an opposed-stator, through-flux steel fin/tab with no moving back iron;
3. a single-sided aluminium induction lane with all magnetic return iron fixed to the launcher.

The dimensioned screening geometry is frozen in `cad/topology_candidates.json` and
`cad/a3a_unit_cells.svg`.

## Inputs I fixed

- Worst commanded channel force: read from committed A2 output.
- Active length: 336 mm.
- Reluctance face width: 15 mm; two active faces per channel.
- Induction-lane width: 30 mm; one active face per channel.
- Four channels.
- Steel density: 7,650 kg/m³; aluminium density: 2,700 kg/m³.
- Moving non-active allowance: 75 g for capture, covers and local reinforcement.
- Steel working-flux screen: 1.60 T. This is an assumption, not a selected grade's B-H curve.
- Preferred interface increment: 0.25 kg; absolute kill: 0.40 kg.
- Required stress-area band: 26 kPa.

For the corner return, normal gap flux `Bn` is swept rather than guessed. The minimum
equal-component field associated with the required shear is reported from the optimistic
Maxwell-stress relation

`tau = Bn * Bt / mu0`, with `Bn = Bt = sqrt(mu0 * tau)`.

I treat this as a lower-bound screen, not a reluctance-machine solution. Leakage, fringing, saturation,
cover loss and commutation can only make the real design harder.

## Bands I declared before execution

| ID | Band | Failure action |
|---|---|---|
| A3a-1 | Each promoted unit cell provides at least `Fchannel / 26 kPa` active area. | Reject or widen that interface. |
| A3a-2 | Moving interface increment is at most 0.25 kg preferred and never above 0.40 kg. | Reserve a hard-limit candidate; reject above 0.40 kg. |
| A3a-3 | A corner L-return inside the 0.25 kg mass gate can carry at least the optimistic equal-component normal field. | Do not promote the original corner return to FEA if it fails. |
| A3a-4 | Opposed-fin steel remains below 0.25 kg including the 75 g allowance. | Reject opposed-fin reluctance. |
| A3a-5 | The 1 mm aluminium induction lane remains below 0.25 kg including the 75 g allowance. | Reject the induction fallback. |
| A3a-6 | At least one candidate passes area and preferred mass. | Stop A3 and revisit payload modification or Bolley-U. |

## What I explicitly did not claim

- Double-sided stator access around the fin/tab is **not proven** by this screen.
- Induction thrust, slip, secondary heating and normal force are **not calculated**.
- The corner return's actual `Bn/Bt` relationship is **not calculated**.
- A mass pass does not promote a candidate directly to hardware.

## Output I required

The committed JSON must report equations, every assumed dimension, candidate mass, active area,
required shear, the corner-return field window and a disposition. A generated Markdown summary
must name unresolved access and electromagnetic work without calling it validation.

