# Low-profile comb-fin interface

In A3a I found that one large corner return was the wrong place to spend moving mass. With the
comb-fin I kept the flux return on the launcher and changed the CubeSat only where I thought the
interface could afford it: a thin, passive, covered structure on each broad face.

## The geometric move

I divided one 15 mm through-flux face into three 5 mm fins. Each fin is only 1.0 mm thick after
its two aluminium covers, and projects 5.5 mm from the rail plane including its radial cap. A
launcher-owned slotted stator places a pole on both sides of each fin. Because the CubeSat moves
parallel to the slots, nothing opens, closes, returns or chases it.

Across one channel:

`2 sides × 3 fins × 5 mm × 336 mm = 100.8 cm²`

That let me preserve the A3a developed area exactly while replacing a bulky corner yoke with three
shallow teeth. I used four copies, one centred on each broad face, to retain independently
commanded force lines around the payload.

![A5a comb-fin cross-section and longitudinal tooth pattern](../cad/a5a_comb_fin_cross_section.svg)

## What I kept standard-like

- The four corner rails remain continuous hard-anodized aluminium contact surfaces.
- The comb is centred far from the 8.5 mm rail keep-outs.
- The protrusion target remains inside the 6.5 mm CDS preliminary-design guidance.
- The spacecraft carries no winding, power switch, permanent magnet, pressure vessel or release
  command.

## What I made deliberately custom

I place four slotted stators in the dispenser wall, so I am designing a Bolley dispenser rather
than an off-the-shelf spring box. I do not treat passing CDS guidance as provider acceptance. I
still need to design coil room, back-iron, slot tolerances, fault capture and a qualification
fixture.
