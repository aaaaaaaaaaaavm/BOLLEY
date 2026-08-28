# My validation register

I start validation before I know the result.

My newest system-level branch is [A10](A10_architecture_screen.md): a frozen Gen4-Gen6 premise
screen. It does not replace the Gen3 field, circuit or CAD evidence and it does not promote Gen5 or
Gen6 to hardware baselines.

In each run sheet I state inputs, evidence class, numerical bands and the action following a
failure. I do not edit a committed run sheet to make a completed run pass. If I decide a band was
wrong, I supersede it with an ADR while preserving the original and stating that I already knew
the answer.

| Run | Question | Evidence | Current disposition |
|---|---|---|---|
| [A1](A1_first_order_sizing.md) | Is the cooperative architecture dimensionally worth pursuing? | First-order model | 12/12 pass; architecture screen retained |
| [A2](A2_force_allocation.md) | Can four positive rail forces place thrust through the allowed CG envelope? | Independent algebraic model | 10/10 pass; modelled only |
| [A3a](A3a_flux_path_screen.md) | Which explicit moving flux/conductor path deserves nonlinear analysis? | Analytical topology screen | Original corner return rejected |
| [A3](A3_corner_coupon.md) | Can one covered-gap rail channel make the force at speed? | FEA, then measurement | NOT RUN; obsolete topology |
| [A4](A4_magnetic_compatibility.md) | Is the passive interface magnetically tolerable? | Measurement | NOT RUN |
| [A5a](A5a_comb_fin_envelope.md) | Can a low-profile three-fin face channel fit preliminary CubeSat guidance and preserve control? | Analytical interface screen | Fit passes; force topology later rejected |
| [A3b0](A3b0_edge_force_bound.md) | Can that exact comb meet force even in an ideal tooth-edge energy bound? | Analytical upper bound | Rejected |
| [A5b](A5b_quad_comb_envelope.md) | Does a four-fin, 6 mm redesign recover ideal force margin without breaking the interface? | Analytical interface/force screen | Screen passes; shared-pole stator later rejected |
| [A3b1](A3b1_stator_throat_bound.md) | Can the quad-comb's shared stationary poles carry and return its required flux? | Analytical flux-conservation bound | Rejected |
| [A3c](A3c_fluxfoil_induction.md) | Can a passive four-fin aluminium sheet carry the pulse without excessive slip, heating or normal imbalance? | Analytical thin-sheet model | 0.50 T efficiency point rejected |
| [A3d](A3d_fluxfoil_operating_point.md) | Does a 0.60 T launcher-side field repair A3c's frozen efficiency miss without breaking another band? | Revised analytical operating point | 19/19 pass; superseded by explicit stator work |
| [A3e](A3e_serpentine_stator.md) | Can an explicit series-flux stator create A3d's field inside mass, voltage, energy and power limits? | Lumped magnetic/circuit model | 15/15 pass; winding later rejected |
| [A5](A5_interface_fit.md) | Can the rail remain a valid mechanical interface? | Drawing review and fit check | NOT RUN against provider-controlled drawing |
| [A5c](A5c_gen1_cad.md) | Does Gen1 exist as traceable, non-interfering STEP/STL geometry rather than a sketch? | Parametric CAD + manifest checks | 9/10 pass; Gen1 winding rejected |
| [A3f](A3f_fluxbridge_cage.md) | Can a passive magnetic-matrix/copper-ladder blade remove the Gen1 copper penalty? | Analytical cage/circuit model | 23/23 pass; promoted to optimisation |
| [A3g](A3g_fluxbridge_optimization.md) | Is there a robust winding-size/field/pitch point for Gen2 CAD? | Deterministic search with eight robustness corners | 10 robust candidates; selected point later rejected by A6 |
| [A5d](A5d_gen2_cad.md) | Does the selected Fluxbridge stator and cage fit in manufacturing-intent nominal CAD? | Parametric CAD + exact intersection checks | 13/13 pass; geometry retained |
| [A6](A6_gen2_field.md) | Does the actual nonlinear cross-section reproduce A3g field and inductance without core saturation? | Three-mesh 2D nonlinear magnetostatic FEA | 10/13 pass; operating point rejected |
| [A6b](A6b_gen21_fluxmanifold.md) | Does my first radius-fed return repair the A6 saturation failures? | Three-mesh 2D nonlinear magnetostatic FEA | 11/13 pass; exact geometry rejected |
| [A6c](A6c_gen22_fluxmanifold_r4.md) | Does lower MMF and a deeper return haunch close the remaining peaks? | Three-mesh 2D nonlinear magnetostatic FEA | 12/13 pass; moving ligament rejected |
| [A6d](A6d_gen23_fluxrib.md) | Does a locally thicker passive rib close the ligament peak? | Three-mesh 2D nonlinear magnetostatic FEA | 12/13 pass; exact rib rejected |
| [A6e](A6e_gen24_fluxrib.md) | Can I spend more passive mass and slightly less MMF to close that peak? | Three-mesh 2D nonlinear magnetostatic FEA | 12/13 pass; local peak rejected |
| [A6f](A6f_gen25_fluxweb.md) | Does a layered magnetic web beneath the copper rungs close the transverse field? | Three-mesh 2D nonlinear magnetostatic FEA | 13/13 pass; cage/circuit reclosure opened |
| [A7a](A7a_gen25_cage_circuit.md) | Does exact Gen2.5 still close energy, thermal, cage and CG bands? | Post-field cage/circuit model | 0/4 robustness corners pass all bands; point rejected |
| [A6g](A6g_gen26_quintweb.md) | Does a five-lane cage retain the transverse-field pass? | Three-mesh 2D nonlinear magnetostatic FEA | 13/13 pass; cage/circuit reclosure opened |
| [A7b](A7b_gen26_cage_circuit.md) | Does the fifth lane close A7a without moving my bands? | Post-field cage/circuit model | Translator failures close; hot reference energy remains high |
| [A8a](A8a_axial_engagement.md) | Does the exact Gen2.6 cage remain engaged through the claimed powered travel? | Finite-interval axial model | 900 mm package and simple extension rejected |
| [A8b](A8b_gen27_codesign.md) | Can I close engagement, installed mass and sectional energy together? | Coupled deterministic design-space search | 77 candidates pass; one Gen2.7 point selected |
| [A6h](A6h_gen27_fluxrelay.md) | Does the exact selected 380 A point survive a fresh nonlinear field solve? | Three-mesh 2D nonlinear magnetostatic FEA | 13/13 pass; A7c and A5e later passed |
| [A7c](A7c_gen27_cage_circuit.md) | Does the exact selected point still close every circuit and cage band from A6h? | Post-field homogenized cage + sectional circuit/CG model | Four corners pass 29/29; A5e passed and A9 remains open |
| [A5e](A5e_gen3_cad.md) | Does that exact selected point exist as traceable, non-interfering Gen3 nominal geometry? | Parametric CAD + exact solid intersections + deterministic archives | 17/17 pass; tolerance, structure and A9 opened |
| [A10](A10_architecture_screen.md) | Which changed premise deserves Gen5/Gen6 work after the pulse became the controlling term? | First-order architecture and requirement screen | 7 pass, 2 fail, 1 open, 2 report; requirement corrected and finite next gates opened |
| [A11](A11_fluxpiston_flow.md) | Can a deliberately leaking full-face pressure interface stay inside gas, store and feed screens? | Ideal gas + continuum choked clearance flow | 8/8 executable bands pass; contact, plume and seal evidence remain open |
| [A12](A12_fluxframe_mass.md) | Is Gen5's 121.36 g credit material relative to sourced public 3U chassis masses? | Sourced public mass-envelope arithmetic | 5/5 executable bands pass; 3 integration bands open and zero credit granted |

I do not use `MODELLED` as a synonym for `VALIDATED`. Only hardware evidence can close my central
claim.
