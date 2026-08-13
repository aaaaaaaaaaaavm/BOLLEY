# Run status

| Run | State | Result |
|---|---|---|
| A1 | MODELLED | 8/8 declared bands pass. Required worst-corner shear is 25.04 kPa; screened interface mass is 0.229 kg. |
| A2 | MODELLED | 5/5 declared bands pass over 441 CG points. Peak channel force is 252.43 N. |
| A3a | MODELLED | 6/7 declared bands pass. The corner L-return fails its preferred-mass lower bound; fin and induction candidates survive mass/area only. |
| A3 | NOT RUN | — |
| A4 | NOT RUN | — |
| A5a | MODELLED | 11/11 executable bands pass. Comb-fin mass is 121.2 g; peak channel load is 229.07 N and developed shear is 22.73 kPa. |
| A3b0 | MODELLED | 0/3 bands pass. The three-fin comb makes only 250.67 N at an optimistic 2.0 T and is rejected before FEA. |
| A5b | MODELLED | 15/15 bands pass. Quad-comb mass is 158.9 g; ideal field requirement is 1.595 T with 13.6% ideal margin at 1.7 T. |
| A3b1 | MODELLED | 0/7 bands pass. Required outer/interior throat fields are 4.78/9.57 T; the shared-pole stator is rejected. |
| A3c | MODELLED | 17/18 bands pass. The 0.50 T point fails worst-CG secondary-only efficiency at 66.2% versus 70%. |
| A3d | MODELLED | 19/19 bands pass. At 0.60 T, worst-CG secondary-only efficiency is 73.9%, peak air-gap power 6.84 kW and rated local rise 4.85 K. |
| A3e | MODELLED | 15/15 bands pass over 882 shots. Active electromagnetic mass is 40.96 kg; reference draw 821 J; qualification peak 11.08 kW. |
| A5 | NOT RUN | — |
| A5c | NOT RUN | Gen1 CAD objects, fit, exports, renders and manifest bands declared. |

This file is updated only after the corresponding committed run sheet exists.

`MODELLED` does not close A1 or A2 as hardware evidence. It records that their declared
first-order questions have answers and leaves the physical claims to A3–A5. A3a rejects one
geometry; it does not validate either surviving candidate.
Likewise, A5a is a preliminary envelope screen, not dispenser acceptance or structural evidence.
