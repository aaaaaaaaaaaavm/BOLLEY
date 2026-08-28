# Bolley in one page

Bolley asks whether a CubeSat can accept a few hundred grams of passive reaction hardware so the
launcher can remove VOLLEY's moving sled, brake and return stroke while keeping windings,
switching, sensing and stored energy on the launcher.

My selected baseline is Gen3 Fluxrelay: a 318.6 mm five-lane passive cage on the spacecraft and
four stationary 27-cell face channels over a 1.2231 m active stator. A6h passes its nonlinear
field gate, A7c passes its selected circuit/energy corners, and A5e passes nominal CAD. A7c leaves
only 6.588 J under the 900 J reference cap, so A9 sectional switching remains a controlling gate.

That is not completion. My live defect register still requires sectional switching, transient 3D
fields, tolerance, structure, thermal cadence, EMC, six-degree-of-freedom release and complete
packaged power/mass. Supplier, hardware and provider evidence remain separate blockers.

I preserve every real failed branch. The result is a reproducible design record, not a claim that
Bolley has been built, fired, measured, qualified or flown.

Start with [`README.md`](README.md), [`docs/COMPLETION_STANDARD.md`](docs/COMPLETION_STANDARD.md),
[`docs/PROVENANCE.md`](docs/PROVENANCE.md) and [`validation/STATUS.md`](validation/STATUS.md).
