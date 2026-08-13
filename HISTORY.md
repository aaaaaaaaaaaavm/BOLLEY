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

Every rejected branch remains in the repository because it explains why the current geometry
exists. The active question is now narrower: can Gen2.1 redistribute the stationary return flux
without surrendering the passive cage, the 6.5 mm interface envelope or the no-sled architecture?

## Authorship

Bolley is conceived, directed and maintained by **Adityavardhan Mishra**. The repository records
his requirements, design decisions, calculations, CAD, failures and future test evidence as one
continuous engineering project.
