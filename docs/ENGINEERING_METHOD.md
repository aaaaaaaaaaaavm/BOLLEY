# Engineering method

I carry VOLLEY's most useful habit into Bolley: I try to make self-deception inconvenient.

## Evidence labels

I put every important number in one of four classes.

| Label | Meaning |
|---|---|
| **ASSUMPTION** | Chosen for a screen. It has no external authority. |
| **EXTERNAL DATA** | Read from a named standard, paper or supplier document. |
| **MODEL OUTPUT** | Produced by executable analysis from recorded inputs. |
| **MEASUREMENT** | Produced by identified hardware and instrumentation. |

I do not turn a model output into a measurement because two scripts agree. I call agreement
between independent formulations a **cross-check**.

## Run order

1. I state the question.
2. I state the input provenance.
3. I declare numerical bands and what happens at each failure.
4. I commit the run sheet.
5. I run the analysis or experiment.
6. I commit raw/generated outputs without editing them into a preferred answer.
7. I update the design, requirement or defect register. I never retroactively widen the band.

## Generated files

I treat every file carrying a generated notice as script-owned. I change the script or its inputs,
rerun it, and commit both. My repository check regenerates deterministic outputs in memory and
compares them with the committed versions.

## Corrections

I keep corrections visible. When I replace a result, I record:

- what was wrong;
- how it was found;
- which conclusions moved;
- which conclusions survived;
- the commit containing the correction.

I do not call deleting an uncomfortable result a correction.

## Scope

I use this repository for requirements, ADRs, models, test procedures, CAD parameters, supplier
evidence and measurements. I deliberately keep a paper-production pipeline outside its scope.
