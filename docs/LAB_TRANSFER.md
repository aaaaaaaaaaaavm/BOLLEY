# How I use VOLLEY-lab from Bolley

I keep Bolley's executed failures, passing models and controlled baseline in this repository. I do
not move them out when I decide an underlying principle may be useful elsewhere.

[VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) is now the shared architecture vault for
VOLLEY and BOLLEY. It contains hypotheses that are not yet allowed to change either flagship.

## What stays here

- every A1-A12 run sheet and generated result;
- the rejected buried return, comb, shared-pole and Fluxfoil winding geometries;
- the Gen2 field iterations that led to Fluxrelay;
- the A6h/A7c/A5e Gen3 controlled baseline;
- Fluxframe and Fluxpiston as the current named Gen5 and Gen6 questions;
- every open problem and the evidence boundary attached to it.

Those items explain Bolley. Moving them would make the present design look cleaner and the record
less true.

## What I send to the lab

I send an idea when it changes a premise rather than corrects an error. Current examples are:

- `VLAB-B001`, a no-inherited-constraints bus/stage co-design in which Fluxframe and Fluxpiston
  become one multifunctional spacecraft body;
- `VLAB-B002`, a powered cooperative spacecraft interface that explicitly reopens BOL-R-007 without
  changing the controlled requirement;
- `VLAB-B003`, distributed or staged Fluxpiston feed architectures aimed at P48;
- `VLAB-X001`, a quadrant leakage bearing that tries to turn P44's gas loss into lateral stiffness;
- `VLAB-X002`, a deployer-owned Fluxrelay secondary that may remove permanent magnets from VOLLEY's
  trim stage;
- shunted magnets, Thomson repulsion, selected springs, Strainrail, a carousel, burn-and-drop and
  the unmodified four-finger fallback.

The shared routing and frozen first gates are in the lab's
[`TRANSFER_LEDGER.md`](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab/blob/main/TRANSFER_LEDGER.md).

## What may return to Bolley

A lab branch may open a new Bolley ADR only if it:

1. passes bands written before its executable model;
2. closes a controlling defect such as P39, P41, P44, P46 or P48;
3. compares complete installed mass, energy, host impulse and failure concentration against the
   current target on the same boundary;
4. preserves a failed lab result rather than silently absorbing its useful half;
5. does not call a provider assumption, bus credit or unmeasured seal property evidence.

I use the lab to take larger risks. I do not use it to lower the standard for bringing one back.
