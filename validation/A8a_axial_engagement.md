# A8a — Gen2.6 axial engagement and sectional-excitation audit

**State at declaration:** NOT RUN  
**Evidence class:** exact interval overlap + current-limited kinematic integration  
**Purpose:** determine whether the 900 mm stator can deliver the 900 mm powered travel claimed by
the post-field shot model when the 336 mm cage actually leaves it.

## Frozen audit

A8a does not change A6g field, A7b cage, current or energy bands. It places the CAD intervals on
one axis:

- stator active interval 0–900 mm;
- cage active interval 2.25–338.25 mm at retention;
- +900 mm commanded travel;
- 375 A rated and 400 A absolute phase-current ceiling; and
- force proportional to overlapped active area and squared current-derived field.

Three traces are required: the as-drawn point at 375 A, the as-drawn point with current raised
only as needed and clipped at 400 A, and the best axial placement over the same 900 mm stator.
Every trace uses 9,001 travel points. The best-placement search uses 673 declared starting
positions and cannot change stator or cage length.

## Bands declared before execution

1. As-drawn 375 A reference exit speed is at least 11.8 m/s.
2. As-drawn 375 A qualification exit speed is at least 10.0 m/s.
3. Best placement with current limiting still reaches at least 11.8 m/s.
4. Current never exceeds 400 A RMS.
5. End-of-travel overlap remains 100% if full nominal force is claimed.
6. The minimum three-phase-cell-quantised full-overlap primary remains <=16.0 kg.
7. The minimum 150 mm-tile-quantised full-overlap primary remains <=16.0 kg.
8. A cell-sectional window has <=82.0176% of A7b phase resistance.
9. A whole-tile-sectional window has <=82.0176% of A7b phase resistance.
10. The cell-quantised extension retains a complete three-phase cell count.

The 82.0176% resistance limit is the A7b paired-corner diagnostic committed before this gate. It
is not refit here.

## Explicit non-bands

- Overlap force scaling is geometric; no axial transient electromagnetic solve is claimed.
- Boosting current does not assume the A6g field remains within saturation bands.
- Length-scaled primary mass excludes containment, cooling, inverters and cables.
- A sectional-window pass is permission to model switches and individual cells, not validation of
  that circuit.

## Required output

Commit all 9,001 profile rows, the three traces, exact full-overlap length, cell/tile-rounded
lengths and masses, sectional resistance ratios and all ten Boolean bands. A failure rejects the
as-drawn axial package, not the five-lane transverse field result.

## Recorded result

**Run completed 2026-08-13. Result: 5/10 bands pass; reject the as-drawn axial package.**

At 375 A the full-force-equivalent work distance is 0.72975 m and exit velocity is 10.702 m/s.
Clipping an overlap-compensation command at 400 A raises that to only 10.851 m/s. The best
possible placement begins and ends at 50% overlap and reaches 11.517 m/s, still below 11.8 m/s.

Full engagement requires 1.23825 m continuously. The first complete three-phase lattice is 42
cells / 1.26 m / 22.199 kg; whole 150 mm modules require nine tiles / 1.35 m / 23.785 kg. Both
fail 16 kg. Cell and whole-tile sectional windows retain 0.50 and 0.70 times A7b phase resistance,
so both pass the predeclared 0.820176 circuit diagnostic.

The 9,001-row deterministic trace is retained at
`analysis/results/axial_engagement_points.csv.gz`, SHA-256
`c5abf2e51c0501602b2847db242ff6bb0461c80c0463e9739d89ca9be93a2f4a`.
