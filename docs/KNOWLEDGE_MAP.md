# My four-quadrant knowledge map

I use this file to decide what kind of work a question deserves before I spend time on it. A
quantity can sit in Quadrant I only inside its stated evidence boundary. A model result remains a
model result.

The machine-readable copy is [`analysis/knowledge_map.json`](../analysis/knowledge_map.json).

## I. What I know I know

These are retained facts from executed work.

| ID | What I know | Boundary |
|---|---|---|
| K1 | The selected Gen2.7 Fluxrelay point passed all 13 A6h nonlinear-field bands at 380 A. | Three-mesh 2D nonlinear magnetostatic model. No transient 3D or hardware evidence. |
| K2 | The selected cage/circuit point passed all 29 A7c bands in all four declared corners. | Homogenized cage plus sectional circuit and CG model. |
| K3 | The controlling A7c hot reference shot is 893.412 J, 6.588 J below the 900 J requirement. | Supplier-backed hot resistance and switching loss are still absent. |
| K4 | A5e passed all 17 nominal CAD-fit bands for the exact selected Gen3 point. | Nominal solid geometry only. Tolerance, thermal growth, vibration and runout stay open. |
| K5 | A10 exposed the 12.0 m/s, 0.90 m and 8 g inconsistency; ADR-040 changed BOL-R-002 to 11.8 m/s. | Requirement correction. |
| K6 | A11 passed its eight executable ideal-gas and continuum-leakage bands. | Seal contact, friction, rarefaction, contamination, plume and valve transients stay open. |
| K7 | A12 showed the 121.36 g Fluxframe credit is material against the sourced 3U chassis envelope. | No bus-specific displaced-mass credit has been awarded. |

A failure belongs here too once I know what failed and under what boundary. I do not reserve
Quadrant I for favourable results.

## II. What I do not know I know

This is work already latent in the repositories.

I mine it before opening a new model:

- assumptions reused by several analyses but justified only once;
- sensitivity and candidate archives whose information never reached a decision;
- rejected architectures that were strong on a metric that now controls a different subsystem;
- launcher parts that exist only because another launcher part exists;
- BOLLEY rules inherited from VOLLEY rather than from physics, safety or a provider;
- sibling-repository results that answer the same physical question on a different boundary.

The first product of this mining pass is
[`ASSUMPTION_LEDGER.md`](ASSUMPTION_LEDGER.md). I will add a parameter/result dependency graph after
I can derive it from controlled inputs rather than from prose.

## III. What I know I do not know

[`OPEN_PROBLEMS.md`](../OPEN_PROBLEMS.md) remains the authoritative defect register. I classify its
next action separately so a provider decision does not compete with a computation for engineering
time.

| Next action | Current IDs |
|---|---|
| Compute now | P2, P3, P4, P5, P8, P10, P14, P21, P25, P29, P30, P38, P39, P40, P41, P45, P46, P47, P48 |
| Compute, then require hardware | P1, P6, P7, P9, P27, P44 |
| Supplier or customer evidence | P11, P13, P16, P43 |
| Provider or other external decision | P12, P15, P19, P20 |
| Deferred or historical branch | P17, P18, P22, P23, P24, P26, P32, P33, P34, P35 |

This table does not change a problem state. It says what kind of evidence can move it.

The controlled Fluxrelay queue starts with P38, P40, P11 and P39. The selected point has 6.588 J
of model margin. I need to know whether switching, real hot resistance and packaged electrical
hardware consume that margin before I spend the same effort polishing secondary parts of the
machine.

## IV. What I do not know I do not know

I cannot list this quadrant completely. I can control how I search it.

Current searches belong in the shared lab until they earn a target-specific gate:

- `VLAB-B001`: bus, deployment interface and spent stage co-designed as one temporary machine;
- `VLAB-X001`: use metered leakage as a restoring gas bearing instead of treating all leakage as
  waste;
- proposed `VLAB-B002`: allow a powered cooperative spacecraft interface and require the added
  hardware to retain an orbital job after release;
- proposed `VLAB-B003`: replace one lumped Fluxpiston feed with distributed or staged injection;
- vector release, opposed release, Fluxsleeve, shunted magnets, selected springs, carousel and
  burn-and-drop remain branch-register work until each has its own gate.

I search by physical subproblem outside deployer literature: gas bearings, turbomachinery seals,
machine-tool guidance, magnetic bearings, linear motors, launch locks, pneumatic machinery,
multifunctional structures, pressure balancing, vibration control and separation mechanisms. An
outside example can change the question. It does not provide BOLLEY performance evidence.

## Movement between quadrants

An Unbound idea enters Quadrant III only after I give it a source boundary, a stop condition and
acceptance bands. A run, measurement, supplier document or external decision can move that question
into Quadrant I. Repository mining in Quadrant II can expose a new Quadrant III question without
changing the controlled baseline.

That movement is the work. The quadrant label itself is bookkeeping.
