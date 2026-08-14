# What would make me stop Bolley

I treat open problems as work. I treat the failures below as reasons to stop or change the
architecture rather than explain them away.

## 1. Rail force density

**Threshold:** a representative covered-gap corner channel must produce at least 255 N for
150 ms without exceeding its material, current or temperature limits.

I require the first-order area screen to remain at or below 26 kPa air-gap shear in the 6 kg,
worst-CG case. I deliberately set that below the approximately 35 kPa external benchmark; I reserve
the difference as provisional margin for cover, fringing, manufacturing and control.

**Status:** OPEN. I have no electromagnetic model or hardware result for this criterion.

## 2. High-speed commutation

**Preferred band:** no more than 200 V DC link at the reference duty.

**Kill threshold:** more than 400 V required to establish and extinguish channel current at the
maximum commanded speed, or no positive force margin after voltage saturation.

**Status:** OPEN. I do not treat pole-passage frequency alone as an answer.

## 3. Cooperative-interface mass

**Target:** no more than 0.25 kg incremental payload mass.

**Kill threshold:** more than 0.40 kg after structural retention and shielding are included.

Above the threshold, I consider the interface to be surrendering too much of its advantage over compact
propulsion and the unmodified-payload fallback.

**Status:** OPEN. I have only a Phase 0 material-volume screen.

## 4. Electrical shot energy

**Kill threshold:** more than 900 J gross stored-energy draw for the 4 kg reference shot.

I use this threshold to prevent a lower-force topology from quietly retaining VOLLEY's
multi-string bank problem through poor efficiency.

**Status:** OPEN. My first-order result uses an assumed 40–60% total efficiency.

## 5. Tip-off

**Kill threshold:** more than 2 deg/s per axis at free flight.

I treat force-centroid control only as a proposed remedy. I require exit fringing, channel
calibration, guide clearance and CG error to fit inside the same number.

**Status:** OPEN.

## 6. Magnetic compatibility

**Static threshold:** more than 50 microtesla above ambient outside the unpowered payload envelope.

**Transient threshold:** supplied by the manifested spacecraft; I do not invent a universal
induced-voltage number here.

**Status:** OPEN.

## 7. Interface acceptance

**Kill threshold:** no plausible path to a launch-provider-approved aluminium contact surface and
mechanically retained internal magnetic circuit.

I do not call a machine successful if it works only by violating its payload interface.

**Status:** OPEN.

## 8. Commercial reason to exist

**Kill threshold:** quoted recurring hardware plus integration is not lower than the customer's
credible alternative for same-plane phasing.

I will not close this item with an assumed rupee or dollar comparison.

**Status:** NOT EVALUABLE until I have quotations and a customer case.
