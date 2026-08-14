# A7a — Gen2.5 post-field cage/circuit reclosure

**What I knew at declaration:** NOT RUN  
**Evidence class:** post-field homogenized cage + lumped circuit/CG shot model  
**Purpose:** I wanted to decide whether the A6f field point and Fluxweb's 8% copper-conductance trade still
meet the energy, slip, thermal, voltage and current gates that selected Gen2.

## The model I froze

- A6f's minimum three-mesh mean tooth field controls force; its largest three-mesh inductance
  controls voltage.
- Four face channels, four blades per channel, 5.50 mm active height and 336 mm active length.
- 30 mm cell pitch, 90 mm electrical wavelength, 30 cells per channel and ten cells per phase.
- Three 27 mm2 turns, 400 A RMS and 1,200 A-turn at full field.
- 0.345 mm equivalent copper sheet, 0.11356 kg cage copper and 0.14703 kg magnetic matrix.
- 4 kg reference and 6 kg qualification payloads include the 0.31059 kg interface.
- Every 21 by 21 CG point is evaluated for both payloads.
- Four robustness corners combine 90/100% nominal cage conductance with 100/125% phase
  resistance. The field already uses the lowest formal A6f mesh result.

I treat this as a quasi-steady reclosure of the existing analytical cage law. It is deliberately cheaper
than the transient solve it gates.

## Bands I declared before execution

Each robustness corner must pass all 19 hard bands:

- A6f remains 13/13 and interface mass remains <=0.40 kg;
- active primary mass <=16.0 kg;
- phase current <=400 A, current density <=40 A/mm2 and gross slot fill <=60%;
- required DC link <=48 V with >=10% margin on the 48 V link;
- reference source energy <=900 J and qualification source energy <=1,500 J;
- source-to-payload efficiency >=30% and secondary-only efficiency >=50%;
- peak DC power <=15 kW;
- primary/cage copper rise <=3/20 K per shot;
- cage current density <=180 A/mm2 and slip <=8 m/s;
- terminal frequency <=350 Hz; and
- 1% opposed-field mismatch leaves <=100 N net normal force.

The 0.25 kg programme target and 0.30 kg interface preference are recorded separately and already
fail. They are not silently removed, but neither replaces the 0.40 kg hard requirement.

## What I explicitly did not claim

- The cage is still a homogenized sheet, not discrete electromagnetic FEA.
- Prebias is assumed; inverter switching and cold current establishment are absent.
- End-bus resistance, bar-edge current crowding, finite-length fringing and force ripple are absent.
- Material loss and hot-resistance corners are model assumptions, not coupon measurements.
- Passing cannot close P29 or support a hardware claim.

## Output I required

I required the repository to retain all four corners, both payload cases, all 441 CG points per case, every band and the
preference failures. A pass opens discrete CAD and transient force modelling; a failure changes
the cage or field point without moving these bands.

## What I recorded

**I completed the run on 2026-08-13. I recorded: no corner passes all 19 bands; Gen2.5 is rejected at A7a.**

Across 3,528 retained CG/corner/payload records, the failed-band union is cage copper rise, cage
current density, reference source energy and secondary-only efficiency. Worst values are 22.74 K,
183.30 A/mm2, 905.1 J and 45.66%. Slip remains 7.073 m/s, required DC link 15.37 V and peak power
11.84 kW, so the correction belongs on the passive translator rather than in more current or bus
voltage. The [controlled result](../docs/GEN25_CAGE_CIRCUIT.md) blocks exact Gen2.5 CAD promotion.
