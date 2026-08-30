# ADR-050: freeze A9c as a resistance-ceiling calculation

Date: 2026-08-31

## Context

A9b leaves the controlling reference shot at 897.74844054099 J against the unchanged 900 J cap.
P40 remains open because A7c's 1.25 resistance multiplier is a model corner rather than a measured
or supplier-bounded winding state.

## Decision

Before the A9c executable exists, I freeze a calculation that solves the inverse problem: the
maximum phase-resistance multiplier allowed by 900 J after A9b's selector overhead.

I use only the committed A7c 1.00x/1.25x resistance corners, A9b's controlling result and the NIST
standard-copper temperature coefficient cited in the run sheet. I do not choose a convenient hot
winding temperature first.

## Consequence

A9c can define the resistance/temperature target a supplier or coupon must beat. It cannot close
P40 without a real winding resistance bound and the remaining electrical-chain losses.
