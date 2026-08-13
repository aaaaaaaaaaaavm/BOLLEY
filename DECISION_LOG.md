# Decision log

This is the compact index. Full arguments live in `docs/adr/`.

| ID | Date | Decision | Consequence | Record |
|---|---|---|---|---|
| D001 | 2026-08-13 | Accept a small passive spacecraft modification. | Universal compatibility becomes a fallback instead of the baseline. | [ADR-001](docs/adr/001-cooperative-payload-interface.md) |
| D002 | 2026-08-13 | Use an active long stator and passive reluctance rails. | No moving magnets, coils or powered spacecraft interface. | [ADR-002](docs/adr/002-passive-reluctance-rails.md) |
| D003 | 2026-08-13 | Freeze Phase 0 at 0–12 m/s, 8 g and 0.90 m for the 4 kg reference case. | The mission-useful differential is prioritised over VOLLEY's model-derived 16.388 m/s ceiling. | [ADR-003](docs/adr/003-phase-zero-duty.md) |
| D004 | 2026-08-13 | Treat 4 kg as the comparison case and 6 kg as the qualification sizing case. | A current maximum mass is not hidden behind the older reference case. | [ADR-003](docs/adr/003-phase-zero-duty.md) |
| D005 | 2026-08-13 | Do not include a paper, LaTeX tree or publication figures. | The repository remains an engineering decision record. | This log |
| D006 | 2026-08-13 | Commit bands before model results. | Git history records what would count as failure before the answer is known. | [Engineering method](docs/ENGINEERING_METHOD.md) |
| D007 | 2026-08-13 | Reject the A5a three-fin comb on an ideal tooth-edge force bound. | A5a remains an interface result; whole-face shear is not used as axial force evidence. | [ADR-006](docs/adr/006-edge-bound-redesign.md) |
| D008 | 2026-08-13 | Screen a four-fin, 6 mm passive quad-comb. | The smallest clean payload-side rescue must pass A5b before nonlinear analysis. | [ADR-006](docs/adr/006-edge-bound-redesign.md) |
| D009 | 2026-08-13 | Reject the conventional shared-pole quad-comb stator before FEA. | Its 2 mm throats cannot return the required flux; widening them breaks the face-width rule. | [A3b1](validation/A3b1_stator_throat_bound.md) |
| D010 | 2026-08-13 | Promote four-fin passive aluminium Fluxfoil to the Gen1 analytical lane. | Induction replaces the failed moving/shared magnetic return while preserving four-channel control. | [ADR-007](docs/adr/007-fluxfoil-baseline.md) |
| D011 | 2026-08-13 | Preserve A3c's 66.2% efficiency failure and screen 0.60 T as A3d. | The band stays fixed; only a launcher-side field input changes. | [ADR-008](docs/adr/008-fluxfoil-operating-point.md) |
| D012 | 2026-08-13 | Freeze the A3e series-flux loop as Gen1. | A real 20 mm core, 20-turn winding and 120 V pulse model now control CAD. | [ADR-009](docs/adr/009-serpentine-stator.md) |
| D013 | 2026-08-13 | Reject the Gen1 winding after A5c exact interference and pack checks. | A3e remains evidence, but its CAD-promotion disposition is superseded. | [ADR-010](docs/adr/010-fluxbridge-cage.md) |
| D014 | 2026-08-13 | Screen a passive magnetic-matrix/copper-ladder Fluxbridge blade. | A small unpowered payload modification is spent to remove the primary copper penalty at its source. | [ADR-010](docs/adr/010-fluxbridge-cage.md) |
| D015 | 2026-08-13 | Promote the passing A3f package to constrained optimisation, not hardware. | The 9.37 kg primary is buildable in section, but 26.9% source efficiency remains an explicit weakness. | [A3f result](docs/FLUXBRIDGE_CAGE.md) |
