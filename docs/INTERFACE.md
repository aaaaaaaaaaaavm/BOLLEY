# Cooperative payload interface

This is a parameter contract for first-order work, not a released drawing.

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

> The 0.50 mm magnetic-equivalent thickness is only an area-times-density placeholder from A1.
> It does not prove a closed return-flux path or a manufacturable rail. A3a explicitly screens
> moving corner return iron, an opposed through-flux fin and an aluminium induction lane before
> any topology is promoted to nonlinear analysis.

The 15 mm magnetic lane is not a claim that a conventional 8.5 mm contact rail can simply be
replaced with steel. It may occupy protected structure immediately behind the two faces meeting
at a corner. The external contact geometry remains aluminium and must pass the selected
provider's fit-check fixture.

## Material stack

The leading candidate is a segmented low-coercivity electrical-steel or soft-magnetic-composite
insert captured mechanically inside an aluminium rail extrusion or machined rail. Adhesive alone
is not accepted as ascent retention.

The material selection must close four questions together:

- saturation and air-gap shear;
- eddy-current and hysteresis loss at the commutation frequency;
- remanence near the spacecraft ADCS;
- galvanic, thermal-cycle and vibration compatibility with aluminium.

## Spacecraft obligations

The cooperative payload supplies:

- four qualified hybrid rails;
- measured mass and centre of gravity;
- declared magnetic-sensitive equipment locations;
- structural evidence for rail insert retention;
- acceptance of the Bolley-specific dispenser interface.

It supplies no electrical connection or deployment command.
