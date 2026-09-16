# A9g: selected 12-turn electrical envelope reclosure

Declared 2026-09-16 before implementation or execution. Starting source: `28cc2a3459a77f82cc87ac7bddef27cf93aa9083`.

I carry A9f's selected 12-turn, 1,520 A-turn partition through the existing A9 time-domain handoff model, then expose the energy margin left for omitted losses. This is an ideal-current-tracking circuit reclosure. It does not replace a nonlinear solve of the individual A5h conductors or validate supplier pulse ratings.

## Fixed inputs and experiment

Use all existing A7c corners and A9 healthy/failed-cell cases. At constant MMF and slot copper, apply I / 3, R * 9 and L * 9 to the 4-turn inputs, including the inherited steady voltage terms. Run 100 and 200 handoff samples. Keep the existing A9 physical bands, residual floor and 48 V link, plus A9f's healthy 10% voltage margin and 900/1,500 J energy caps.

Compare rerun current, voltage and winding/magnetic-energy outputs against analytical turn-scaling. Use relative 1e-9 and absolute 1e-8 for the scaling identity; coarse/fine controlling energy and voltage must agree within 1%. No physical band changes are permitted. A model failure remains in the record.

For the local-bridge topology, reproduce A9f's 25 C conduction baseline within 1e-8 J. Evaluate assumed conduction-resistance multipliers 1/1.25/1.5/2 and additional per-shot losses 0/5/10/20 J against the unchanged energy caps. These are sensitivity assumptions, not supplier temperature curves or switching measurements. Record remaining joules and every failed corner. Report the maximum allowable conduction multiplier when added loss is zero, and the maximum added loss at multiplier one.

Reconcile selected turn count, current, conductor area and copper-volume evidence against A5h/A5g and preserve A5f failure. Report the 2.5488 kg module-only lower bound separately from installed mass. P11, P39 and P40 remain open; P38 retains its previous bounded disposition. No flight/prototype-readiness claim follows.

Required outputs: source-hashed generated JSON/report, independent scaling and corruption tests, integration into the repository checker, and a precise next field/switching/thermal experiment.
