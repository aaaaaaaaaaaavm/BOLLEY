# My assumption and constraint ledger

I use this ledger to separate a physical requirement from an inherited architecture choice. The
machine-readable source is
[`analysis/assumption_ledger.json`](../analysis/assumption_ledger.json).

Changing an entry here does not change the controlled BOLLEY baseline. A constraint can move only
through an ADR in BOLLEY or a gated branch in VOLLEY-lab. Physics, launch safety, evidence
provenance and provider-controlled requirements do not become optional because a branch is called
Unbound.

## Controlled assumptions

| ID | Source | Controlled assumption | Cost or consequence I can already state | Route if I attack it |
|---|---|---|---|---|
| A-001 | BOL-R-001 | 3U, 4 kg reference, 6 kg qualification | Fixes interface, panel, pressure-area and CG geometry. I have no isolated mass cost for the class choice. | VLAB-B001 |
| A-002 | BOL-R-002/004 | 11.8 m/s inside 0.90 m and no more than 8 g | Sets force and stroke. The separate installed cost of the three numbers is not yet attributed. | VLAB-B001, burn-and-drop |
| A-003 | BOL-R-005 | Tip-off no more than 2 deg/s per axis | Drives CG knowledge, four-channel allocation, end-effect control and 6-DOF work. | Active interface, vector release |
| A-004 | BOL-R-006 | 0.25 kg preferred and 0.40 kg absolute interface increment | The selected 0.37136 kg interface misses the preference by 0.12136 kg. | Fluxframe, VLAB-B001 |
| A-005 | BOL-R-007 | Spacecraft deployment hardware remains passive | Keeps active field generation, sensing and stored energy on the launcher; P41 questions that cost. | VLAB-B002 |
| A-006 | BOL-R-008 | Hard-anodized aluminium contact and preliminary provider rail geometry | Adds magnetic gap and constrains side-panel/stator access. | VLAB-B001, Fluxsleeve |
| A-007 | BOL-R-009/010 | 900 J gross shot cap and 15 kW preferred peak power | A7c leaves 6.588 J of model energy margin. | Fluxpiston, mechanical-energy controls |
| A-008 | BOL-R-011 | No launcher propulsion member requires capture after release | Pushes the special moving interface onto the spacecraft. | Fluxsleeve, short trim shuttle |
| A-009 | BOL-R-012 | Independent fail-safe retention gate | Adds a mechanism and ascent load path that remain unsized. | Provider-specific retention study |
| A-010 | BOL-R-013 | Exit-velocity dispersion no more than 0.10 m/s at 3 sigma | Requires repeatability, sensing, calibration and precision authority. | Bulk-plus-trim, reachable-domain study |
| A-011 | BOL-R-014 | Unpowered interface field no more than 50 microtesla above ambient outside the static payload envelope | Restricts material state and discourages spacecraft permanent magnets. | VLAB-B002, shunted-magnet branch |
| A-012 | BOL-R-015 | Four face channels provide independent force allocation | Multiplies actuation, calibration and fault cases in exchange for force-centroid authority. | VLAB-X001, vector release |
| A-013 | BOL-R-016 | Every externally retained part remains attached | Forces containment and load paths into every cooperative interface. | Safety constraint; no deletion route |
| A-014 | Architecture convention | Release is mainly axial and one payload leaves at a time | Leaves vector authority and paired recoil cancellation unexplored. | Vector and opposed-release branches |
| A-015 | A11 | Nitrogen is the current Fluxpiston screening fluid | Sets storage, leakage, thermal state and plume composition for A11 only. | Distributed Fluxpiston, host-fluid branch |

## The five attacks

For every architecture rule I ask the same five questions.

| Attack | Meaning here |
|---|---|
| Delete | Remove the rule and price every new burden it creates. |
| Move | Put the function on the spacecraft, launcher, stage or removable carrier instead. |
| Invert | Reverse who controls or supplies the function. |
| Merge | Make the same hardware close another real requirement and name the part it deletes. |
| Scale | Change size, count, stroke, pressure area, channel count or duty and re-run the full boundary. |

The JSON ledger records a concrete version of all five attacks for every row above. These are search
directions. None is a design result.

## What this immediately changes

The next controlled work is electrical closure. P38, P40, P11 and P39 sit on the same dependency
chain: sectional switching changes energy and current; real hot resistance can consume the 6.588 J
margin; the source and switches add mass and thermal load; that package decides whether the
selected electromagnetic architecture remains worth carrying.

The first Unbound work attacks A-005 and A-007. A-005 asks whether the passive-only spacecraft
interface is still a useful restriction once deployment hardware can keep an orbital function.
A-007 asks whether the pulse should exist at all. Those questions become lab branches before they
can alter BOLLEY.
