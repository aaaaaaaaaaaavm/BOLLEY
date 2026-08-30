# A9: selected Gen3 sectional-drive transient

**What I know at declaration:** NOT RUN  
**Evidence class:** time-domain sectional circuit/force model  
**Purpose:** I want to find out whether the selected Fluxrelay point still fits its existing electrical and departure-state limits once I stop treating the active window as prebiased and quasi-steady.

> Pre-execution correction, 2026-08-31: my first controlled parameter file used 9.80665 m/s2 for
> gravity. A7c actually used 9.81 m/s2. Before `analysis/sectional_drive.py` existed, I changed only
> that inherited constant so A9 reproduces A7c's mechanical work exactly. No band, geometry,
> electrical limit or fault condition changed. ADR-047 records the correction.

## Point I freeze

I keep the exact selected A8b/A6h/A7c/A5e point:

- 27 cells per face at 45.3 mm pitch;
- 318.6 mm five-lane passive cage;
- 1.2231 m installed primary;
- four face channels;
- 380 A rated phase current;
- 10.4 mm2 per turn and four turns per cell;
- A6h fine three-cell phase-window inductance of 4.81156 uH;
- A7c active-window phase resistance before the existing 100/125% corner multiplier;
- A7c 90/100% cage-conductance and 100/125% resistance corners;
- 4 kg reference and 6 kg qualification payload cases;
- the existing 21 by 21 transverse-CG envelope.

I do not alter the 900 J reference-energy limit to make room for switching.

## What changes from A7c

A7c assumes a quasi-steady prebiased active window. A9 must make current a state variable and move the cage through the cell lattice. It must represent:

- finite current rise and decay from the solved A6h inductance and A7c resistance;
- overlap of an outgoing and incoming section during handoff;
- the first and last active-cell transitions rather than a periodic infinite machine;
- electrical source energy including copper and magnetic-energy changes;
- one declared failed-cell case in each face channel;
- channel-force redistribution using the existing A2 force-allocation boundary.

The model may use an ideal controlled voltage source for this first transient gate. P11 remains open until a supplier-backed source, switch and cable chain replaces it.

## Existing bands I inherit

I use existing requirements rather than inventing a second set of softer transient limits.

1. Maximum phase current is at most 400 A.
2. Required DC-link voltage is at most 48 V.
3. Peak DC power is at most 15 kW.
4. Reference source energy is at most 900 J.
5. Qualification source energy is at most 1,500 J.
6. Reference and qualification longitudinal acceleration do not exceed 8 g in the modeled healthy shot.
7. The healthy reference-shot exit-state error caused by switching, handoff and finite ends is no more than 0.10 m/s relative to the same A7c constant-force target. I use the full BOL-R-013 dispersion requirement as an upper bound on this model contribution; a pass consumes that whole budget and therefore does not establish hardware dispersion.
8. The healthy qualification shot reaches at least 10 m/s.
9. Opposed-field normal-force imbalance remains at most 100 N under the existing A7c 1% mismatch condition.
10. No healthy handoff or end transition creates negative commanded axial force.
11. A single failed cell may not require more than 400 A or 48 V in the remaining commanded cells and may not create reverse axial force. I report the resulting exit velocity as a degraded case rather than require the nominal velocity after a fault.

## Numerical checks

I require at least two time-step resolutions. Refinement must not change any pass/fail outcome. I report the change in exit velocity, source energy, peak current and peak voltage rather than hide it inside a generic convergence label.

I also require energy-accounting closure: source energy, copper loss, magnetic-energy change and mechanical work must close to the residual produced by the stated model. I report the residual and do not assign an acceptance percentage before I see the discretization behaviour.

## What this run cannot establish

- It does not resolve the passive cage into discrete 3D rungs and end buses. P29 remains open.
- It does not provide supplier switching loss, hot resistance, SOA or cable evidence. P11 and P40 remain open after a model pass.
- It does not close package mass, cooling, containment or EMC. P39 remains open.
- It does not close full 6-DOF separation or hardware tip-off. P5 and P10 remain open.
- It does not validate force. No hardware exists.

## Disposition rule

If an inherited electrical or departure-state band fails, I record the failure and do not widen the band. A pass may move P38 from OPEN to MODELLED only for the effects represented here. It does not close Gen4 or promote hardware readiness.
