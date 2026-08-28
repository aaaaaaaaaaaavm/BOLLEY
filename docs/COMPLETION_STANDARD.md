# My completion standard for Bolley

I do not use later generation labels as a substitute for finishing the selected Gen3 Fluxrelay
baseline. I use VOLLEY's mature repository as a depth standard while keeping Bolley's different
architecture and every real failed branch intact.

## Practices I carry across

| Source record | Practice I retain | Bolley implementation |
|---|---|---|
| VOLLEY | Attribute mass, energy and risk to the requirement that causes them | P39 and P41 require packaged pulse and installed-machine accounting rather than active copper alone |
| VOLLEY-lab | Preserve a rejected idea with its stopping result and revival condition | Failed magnetic paths, CAD collisions and exploratory Fluxframe/Fluxpiston work remain reproducible |
| Engineering Evidence Toolkit | Check provenance, links, generated artifacts and the failure path | `tools/check_repo.py` verifies stage sets, deterministic results, manifests, links and repository metadata |
| orbital-deployment-trade-study | Separate a command from the outcome and require an independent path | P5 and P10 keep commanded force distinct from six-degree-of-freedom release behaviour |
| pulsed-linear-motor-design-lab | Do not call a wrapper around the same calculation independent | P25 and P29 require a genuinely separate transient/3D field implementation |
| GatewayCX | Give claims evidence classes and exercise fault semantics | A9 must distinguish cell, module, timing, sensing and recovery faults |

## The bar I enforce

Before I call the repository computationally complete:

1. Every live computable defect has an executable result or a recorded rejection.
2. Every material claim maps to an assumption, external datum, controlled model, cross-check,
   measurement or explicit decision.
3. Generated results reproduce; CAD and binary artifacts retain hashes and manifests.
4. Controlling physical domains receive an independently implemented check.
5. Bad inputs, stale artifacts and declared operational faults cannot silently pass.
6. Installed mass includes structure, containment, cooling, harness, sensing and electronics.
7. Hardware, host-data and provider blockers remain visible after computation ends.

Meeting this bar would complete the computable engineering record. It would not mean I have built,
fired, measured, qualified or flown Bolley.
