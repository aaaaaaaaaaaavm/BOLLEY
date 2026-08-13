# Project history

Bolley did not begin as a renamed copy of VOLLEY, and its record is not backdated.

## 22 March 2021 — the question that became VOLLEY

Adityavardhan Mishra began VOLLEY from a direct mission question: could a CubeSat leave a host
spacecraft at a controlled velocity without carrying its own propulsion? The early architecture
kept the CubeSat conventional and put the electromagnetic reaction hardware on a reusable moving
sled. That choice protected payload compatibility, but it also created the mass, braking and
return mechanisms that later became the design's largest penalties.

## 13 August 2026 — the premise changes

Bolley begins when Mishra deliberately reverses one VOLLEY constraint: accept a small, passive
CubeSat modification if it removes much more hardware from the launcher. The starting thought was
the project's “small price for salvation”: spend a few hundred grams of passive interface mass
once, then accelerate the spacecraft directly with all active electronics retained by the host.

The first Bolley commit therefore starts on 13 August 2026. VOLLEY's 2021 origin explains the
problem lineage; it is not Bolley's creation date.

## The design path on its first day

The concept did not travel in a straight line:

1. A buried passive reluctance return failed its moving-iron mass screen.
2. A three-fin comb fit the envelope but failed an ideal force upper bound.
3. A four-fin comb recovered the ideal edge-force margin, then failed stationary throat flux.
4. A passive aluminium Fluxfoil passed a revised induction screen and an explicit Gen1 circuit.
5. Gen1 CAD exposed a 66.7:1 winding-window deficit and rejected the package.
6. The Fluxbridge cage replaced the continuous aluminium fin with a perforated magnetic matrix
   and shorted copper ladder, keeping the payload side thin, passive and unpowered.
7. A robust search selected Gen2; nominal CAD passed all 13 fit bands.
8. The first independent nonlinear field solve rejected that Gen2 operating point on field,
   stationary-core peak and inductance.
9. Gen2.1 through Gen2.4 redistributed the stationary return and passive rib; each failed one or
   more predeclared local-field bands and remains as rejected evidence.
10. Gen2.5 Fluxweb layered magnetic continuity beneath its copper rungs and became the first
    13/13 transverse-field pass.
11. A7a rejected Fluxweb's four-lane cage on heat, current density, secondary efficiency and
    reference energy.
12. Gen2.6 Quintweb spent most of the absolute interface-mass allowance on a fifth lane. A6g
    passed 13/13 and A7b closed all four translator failures; only hot winding resistance kept the
    reference shot above 900 J.
13. A8a checked the finite axial intervals. It rejected the 900 mm stator because the 336 mm cage
    leaves it during the claimed 900 mm powered travel. A simple full-overlap extension also
    failed the stationary-primary mass band.

Every rejected branch remains in the repository because it explains why the current geometry
exists. The active question is now narrower: can a shorter aft-positioned Quintweb cage and a
sectional primary close engagement, installed mass and the A7b hot-energy corner together, or does
the existing-rail control in VOLLEY make the cooperative interface unnecessary?

## Authorship

Bolley is conceived, directed and maintained by **Adityavardhan Mishra**. The repository records
his requirements, design decisions, calculations, CAD, failures and future test evidence as one
continuous engineering project.
