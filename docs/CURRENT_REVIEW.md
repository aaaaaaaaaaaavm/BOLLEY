# Current Fluxrelay review

I generate this review from the committed result files with `tools/make_review_snapshot.py`.
It supplements the historical [run status](../validation/STATUS.md) with the later drive and winding sequence.
A passing screen means its declared calculation checks passed. The design disposition can still be a rejection.
Nothing here is hardware evidence.

![Current drive and winding evidence](../figures/current-review.svg)

| Run | Screen checks | Design disposition | Remaining boundary |
|---|---|---|---|
| [A9b](../validation/A9b_sectional_drive_residual_reclosure.md) | PASS | `A9B_PASS_RETAIN_FLUXRELAY_FOR_SUPPLIER_AND_PACKAGING_CLOSURE` | Model reclosure; supplier and package work remains |
| [A9c](../validation/A9c_hot_winding_margin.md) | PASS | `A9C_TARGET_DEFINED_P40_REMAINS_OPEN` | Resistance/temperature allowance; P40 remains open |
| [A9d](../validation/A9d_supplier_bridge_lower_bound.md) | PASS | `A9D_LOWER_BOUND_SURVIVES_P11_P39_P40_REMAIN_OPEN` | Conduction lower bound; full electronics remain open |
| [A9e](../validation/A9e_selector_realization_lower_bound.md) | PASS | `A9E_NO_SELECTOR_PROMOTED_SECTIONAL_PARTITION_REQUIRES_REDESIGN` | No selector promoted; electrical partition requires redesign |
| [A9f](../validation/A9f_turn_current_exchange.md) | PASS | `A9F_SELECT_12TURN_LOCAL_BRIDGE_FOR_FRESH_FIELD_CAD_AND_SWITCHING_CLOSURE` | Selected for fresh field, switching and package checks |
| [A5f](../validation/A5f_gen3_12turn_winding.md) | FAIL | `A5F_FAIL_FIXED_INNER_SPANS_EXCEED_A5E_COPPER_VOLUME` | Failed copper-volume gate; failure retained |
| [A5g](../validation/A5g_gen3_12turn_path.md) | PASS | `A5G_PASS_PROMOTE_SELECTED_12TURN_WINDING_TO_DETAILED_CAD` | Analytical path fit; detailed CAD follows |
| [A5h](../validation/A5h_gen3_12turn_detailed_cad.md) | PASS | `10/10 nominal-CAD bands` | Nominal envelopes only; not a manufacturing release |
| [A9g](../validation/A9g_selected_winding_reclosure.md) | PASS | `BOUNDED_RECLOSURE_ONLY_HOT_SWITCHING_AND_FIELD_OPEN` | Six of sixteen assumed loss corners pass; hot switching remains open |

## The selected electrical screen

These A9f values use the declared scaling and supplier conduction assumptions. They do not include a complete hot switching implementation.

| Quantity | Model output |
|---|---:|
| Turns per cell | 12 |
| Rated phase current | 126.667 A |
| Reference source energy | 889.719 J |
| Qualification source energy | 1296.786 J |
| Healthy required DC link | 42.448 V |
| Failed-cell required DC link | 45.023 V |
| Supplier modules | 108 |
| Module-only mass | 2.5488 kg |

A9c's earlier configuration has 2.252 J remaining below its reference cap,
equivalent to only 2.669 C beyond its inherited hot-winding corner under that model.
That is not the margin of the later A9f candidate; the configurations must stay separate.

## Selected-partition reclosure

[A9g](SELECTED_WINDING_RECLOSURE.md) reruns the ideal-current handoff model at twelve turns.
It reproduces the current/voltage/energy scaling at two resolutions. The selected 25 C
conduction point leaves 10.280918 J below the reference cap; only six of sixteen assumed
conduction/additional-loss corners pass. This does not close the actual winding field or hot switching.

## What I would close next

1. Check RMS, peak, internal-path and package current definitions against the supplier data before crediting a device rating.
2. Re-solve the field/current distribution for the actual A5h winding, including terminals and lead routing.
3. Couple hot conduction, switching, parasitics, protection, supply sag and thermal paths across the full campaign.
4. Carry the lane gap and guide alignment through manufacturing, thermal and dynamic tolerances.
5. Close installed mass and six-degree-of-freedom release/fault behaviour before a full-system prototype design review.

The [completion standard](COMPLETION_STANDARD.md) still applies. The shared
[prototype programme](https://github.com/aaaaaaaaaaaavm/VOLLEY/blob/main/docs/PROTOTYPE_READINESS.md)
defines the intended build package and the dependency order. These are open work, not newly passed gates.

## Reproduction and provenance

Run `python tools/make_review_snapshot.py --check` to check these surfaces against their source files.
This does not rerun the physical analyses. `python tools/check_repo.py` checks the existing repository pipeline;
full solver and CAD reconstruction remain distinct from artifact checks.

| Source | SHA-256 |
|---|---|
| [sectional_drive_a9b.json](../analysis/results/sectional_drive_a9b.json) | `ca6a03cfb21ff5760d1764725571e9f57c9e9fdd4e0226cbc19284f9bed2b972` |
| [hot_winding_margin.json](../analysis/results/hot_winding_margin.json) | `b79bd435a70a060a7ff8eb8afb4af39afd1cdf2c4e9eadc892a0d46d8caf20f1` |
| [supplier_bridge_screen.json](../analysis/results/supplier_bridge_screen.json) | `f0065bf5d463e3ce56aaf3397242dd978fbbfdc808fd7a57e302b240e7eb26d0` |
| [selector_realization_screen.json](../analysis/results/selector_realization_screen.json) | `19c96292498b91947fcaab70e926c8152ea512927bf4556c417c0c2dc89d5753` |
| [turn_current_exchange.json](../analysis/results/turn_current_exchange.json) | `7e112a7a432771ae9ede17704f45f80275e3967f147564db9655cedae8ed35bd` |
| [gen3_12turn_winding_fit.json](../analysis/results/gen3_12turn_winding_fit.json) | `02e347838230732e90b35291ad581d8c777bae2cdfb3099aad87fda4c8237325` |
| [gen3_12turn_path_fit.json](../analysis/results/gen3_12turn_path_fit.json) | `0a721b355f1b719a0d547fa97d7fc16833e103a21311a18f16a9f943de91d1a0` |
| [gen3_12turn_detailed_fit.json](../analysis/results/gen3_12turn_detailed_fit.json) | `749d7f0b167a0e6d32d6cb3f0d5699ecca57c1ccbce801a1ea212a12a2cf59b7` |
| [selected_winding_reclosure.json](../analysis/results/selected_winding_reclosure.json) | `dcf6422a359cc78f2199c951579837e9cc27eb590db8e6a6ca772160042e9e1d` |
