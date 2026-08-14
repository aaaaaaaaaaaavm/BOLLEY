# Cooperative payload interface

I use this as my parameter contract for first-order work, not as a released drawing.

## Initial geometry

| Parameter | Phase 0 value | Provenance |
|---|---:|---|
| Payload class | 3U | Programme decision |
| Magnetic active length | 336 mm | Seven 48 mm pitches, assumption |
| Rail-force radius from geometric centre | 45.75 mm | Geometric estimate |
| Corners | 4 | CubeSat interface |
| Active magnetic faces per corner | 2 | Architecture decision |
| Active width per face | 15 mm | Assumption to be fit-checked |
| Magnetic material equivalent thickness | 0.50 mm | Mass-screen assumption |
| Aluminium cover over magnetic circuit | 0.50 mm target | Assumption |
| Mechanical clearance per stator face | 0.75 mm target | Assumption |
| Effective nominal magnetic gap | 1.25 mm target | Derived assumption |
| Translator pole pitch | 48 mm | Commutation/packaging compromise |

> I use the 0.50 mm magnetic-equivalent thickness only as an area-times-density placeholder from
> A1. I do not treat it as proof of a closed return-flux path or manufacturable rail. In A3a I screen
> moving corner return iron, an opposed through-flux fin and an aluminium induction lane before
> any topology is promoted to nonlinear analysis.

## A3a disposition

I rejected the original L-shaped corner return as configured. Its moving return iron cannot
carry even the optimistic lower-bound field inside the declared 0.40 kg interface limit at 50%
tooth duty. The current primary candidate is a 0.50 mm through-flux steel fin/tab with 0.25 mm
cover per side and 0.50 mm target clearance per stator face. Its screened increment is 0.114 kg,
including the same 75 g non-active allowance.

I treated those dimensions as assumptions. In A5a I replaced the single 15 mm fin with three 5 mm fins per
broad face. The resulting 14 mm comb footprint projects 5.5 mm from the rail plane, retains the
corner rails and screens at 121.2 g including explicit side/tip cover and a 50 g root/capture
allowance. It passes the preliminary CDS-guidance checks, but still needs provider approval and a
real structural capture design. The 30 mm × 1.00 mm single-sided aluminium lane remains the
fallback.

I do not claim that a conventional 8.5 mm contact rail can simply be
replaced with steel. It may occupy protected structure immediately behind the two faces meeting
at a corner. The external contact geometry remains aluminium and must pass the selected
provider's fit-check fixture.

## Material stack

My leading candidate is a segmented low-coercivity electrical-steel or soft-magnetic-composite
insert captured mechanically inside an aluminium rail extrusion or machined rail. Adhesive alone
is not accepted as ascent retention.

I require the material selection to close four questions together:

- saturation and air-gap shear;
- eddy-current and hysteresis loss at the commutation frequency;
- remanence near the spacecraft ADCS;
- galvanic, thermal-cycle and vibration compatibility with aluminium.

## Spacecraft obligations

I require the cooperative payload to supply:

- four qualified passive comb-fin face interfaces and conventional corner contact rails;
- measured mass and centre of gravity;
- declared magnetic-sensitive equipment locations;
- structural evidence for rail insert retention;
- acceptance of the Bolley-specific dispenser interface.

I require no electrical connection or deployment command from it.
