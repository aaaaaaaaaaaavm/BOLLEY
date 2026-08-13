# Bolley CAD

The current controlled geometry is **Gen2 Fluxbridge**, selected by A3g and passed through the A5d
nominal-fit gate. Gen1 remains here because its failed winding package is evidence, not clutter.

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

## What is actually modelled

- A 340.5 × 100 × 100 mm 3U envelope proxy with 8.5 mm corner rails.
- Four passive Fluxbridge blades on each of four faces.
- A homogenized full-length blade and a separate 60 mm bar-resolved coupon.
- Four 30-cell primary cassettes at 30 mm pitch.
- Alternating lower/upper winding-pack layers around adjacent teeth.
- A 160 mm track frame, guide bars and an independent retained-state gate envelope.
- Retained and positive-$x$ departure arrangements.

The full-length Fluxbridge split layers represent the homogenized A3g model. They are not a claim
that copper and amorphous ribbon can occupy the same material volume. The coupon is the only CAD
object that resolves discrete rungs and ligaments.

## Regenerate

```bash
python -m pip install -r requirements-cad.txt
python cad/build_gen2.py --write
python cad/render_gen2.py --write
python tools/package_gen2_cad.py --write
python tools/check_repo.py
```

STEP is the master exchange geometry. STL is a derived preview mesh. The download ZIP timestamps
are fixed, member order is sorted, and every unpacked member is verified against the package
manifest.

## Coordinate frame

$+x$ points from the retained payload toward the muzzle. $y$ is lateral, $z$ is vertical, and the
origin lies on the aft payload face at the retained position. Any arrangement ejecting in $-x$ is
wrong.

## Evidence boundary

This is parametric model geometry, not a drawing release. It establishes nominal arrangement,
cross-sectional winding space, exact solid non-interference and traceable exports. It does not
establish tolerances, structural margins, fatigue, thermal distortion, vacuum materials, debris
containment, electrical insulation, cooling, gate actuation or launch-provider acceptance.
