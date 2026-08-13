# Bolley

**A cooperative electromagnetic CubeSat deployer that spends a few hundred grams on the
spacecraft to remove kilograms of machinery from the launcher.**

> **Status:** Phase 0 design study. Nothing has been built, measured, qualified or flown.
> Every number in this repository is either an assumption, a first-order model output or
> external evidence labelled as such.

VOLLEY asked whether an unmodified CubeSat could receive a programmable deployment velocity
without carrying propulsion. Its answer used a reusable magnetic sled. The model worked, but
the sled became 9.445 kg: most of the energy accelerated launcher hardware and most of the
mechanism existed to stop and return it.

Bolley changes one premise. A compatible CubeSat carries four **passive reaction interfaces**.
All windings, switches, sensors and stored energy remain on the launcher. The spacecraft becomes
the passive translator of a segmented linear electromagnetic machine.

That small concession removes the launch sled, the post-release brake and the return stroke.

A3a found that the original buried corner-return rail was not an elegant flux path: sizing its
moving return iron breaks the declared mass logic. The current primary candidate is a thin
three-fin comb on each broad face between opposed stationary pole webs. A5a screens that moving
interface at 121.2 g and inside preliminary CubeSat envelope guidance. A single-sided aluminium
induction lane is the fallback. The comb has not passed provider review, FEA, structural analysis
or test.

## The proposed machine

- Four independently controlled face channels apply axial force around the spacecraft.
- Software distributes force so its centroid follows the declared payload centre of gravity.
- Six 150 mm stator tiles provide a 0.90 m acceleration zone.
- The Phase 0 reference duty is a 4 kg 3U payload, 8 g and approximately 12 m/s.
- A 6 kg 3U is the qualification sizing case, not silently treated as a 4 kg satellite.
- No permanent magnets, powered spacecraft hardware, pyrotechnics or pressure vessels are added.
- An independent gate carries ascent loads and prevents an uncommanded deployment.
- When the field ends, the CubeSat coasts out. No moving launcher member follows it.

## What is not claimed

Bolley has not demonstrated force density, commutation voltage, thermal margin, electromagnetic
compatibility, tip-off, rail life, cost or customer acceptance. The current calculations are
screens that decide which coupon to build. They are not validation of the machine.

The exact combination may be unusual. That is not proof of novelty or patentability.

## Start here

1. [`REQUIREMENTS.md`](REQUIREMENTS.md) — what the machine must do.
2. [`docs/CONCEPT.md`](docs/CONCEPT.md) — architecture and shot sequence.
3. [`docs/KILL_CRITERIA.md`](docs/KILL_CRITERIA.md) — numbers that can end the concept.
4. [`validation/README.md`](validation/README.md) — why bands are written before runs.
5. [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) — the work that remains.
6. [`docs/TOPOLOGY_SCREEN.md`](docs/TOPOLOGY_SCREEN.md) — why the original flux return was rejected.
7. [`docs/INTERFACE_FIT_SCREEN.md`](docs/INTERFACE_FIT_SCREEN.md) — the comb-fin envelope and allocation result.
8. `docs/BASELINE.md` — generated only after the first declared runs complete.

## Repository rules

1. Requirements precede calculations.
2. Validation bands precede results and are never widened after a run.
3. Model-to-model agreement is a cross-check, not experimental validation.
4. Generated results are changed through their scripts, never by hand.
5. A failed result changes the design or kills it. It does not change the threshold.
6. Assumptions, external data, model outputs and measurements are never mixed without labels.
7. This repository is an engineering record, not a paper-production project.
