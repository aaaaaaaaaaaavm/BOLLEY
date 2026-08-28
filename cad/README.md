# Bolley CAD

My current controlled geometry is **Gen3 Fluxrelay**, built directly from the exact A8b point that
passed A6h and A7c. A5e passes all 17 frozen nominal-fit bands. I retain Gen1 and Gen2 because their
failed and superseded packages explain why I changed the machine.

![My Gen3 retained assembly](renders/gen3/01_gen3_hero.png)

## Start here

| Need | My file |
|---|---|
| Controlled Gen3 dimensions | [`gen3_parameters.json`](gen3_parameters.json) |
| Native construction source | [`build_gen3.py`](build_gen3.py) |
| STEP masters | [`Bolley_Gen3_STEP.zip`](exports/gen3/Bolley_Gen3_STEP.zip) |
| STL previews | [`Bolley_Gen3_STL.zip`](exports/gen3/Bolley_Gen3_STL.zip) |
| Per-part hashes, solids, volumes and bounds | [`BUILD_GEN3.json`](BUILD_GEN3.json) |
| Archive member verification | [`exports/gen3/PACKAGE.json`](exports/gen3/PACKAGE.json) |
| Controlled dimension sheet | [`GEN3_DIMENSIONS.md`](GEN3_DIMENSIONS.md) |
| Analytical BOM | [`GEN3_BOM.md`](GEN3_BOM.md) |
| Details I still need to design | [`GEN3_MANUAL_DETAILS.md`](GEN3_MANUAL_DETAILS.md) |
| A5e result and exact intersections | [`../docs/GEN3_CAD_FIT.md`](../docs/GEN3_CAD_FIT.md) |

## What I actually modelled

- My 340.5 × 100 × 100 mm 3U envelope proxy and its 8.5 mm corner rails.
- Five passive Fluxrelay lanes on each of four faces, from x=2.25 mm over 318.6 mm.
- One bar-resolved 100 mm lane coupon with fifty copper-rung/magnetic-web periods.
- Four complete 27-cell primary cassettes at 45.3 mm pitch over 1,223.1 mm.
- One separate nine-cell active-window cassette with three cells per phase.
- Alternating lower/upper winding-pack layers around adjacent teeth.
- A two-cell core/winding/cage coupon, track, 160 mm open frame and independent gate envelope.
- Retained, positive-$x$ departure and 900 mm endpoint-engagement arrangements.

I use homogenized full-length Fluxrelay lanes because that is the A6h/A7c model representation. My
coupon alone resolves discrete copper rungs, magnetic webs and side skins. I keep those two evidence
classes visibly separate.

## What exact geometry closed

My nominal payload/stator, coil/core and adjacent-coil intersection volumes are all zero. I retain
0.20 mm clearance on each side of a finished lane, 0.75 mm from the nearest coil pack to a lane tip,
a 150 mm open muzzle and a 2.25 mm engagement guard after the full powered travel. The complete CAD
winding volume matches A8b's installed copper volume to numerical round-off.

## Regenerate

```bash
python -m pip install -r requirements-cad.txt
python cad/build_gen3.py --write
python cad/render_gen3.py --write
python tools/package_gen3_cad.py --write
python analysis/gen3_cad_fit.py --write
python tools/make_gen3_cad_fit.py --write
python tools/check_repo.py
```

I use STEP as my master exchange geometry and STL as a derived preview mesh. I fix the download ZIP
timestamps, sort member order, and verify every unpacked member against my package manifest.

## Coordinate frame

I define $+x$ from the retained payload toward the muzzle, $y$ as lateral and $z$ as vertical. I
place the origin on the aft payload face at the retained position. I reject any arrangement that
ejects in $-x$.

## Evidence boundary

I treat A5e as parametric nominal geometry, not a drawing release. I use it to establish arrangement,
winding space, axial engagement, exact solid non-interference and traceable exports. I do not use it
to establish tolerances, structural margins, fatigue, thermal distortion, vacuum materials, debris
containment, electrical insulation, cooling, gate actuation, packaged-system mass or provider
acceptance.
