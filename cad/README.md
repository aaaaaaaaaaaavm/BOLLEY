# Bolley CAD

My current completed CAD evidence is **Gen2 Fluxbridge**, which I selected in A3g and passed through
the A5d nominal-fit gate. I retain Gen1 because its failed winding package is evidence, not clutter.
My current analytical baseline is Gen2.7 Fluxrelay after passing A6h and A7c; I have not yet
converted it into controlled Gen3 CAD.

![Gen2 retained assembly](renders/gen2/01_gen2_hero.png)

## Start here

| Need | File |
|---|---|
| Controlled Gen2 dimensions | [`gen2_parameters.json`](gen2_parameters.json) |
| Native construction source | [`build_gen2.py`](build_gen2.py) |
| STEP masters | [`Bolley_Gen2_STEP.zip`](exports/gen2/Bolley_Gen2_STEP.zip) |
| STL previews | [`Bolley_Gen2_STL.zip`](exports/gen2/Bolley_Gen2_STL.zip) |
| Per-part hashes, solids, volumes and bounds | [`BUILD_GEN2.json`](BUILD_GEN2.json) |
| Archive member verification | [`exports/gen2/PACKAGE.json`](exports/gen2/PACKAGE.json) |
| Controlled dimension sheet | [`GEN2_DIMENSIONS.md`](GEN2_DIMENSIONS.md) |
| Analytical BOM | [`GEN2_BOM.md`](GEN2_BOM.md) |
| Details still needing a modeller/manufacturer | [`GEN2_MANUAL_DETAILS.md`](GEN2_MANUAL_DETAILS.md) |
| A5d result and exact intersections | [`../docs/GEN2_CAD_FIT.md`](../docs/GEN2_CAD_FIT.md) |

## What I actually modelled

- A 340.5 × 100 × 100 mm 3U envelope proxy with 8.5 mm corner rails.
- Four passive Fluxbridge blades on each of four faces.
- A homogenized full-length blade and a separate 60 mm bar-resolved coupon.
- Four 30-cell primary cassettes at 30 mm pitch.
- Alternating lower/upper winding-pack layers around adjacent teeth.
- A 160 mm track frame, guide bars and an independent retained-state gate envelope.
- Retained and positive-$x$ departure arrangements.

I use the full-length Fluxbridge split layers to represent my homogenized A3g model. I do not claim
that copper and amorphous ribbon can occupy the same material volume. My coupon is the only CAD
object that resolves discrete rungs and ligaments.

## Regenerate

```bash
python -m pip install -r requirements-cad.txt
python cad/build_gen2.py --write
python cad/render_gen2.py --write
python tools/package_gen2_cad.py --write
python tools/check_repo.py
```

I use STEP as the master exchange geometry and STL as a derived preview mesh. I fix the download
ZIP timestamps, sort member order, and verify every unpacked member against the package manifest.

## Coordinate frame

I define $+x$ from the retained payload toward the muzzle, $y$ as lateral, and $z$ as vertical. I
place the origin on the aft payload face at the retained position. I reject any arrangement that
ejects in $-x$.

## Evidence boundary

I treat this as parametric model geometry, not a drawing release. I use it to establish nominal
arrangement, cross-sectional winding space, exact solid non-interference and traceable exports. I
do not use it to establish tolerances, structural margins, fatigue, thermal distortion, vacuum
materials, debris containment, electrical insulation, cooling, gate actuation or launch-provider
acceptance.
