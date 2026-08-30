# How I search the part of the problem I do not know exists

The useful part of the four-quadrant knowledge picture is not the labels. It is the instruction to
change where I look. If I search only for “better CubeSat linear induction motors”, I can find only
better versions of the architecture I already know.

I now force every generation review across six boundaries:

| Boundary I move | Question I ask | What it exposed here |
|---|---|---|
| Energy | Must shot energy arrive electrically during the shot? | VOLLEY A35 showed the pulse costs more than the mover; Gen6 moves bulk energy to gas |
| Force path | Must a launcher mover push the spacecraft? | Bolley made the spacecraft passive translator; Fluxpiston makes its aft interface the pressure piston |
| Function | Must interface mass perform only deployment work? | Fluxframe tries to make the same material carry structure, heat, ground and guidance duties |
| Time | Must relative velocity be created inside a 0.9 m shot? | Burn-and-drop creates it over a stage manoeuvre after one payload is released |
| Host | Must the dispenser be independent of the upper stage? | A stage tube, stage thrust arc or shared sequencer can erase dispenser subsystems while adding integration cost |
| Verification | Is a passing local model the decision? | Leakage, provider acceptance, tip-off and packaged mass can kill a locally passing electromagnetic design |

## Ideas I keep, reject or quarantine

| Idea | Why I considered it | Current disposition |
|---|---|---|
| Null-flux differential trim | Passive electrodynamic systems can turn lateral offset into restoring force | Keep for Gen6 centring; it needs a topology that does not add spacecraft magnets |
| Shunted permanent-magnet mover | A synchronous secondary could cut slip loss and pulse energy | Quarantine; it violates BOL-R-007 and creates magnetic-cleanliness work |
| Thomson-coil repulsion | No long moving launcher member is required | Reject for the flagship; it intensifies the exact pulse/EMI problem P41 says to delete |
| Digitally selected spring banks | Mechanical energy can wait without a pulse inverter | Keep as a control; a pusher, latch, variable stroke and reset mechanism can recreate the machinery Bolley removed |
| Strain-energy spacecraft rails | The cooperative interface could store its own launch energy | Screen only; required specific energy and launch-safety implications are severe |
| Centrifugal carousel | Mechanical bulk energy plus electromagnetic trim works in other launch problems | Mission-specific off-ramp; host momentum, packaging and a rotating mechanism dominate |
| Burn-and-drop | The upper stage can create relative velocity by continuing to accelerate after release | Strong mission-level comparator, not a dispenser replacement for an unwilling host |
| Fluxframe | The cage may replace rather than add bus structure and thermal hardware | Gen5 target; no credit until a real bus parts ledger closes |
| Fluxpiston | A full-face passive pressure interface can delete the pulse chain | Gen6 target; seal leakage, rear-face structure and exit gas are the first kill gates |

## The rule I carry forward

I do not reward an idea for being unusual. I reward it when changing the boundary deletes a larger
requirement than it adds. Every wild branch therefore needs a one-sentence stop condition before I
let it become CAD.

I now put those branches in the shared
[VOLLEY-lab](https://github.com/aaaaaaaaaaaavm/VOLLEY-lab) rather than letting them become an
unannounced Bolley generation. [`LAB_TRANSFER.md`](LAB_TRANSFER.md) records the boundary. The first
cross-program gates are the quadrant leakage bearing and a deployer-owned passive trim secondary;
neither inherits a result merely because its principle came from a passing model here.
