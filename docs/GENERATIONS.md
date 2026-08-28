# The generations I now mean

I use a generation number only when the controlling claim changes. A longer stator, a smoother
render or a renamed winding is not a new generation.

| Generation | Question I require it to answer | Architecture | Evidence boundary |
|---|---|---|---|
| Gen3, Fluxrelay | Can my cooperative passive cage and sectional primary close field, circuit and nominal geometry together? | Five-lane magnetic/copper cage; 27-cell four-face primary | A6h, A7c and A5e pass as models; no hardware exists |
| Gen4, controlled Fluxrelay | Can the selected machine switch, tolerate a failed cell, fit its structure/cooling/electronics and retain its narrow energy margin? | Gen3 hardware plus explicit sectional commutation and packaged launcher | A9 transient, tolerance, structure, thermal and packaged-mass gates remain open |
| Gen5, Fluxframe | Can the spacecraft-side hardware earn its mass by replacing structure, thermal spreading, grounding and guidance hardware rather than being an added cage? | I co-design the passive electromagnetic lanes as a multifunctional side-frame | A12 shows the public mass envelope is large enough to investigate; I still grant zero credit until a bus-specific ledger and coupled models exist |
| Gen6, Fluxpiston | Can I delete the pulse chain by making the cooperative interface the pressure piston, while a short electromagnetic section performs only trim, centring and exit shaping? | Low-pressure stage tube + passive aft pressure cup/seal land + short Fluxrelay/null-flux trim | A10 and A11 bound ideal work and controlled leakage; contact, gas transient, 6-DOF exit and host integration remain kill gates |

## Why Gen5 is not “lighter Fluxrelay”

My 0.37136 kg interface misses the 0.25 kg preference by 0.12136 kg. Removing 121 g from the cage
may destroy the field path I already fought to close. Gen5 instead asks whether that mass can
replace ordinary spacecraft mass. I count only *net* added mass:

\[
m_{net}=m_{Fluxframe}-m_{displaced\ structure}-m_{displaced\ thermal}-m_{displaced\ harness}.
\]

I do not award the credits because multifunctional structures exist in the literature. I use that
work only to justify the design question. A particular CubeSat must show which rail, frame, heat
spreader, ground strap or shield is actually removed.

## Why Gen6 is not “VOLLEY copied into Bolley”

VOLLEY puts a small piston in a long stage tube because its payload must remain unmodified. Bolley
already permits a passive spacecraft interface. I can therefore ask the opposite question: can the
spacecraft's aft interface itself be the piston, using nearly the full 100 x 100 mm face?

That larger area makes the required pressure tens of kilopascals rather than tens of bar. It also
creates a different hard problem: a roughly 400 mm perimeter seal or controlled leakage path around
a flight CubeSat. I gain pressure margin and inherit sealing, contamination and exit-plume risk.
That is a real premise change, not a free improvement.

I keep a short electromagnetic section only if it earns at least one of four jobs:

1. I trim pressure and friction dispersion without asking the gas system for precision.
2. I distribute force around a declared centre of gravity.
3. I create differential/null-flux restoring force before wall contact.
4. I shape the final force decay so the exit does not manufacture tip-off.

If measured sealing makes the gas shot precise enough, I delete the trim section. If the seal or
rear-face load fails, Gen6 stops even if its ideal energy arithmetic is beautiful.

## Mission-level off-ramp

I also retain **burn-and-drop** outside the deployer generations. A cooperative upper stage can
release one payload, continue a low-thrust manoeuvre, and let the remaining stack inherit the later
velocity. That can create relative velocity without a high-energy ejector. It is a mission design,
not a Bolley mechanism: it spends stage delta-v, time, operations authority and a propulsion duty
the rideshare host may refuse. I compare it because the cleanest solution to a mechanism can be to
remove the mechanism's requirement.

## Sources that changed my questions

- I use [NASA's current SmallSat deployment survey](https://www.nasa.gov/smallsat-institute/sst-soa/integration-launch-and-deployment/)
  to keep provider choice, tip-off, initiators, inhibits and maturity inside the problem.
- I use [NASA's multifunctional thermal-structure survey](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/)
  and the [ESA composite enclosure work](https://www.esa.int/TEC/Structures/SEMSMFWUP4F_0.html)
  to justify testing a multifunctional interface, not to claim a mass saving.
- I use the [NASA labyrinth-seal review](https://ntrs.nasa.gov/api/citations/19700016838/downloads/19700016838.pdf)
  to treat non-contact sealing as controlled leakage rather than zero leakage.
- I use [NAVAIR's EMALS description](https://www.navair.navy.mil/product/Electromagnetic-Aircraft-Launch-System-EMALS)
  as a cross-domain example of bulk energy storage plus accurately controlled linear force. I do not
  import its scale, reliability or performance into Bolley.
- I use [Inductrack's passive ladder/Halbach logic](https://en.wikipedia.org/wiki/Inductrack) and
  null-flux electrodynamic suspension only as topology prompts. Permanent magnets remain forbidden
  by BOL-R-007 unless I explicitly reopen that requirement.
