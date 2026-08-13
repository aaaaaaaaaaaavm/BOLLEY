# Run status

| Run | State | Result |
|---|---|---|
| A1 | MODELLED | 8/8 declared bands pass. Required worst-corner shear is 25.04 kPa; screened interface mass is 0.229 kg. |
| A2 | MODELLED | 5/5 declared bands pass over 441 CG points. Peak channel force is 252.43 N. |
| A3a | MODELLED | 6/7 declared bands pass. The corner L-return fails its preferred-mass lower bound; fin and induction candidates survive mass/area only. |
| A3 | NOT RUN | — |
| A4 | NOT RUN | — |
| A5a | MODELLED | 11/11 executable bands pass. Comb-fin mass is 121.2 g; peak channel load is 229.07 N and developed shear is 22.73 kPa. |
| A3b0 | NOT RUN | Ideal tooth-edge upper bound declared for the exact three-fin comb. |
| A5 | NOT RUN | — |

This file is updated only after the corresponding committed run sheet exists.

`MODELLED` does not close A1 or A2 as hardware evidence. It records that their declared
first-order questions have answers and leaves the physical claims to A3–A5. A3a rejects one
geometry; it does not validate either surviving candidate.
Likewise, A5a is a preliminary envelope screen, not dispenser acceptance or structural evidence.
