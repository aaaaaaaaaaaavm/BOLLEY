# Project history

I did not begin Bolley as a renamed copy of VOLLEY, and I have not backdated its record.

## 28 August 2026 — I made the next generations change the premise

I reconstructed and promoted the completed A5e nominal CAD result, then used VOLLEY's
requirement-attribution result to question the term Bolley actually removes. I froze A10 before its
calculator existed. It exposed an inconsistent 12 m/s / 0.90 m / 8 g triplet, quantified the
121.36 g Gen5 displaced-mass target and identified a low-pressure full-face piston plus short trim
stage as the Gen6 direction. I corrected the reference duty to 11.8 m/s and promoted only the next
gates, not unbuilt machines.

I then froze A11 before its calculator. One missing 8 g control value stopped the first execution
before results; I recorded and corrected it. The completed 30-point screen found that even the
0.50 mm, 250 K control uses 6.009 g nitrogen per shot. I promoted gas quantity to a dynamic model
while keeping seal/contact and plume evidence open.

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

## 14 August 2026 — I replace the selected-point field surrogate

I froze A6h before execution, then solved the exact selected 380 A point on three independently
specified nonlinear meshes. All 13 declared bands pass. I now carry the worst 1.52843 T stationary
peak, 1.34336 T moving peak and 4.81156 uH three-cell phase-window inductance into A7c. I have not
treated that model result as force, switching or hardware evidence.

I then froze A7c on that exact point and repeated all four cage/circuit corners over both 21 by 21
CG grids. Every corner passes all 29 hard bands. The controlling reference shot is 893.412 J,
leaving 6.588 J below my 900 J band. I opened provisional Gen3 CAD and transient sectional-drive
work, but I did not promote a model result to a hardware claim.

I next froze A5e and built a new Gen3 assembly around that exact point. I did not stretch or rename
the old 900 mm Gen2 geometry. All 17 nominal CAD bands pass: eight STEP masters, eight STL previews
and ten inspected renders preserve the five-lane cage, 27-cell sectional primary, exact winding
volume, zero nominal solid interference and the 2.25 mm endpoint guard. I promoted the geometry to
tolerance, structure and A9 work, not to manufacturing or flight evidence.

I retain every rejected branch because it explains why I arrived at the current geometry. In
VOLLEY, my stock-CDS-rail control has now failed its A30 edge-effect calculation, while a wider
conductive-plate control survives analytically. I have therefore narrowed Bolley's active question:
does my selected cooperative cage retain its narrow margin through transient drive work,
toleranced structure and later hardware, and can its four-channel interface justify 0.371 kg
against the lighter wide plate?

## 14 August 2026 — VOLLEY measures the premise both projects share, and the answer is a negative

I started Bolley because VOLLEY's sled was 9.445 kg and most of the shot energy accelerated
launcher hardware. My answer was to delete the sled by moving the reaction interface onto the
spacecraft. **That answer has now been tested from the other side, and it holds — but not for the
reason either project assumed.**

VOLLEY's A35 attributed every kilogram of its 84.53 kg rollup to the requirement that causes it,
then deleted requirements one at a time across all 64 corners. Three results bear directly on this
repository:

| | |
|---|---|
| **The mover is 11 % of dry mass** | Deleting it entirely — which is what I do here — saves a ninth. **49.23 kg survives every deletion of every requirement.** |
| **The mover is 70 % of *accelerated* mass** | Which is the number both projects read, and it is why the sled looked like the problem. Both figures are true and they say different things. |
| **An unmodified satellite costs *nothing*** | No item in VOLLEY's ledger exists *because* the satellite is unmodified. The sled is caused by the choice that a **reusable mover carries the magnets**, and the unmodified requirement only implies that choice when nothing else can carry them. |

**Bolley is the corroboration, and it is the stronger evidence of the two.** VOLLEY computed the
result; here I *built* the deletion — seven field iterations, twenty-five run sheets, a co-design
search over 2,856 candidates — and the mass came back as a **15.91 kg primary**. It came back
because I kept the requirement neither project questioned: **that the energy arrives during
the shot.** A35 measures that requirement at **28.1 %**, the largest single driver in the machine,
against the mover's 13.6 %.

**What VOLLEY did with that.** ADR-032, 2026-08-14: the payload is accelerated directly by cold gas
along a rail a spent upper stage provides. No mover, no stator, no bank — 25 to 131 W of charging
over the sixty seconds already spent indexing, and a 1.71 litre bottle for twelve shots.

**What it means here.** My Fluxrelay is a **pulse machine**: 380 A, 27 cells, a 1.2231 m
sectional primary, and P11 still records that no capacitor, inverter, switch or cable has a
supplier-backed pulse rating for the duty. **The premise I reversed was not the expensive
one.** Whether a cooperative interface is worth 0.371 kg of spacecraft mass is a live question;
whether it is worth it *while keeping the pulse* is a question A35 has now answered for the
sibling design.

**I retract nothing.** A8b's selected point stands, its bands stand, and
A6h and A7c remain my next kill gates. What changes is the comparison: the sibling design is no
longer a heavier version of the same idea, and the honest reading of my own P39 — *the
15.908 kg primary leaves 92 g for the active-material band and excludes structure, cooling, wiring
and power electronics* — is that it is the same finding arriving by a different route.

## Authorship

I am **Adityavardhan Mishra**. I conceived Bolley, I direct it, and I maintain it. This repository
is my continuous engineering record: my requirements, design decisions, calculations, CAD,
failures and, when I have them, test evidence.
