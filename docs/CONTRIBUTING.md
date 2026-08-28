# Contributing to Bolley

I welcome discrepancies, independent implementations and evidence that can kill or narrow the
design. I do not want plausible-looking numbers without provenance.

## Ground rules

1. Treat controlled parameters and scripts as the source of computed results. Do not hand-edit a
   generated JSON, report, render manifest or archive manifest.
2. Freeze acceptance bands before executing a new gate. A failed band changes the design or
   remains a failure; it does not move after the answer appears.
3. Label every value as an assumption, external datum, model output, cross-check or measurement.
   Nothing in this repository is currently a hardware measurement.
4. Preserve rejected branches and superseded results. Add a new gate or decision record rather
   than rewriting an old failure into the current architecture.
5. Keep narrative claims in my authored first-person voice. Neutral equations, tables and field
   names may remain impersonal.
6. Keep paper production outside this repository. Bolley is the engineering record.
7. Run `python tools/check_repo.py` before proposing a change. For a narrow generated artifact,
   also run its own `--check` command.

## Reporting a discrepancy

Use the repository's reproduction-discrepancy issue template. Include the controlled input,
script, committed value, reproduced value, environment and whether the discrepancy changes a
pass/fail disposition. If a number is not traceable, say so instead of reconstructing it.

## Evidence boundary

A model-to-model agreement is a cross-check, not validation. A clean CAD Boolean is nominal fit,
not a manufacturing release. A passing repository audit establishes internal consistency, not
physical truth. I keep those distinctions in any accepted contribution.

## Licence

Contributions accepted into this repository are distributed under [CC BY 4.0](../LICENSE). By
contributing, you confirm that you have the right to supply the material on those terms.
