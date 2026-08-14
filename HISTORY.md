# Project history

I did not begin Bolley as a renamed copy of VOLLEY, and I have not backdated its record.

## 22 March 2021 — the question that became VOLLEY

I began VOLLEY with a direct mission question: could a CubeSat leave a host spacecraft at a
controlled velocity without carrying its own propulsion? In the early architecture I kept the
CubeSat conventional and put the electromagnetic reaction hardware on a reusable moving sled.
That choice protected payload compatibility, but it also created the mass, braking and return
mechanisms that later became my design's largest penalties.

## 13 August 2026 — the premise changes

I began Bolley when I deliberately reversed one VOLLEY constraint: I would accept a small, passive
CubeSat modification if it removed much more hardware from the launcher. My starting thought was
the “small price for salvation”: spend a few hundred grams of passive interface mass once, then
accelerate the spacecraft directly while the host retains all active electronics.

I made the first Bolley commit on 13 August 2026. VOLLEY's 2021 origin explains my problem lineage;
I do not use it as Bolley's creation date.

## The path I took on the first day

I did not reach the current concept in a straight line:

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
14. A8b searched cage length, cell pitch, current and conductor area together. Seventy-seven
    candidates closed every analytical band; `n27_p45.3_I380_A10.4` became the single Gen2.7
    Fluxrelay point promoted to fresh field and circuit reclosure.

I retain every rejected branch because it explains why I arrived at the current geometry. In
VOLLEY, my stock-CDS-rail control has now failed its A30 edge-effect calculation, while a wider
conductive-plate control survives analytically. I have therefore narrowed Bolley's active question:
does my selected cooperative cage retain its margin in fresh nonlinear field and sectional-circuit
models, and can its four-channel interface justify 0.371 kg against the lighter wide plate?

## Authorship

I am **Adityavardhan Mishra**. I conceived Bolley, I direct it, and I maintain it. This repository
is my continuous engineering record: my requirements, design decisions, calculations, CAD,
failures and, when I have them, test evidence.
