# Run status

| Run | State | Result |
|---|---|---|
| A1 | MODELLED | 8/8 declared bands pass. Required worst-corner shear is 25.04 kPa; screened interface mass is 0.229 kg. |
| A2 | MODELLED | 5/5 declared bands pass over 441 CG points. Peak channel force is 252.43 N. |
| A3a | MODELLED | 6/7 declared bands pass. The corner L-return fails its preferred-mass lower bound; fin and induction candidates survive mass/area only. |
| A4 | NOT RUN | — |
| A5a | MODELLED | 11/11 executable bands pass. Comb-fin mass is 121.2 g; peak channel load is 229.07 N and developed shear is 22.73 kPa. |
| A3b0 | MODELLED | 0/3 bands pass. The three-fin comb makes only 250.67 N at an optimistic 2.0 T and is rejected before FEA. |
| A5b | MODELLED | 15/15 bands pass. Quad-comb mass is 158.9 g; ideal field requirement is 1.595 T with 13.6% ideal margin at 1.7 T. |
| A3b1 | MODELLED | 0/7 bands pass. Required outer/interior throat fields are 4.78/9.57 T; the shared-pole stator is rejected. |
| A3c | MODELLED | 17/18 bands pass. The 0.50 T point fails worst-CG secondary-only efficiency at 66.2% versus 70%. |
| A3d | MODELLED | 19/19 bands pass. At 0.60 T, worst-CG secondary-only efficiency is 73.9%, peak air-gap power 6.84 kW and rated local rise 4.85 K. |
| A3e | MODELLED | 15/15 bands pass over 882 shots. Active electromagnetic mass is 40.96 kg; reference draw 821 J; qualification peak 11.08 kW. |
| A5c | MODELLED | 9/10 bands pass. Gen1 exact CAD finds 3,987.4 mm3 winding/interface overlap per face and rejects the package. |
| A3f | MODELLED | 23/23 bands pass. Fluxbridge replaces Gen1 with a passive magnetic/copper cage; hardware and field evidence remain open. |
| A3g | MODELLED | Ten robust analytical candidates survive; `p30_B0.56` is frozen for Gen2. |
| A5d | MODELLED | 13/13 CAD bands pass. Seven STEP and seven STL masters close nominal Gen2 fit only. |
| A6 | MODELLED | 10/13 field bands pass. Mean field, stationary-core peak and inductance reject the A3g operating point. |
| A6b | MODELLED | 11/13 field bands pass. Gen2.1 narrowly misses ligament and return-haunch peaks. |
| A6c | MODELLED | 12/13 field bands pass. Gen2.2 misses only the moving ligament at 1.5306 T. |
| A6d | MODELLED | 12/13 field bands pass. Gen2.3's 1.06 mm rib still misses moving material by 1.83%. |
| A6e | MODELLED | 12/13 field bands pass. Gen2.4 reaches 1.5159 T at the local ligament estimate. |
| A6f | MODELLED | 13/13 field bands pass. Gen2.5 Fluxweb opens post-field cage/circuit closure. |
| A7a | MODELLED | 0/4 robustness corners pass all 19 bands. Four-lane Fluxweb fails cage heat, current density, reference energy and secondary efficiency. |
| A6g | MODELLED | 13/13 field bands pass on 212,850 / 751,282 / 240,130 triangles. Gen2.6 Quintweb advances. |
| A7b | MODELLED | 2/4 robustness corners pass all 19 bands. Quintweb closes every translator failure; both 125% resistance corners fail only reference energy. |
| A8a | MODELLED | 5/10 bands pass over 9,001 travel points. The 900 mm axial package and simple full-overlap extension are rejected; sectional excitation survives. |
| A8b | MODELLED | 77/2,856 candidates pass every declared band. `n27_p45.3_I380_A10.4` is selected for fresh field and circuit reclosure. |

I update this file only after the corresponding committed run sheet exists.

I never use `MODELLED` to mean measured. In A8b I closed the coupled axial/sectional analytical
question for one Gen2.7 point. Its field is still my A6g current-scaled surrogate, so I require A6h
and A7c to pass before the new package can supersede the rejected Gen2.6 geometry.
