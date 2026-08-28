# A12, my Fluxframe public chassis-mass screen

**State: RUN. All 5 executable frozen bands pass; 3 integration bands remain OPEN.**

A10 found that the current 0.37136 kg passive interface must displace 0.12136 kg to meet my 0.25 kg
net added-mass preference. A12 asks whether that threshold is even material relative to published
3U primary-structure masses. It does not assume my electromagnetic cage can carry a spacecraft.

The controlled comparators and sources are in
[`analysis/fluxframe_mass_parameters.json`](../analysis/fluxframe_mass_parameters.json). The
calculator and result do not exist in this declaration commit.

## Frozen bands

| Band | My pass condition | Meaning of failure |
|---|---|---|
| 1 | Required displaced mass is below every published structure-mass comparator | Gen5 needs to replace more mass than at least one whole reference chassis contains |
| 2 | Required displaced fraction is at most 50% of every comparator | Fluxframe must replace nearly the whole chassis merely to meet preference |
| 3 | A hypothetical full replacement yields at most 0.25 kg net addition for every comparator | Even total structural replacement cannot meet my preference |
| 4 | Current gross interface mass remains below the 0.40 kg absolute limit | Gen5 begins by violating the existing hard mass limit |
| 5 | I report the EnduroSat value as an upper bound, not guaranteed displaced mass | A less-than datasheet value has been converted into a false lower-bound credit |
| 6 | Bus-specific removed-part credit remains OPEN | Public chassis masses are being treated as proof of Fluxframe integration |
| 7 | Structural, thermal, electrical and magnetic equivalence remain OPEN | A mass subtraction is being presented as multifunctional qualification |
| 8 | CDS rail geometry, hard anodize, 75% contact and provider disposition remain OPEN | Gen5 has silently traded away dispenser compatibility |

## Disposition rule

If bands 1–5 pass, I may promote Fluxframe to selection of one bus and an explicit before/after
parts ledger. Bands 6–8 remain OPEN and block net-mass closure, CAD promotion and customer claims.

## Result and disposition

I ran the sourced arithmetic without changing a band. The required 121.36 g credit is 30.80–42.58%
of my three public chassis-mass comparators. Hypothetical full replacement produces -22.64 to
+86.36 g net added mass at the current 0.37136 kg Fluxrelay interface.

I award zero credit. I promote Fluxframe only to selection of one bus, a before/after parts ledger
and a coupled multifunctional cross-section. Structural, thermal, electrical, magnetic, rail and
provider evidence remain OPEN. The controlled result is
[`analysis/results/fluxframe_mass.json`](../analysis/results/fluxframe_mass.json) and my generated
reading is [`docs/FLUXFRAME_MASS.md`](../docs/FLUXFRAME_MASS.md).
