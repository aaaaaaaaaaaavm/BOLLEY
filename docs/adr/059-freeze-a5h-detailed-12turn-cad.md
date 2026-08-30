# ADR-059: freeze the A5h detailed 12-turn CAD

Date: 2026-08-31

## Context

A5g closes the nominal winding path analytically. The result still represents each turn by dimensions and centreline length rather than a solid. A5e's old homogeneous ring cannot establish that twelve insulated turns replicate through the actual 27-cell core without collision.

## Decision

Before creating `cad/build_gen3_12turn.py`, I freeze A5h on the exact A5g selected dimensions and the unchanged A5e stator core.

I require individual maximum-insulation conductor envelopes in one cell, an ABC module and all 27 cells on one face. The same inherited A5e solid-intersection ceiling applies. I also require deterministic STEP/STL masters for those four CAD scopes.

I do not include bridge modules, leads, terminals or cooling in A5h. Those belong to the packaged electrical gate after the winding itself survives exact geometry.

## Consequence

A5h may reject A5g without changing the analytical winding result. A pass promotes the 12-turn winding only to package, switching and tolerance reclosure. The existing four-turn A5e assembly remains the controlled full-system CAD until those later gates pass.
