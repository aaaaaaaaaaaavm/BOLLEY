# Engineering method

Bolley inherits VOLLEY's best habit: it tries to make self-deception inconvenient.

## Evidence labels

Every important number belongs to one of four classes.

| Label | Meaning |
|---|---|
| **ASSUMPTION** | Chosen for a screen. It has no external authority. |
| **EXTERNAL DATA** | Read from a named standard, paper or supplier document. |
| **MODEL OUTPUT** | Produced by executable analysis from recorded inputs. |
| **MEASUREMENT** | Produced by identified hardware and instrumentation. |

A model output does not become a measurement because two scripts agree. Agreement between
independent formulations is useful and will be called a **cross-check**.

## Run order

1. State the question.
2. State the input provenance.
3. Declare numerical bands and what happens at each failure.
4. Commit the run sheet.
5. Run the analysis or experiment.
6. Commit raw/generated outputs without editing them into a preferred answer.
7. Update the design, requirement or defect register. Never retroactively widen the band.

## Generated files

Files carrying a generated notice are owned by a script. Change the script or its inputs, rerun
it and commit both. The repository check regenerates deterministic outputs in memory and compares
them with the committed versions.

## Corrections

Corrections remain visible. The replacement records:

- what was wrong;
- how it was found;
- which conclusions moved;
- which conclusions survived;
- the commit containing the correction.

Deleting an uncomfortable result is not correction.

## Scope

The repository may contain requirements, ADRs, models, test procedures, CAD parameters, supplier
evidence and measurements. It deliberately does not contain a paper-production pipeline.

