# A11, my Fluxpiston clearance and gas-flow screen

**State: RUN. All 8 executable frozen bands pass; band 9 remains OPEN by declaration.**

A10 showed that a full 0.01 m2 pressure face moves the problem into a roughly 30–33 kPa regime. It
did not model how much nitrogen must fill the growing 9 L chamber, escape around the approximately
400 mm perimeter or pass through a reservoir orifice quickly enough.

I freeze A11 on a non-contact annular-gap control, not a claimed flight seal. The controlled inputs
are in
[`analysis/fluxpiston_flow_parameters.json`](../analysis/fluxpiston_flow_parameters.json). The
calculation script and result do not exist in this declaration commit.

> **Execution correction, 2026-08-28, before any result:** my controlled file omitted the 8.0 g
> requirement value used only to calculate band 2 headroom. The first execution stopped on a
> `KeyError` before calculating a case or writing a result. I added `acceleration_limit_g: 8.0`;
> geometry, cases, sweep, equations and all nine bands are unchanged.

## Model I will use

I will command the gas stage 0.25 m/s below each final target and reserve the short electromagnetic
section for the last 0.25 m/s. I will compute constant mean chamber pressure from work, chamber-fill
mass by the ideal-gas law, and perimeter leakage as choked flow to vacuum. I will screen five radial
clearances from 0.05 to 0.50 mm and three gas temperatures from 250 to 330 K.

This is intentionally a conservative *flow-area* screen and an optimistic *pressure-control*
screen. It has no regulator dynamics, valve opening law, wall heat transfer, rarefied-flow
correction, guide contact, gas recirculation or exit plume.

## Frozen bands

| Band | My pass condition | Meaning of failure |
|---|---|---|
| 1 | Gas-stage acceleration is at most 7.8 g in both mass cases | The trim split does not create useful load headroom |
| 2 | Pressure headroom to the 8 g ceiling is at least 4% | A 2% pressure controller has no credible two-sided margin |
| 3 | Worst 0.50 mm / 250 K gas use is at most 10 g per shot | Controlled leakage costs enough fluid to challenge the architecture |
| 4 | Twelve worst-corner shots use at most 0.15 kg nitrogen | Campaign gas erases the low-mass premise |
| 5 | The equivalent 20 bar reservoir volume is at most 5 L | The gas store becomes a packaging problem before tank structure |
| 6 | Peak required 20 bar supply-orifice diameter is at most 6 mm | A compact fast valve cannot plausibly feed the growing chamber |
| 7 | The final 0.25 m/s trim needs at most 25 J kinetic correction | The short motor remains a bulk launcher |
| 8 | Every leakage point is reported, including the worst corner | I have hidden clearance sensitivity behind a nominal seal |
| 9 | Friction, contact and plume remain explicitly OPEN | A non-contact mass-flow screen is being presented as a qualified seal |

## Disposition rule

I will advance Fluxpiston to a regulator/blowdown transient only if bands 1–8 pass. Band 9 remains
OPEN by design and blocks CAD promotion. A passing A11 will mean “the gas quantity deserves a more
physical model,” nothing more.

## Result and disposition

I ran the full 30-point clearance/temperature grid without changing a band. The reference gas
stage reaches 11.55 m/s at 29.645 kPa mean pressure and 7.555 g, leaving 5.57% pressure headroom to
8 g before the short trim stage adds 0.25 m/s. The qualification gas stage reaches 9.75 m/s at
31.688 kPa and 5.384 g.

The worst corner is the 6 kg case at 0.50 mm and 250 K: 6.009 g nitrogen per shot including chamber
fill and continuum choked leakage. Twelve shots use 72.11 g, equivalent to 3.531 L at 20 bar and
330 K before hardware and margin. Peak equivalent feed diameter is 4.232 mm. Maximum trim kinetic
energy is 14.8125 J.

I promote Fluxpiston only to a dynamic regulator/chamber/blowdown calculation plus contact and
plume gates. Band 9 remains OPEN and blocks CAD. The controlled result is
[`analysis/results/fluxpiston_flow.json`](../analysis/results/fluxpiston_flow.json) and my generated
reading is [`docs/FLUXPISTON_FLOW.md`](../docs/FLUXPISTON_FLOW.md).
