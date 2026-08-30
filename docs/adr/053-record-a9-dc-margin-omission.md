# ADR-053: record the DC-link margin band omitted by A9/A9b

Date: 2026-08-31

## Context

A8b and A7c require both a maximum 48 V DC link and at least 10% margin on that link. A9's run
sheet inherited the 48 V absolute limit but did not carry the separate 10% margin Boolean into its
13-band transient screen.

The omission does not reverse A9b. Its maximum healthy additive link demand is
14.149322762821571 V, which leaves `48 / 14.149322762821571 - 1 = 2.3923885124822846`, or 239.24%,
margin by the same A7c definition.

## Decision

I preserve A9 and A9b unchanged. I restore the inherited 10% DC-link margin in every downstream
winding/drive redesign.

I do not add a new A9b pass claim or rewrite its 13-band count. The missing check is recorded here
because a later higher-turn winding can make it controlling even though the current point is far
from the limit.

## Consequence

The largest downstream healthy link demand that satisfies the inherited margin is
`48 / 1.10 = 43.63636363636363 V`. Fault cases retain A9's absolute 48 V limit unless a separate
fault-margin requirement is declared before its model.
