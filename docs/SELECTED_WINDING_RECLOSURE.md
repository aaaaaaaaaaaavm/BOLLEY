# Selected twelve-turn drive: what the remaining margin buys

I rerun the existing time-domain handoff envelope at A9f's twelve-turn partition and reconcile it with the A5h nominal winding. This is ideal-current tracking and fixed-MMF scaling. I have not solved the individual conductors' nonlinear field or selected a qualified pulse-power chain.

Verification: **PASS**. Rated phase current: **126.666667 A**. The generic-inverter A9 envelope's physical bands pass at both resolutions: **True**. The local-bridge energy accounting is reported separately below.

The conservative link envelope is **42.447968 V healthy** and **45.022869 V with failed-cell compensation**. A9f's 10% healthy margin: **PASS**. R and L rise by nine, current falls by three and the calculated voltage rises by three; ideal winding and magnetic energy are unchanged.

At the A9f 25 C conduction point, only **10.280918 J** remains below the 900 J reference cap. With no other added loss, the allowed conduction-resistance multiplier is **1.543875**. Neither value is a thermal rating.

| Assumed conduction multiplier | Added loss (J) | Reference source (J) | Margin (J) | Reference cap | Qualification source (J) |
|---:|---:|---:|---:|---|---:|
| 1.00 | 0 | 889.719082 | 10.280918 | PASS | 1296.786077 |
| 1.00 | 5 | 894.719082 | 5.280918 | PASS | 1301.786077 |
| 1.00 | 10 | 899.719082 | 0.280918 | PASS | 1306.786077 |
| 1.00 | 20 | 909.719082 | -9.719082 | FAIL | 1316.786077 |
| 1.25 | 0 | 894.444855 | 5.555145 | PASS | 1303.674001 |
| 1.25 | 5 | 899.444855 | 0.555145 | PASS | 1308.674001 |
| 1.25 | 10 | 904.444855 | -4.444855 | FAIL | 1313.674001 |
| 1.25 | 20 | 914.444855 | -14.444855 | FAIL | 1323.674001 |
| 1.50 | 0 | 899.170629 | 0.829371 | PASS | 1310.561925 |
| 1.50 | 5 | 904.170629 | -4.170629 | FAIL | 1315.561925 |
| 1.50 | 10 | 909.170629 | -9.170629 | FAIL | 1320.561925 |
| 1.50 | 20 | 919.170629 | -19.170629 | FAIL | 1330.561925 |
| 2.00 | 0 | 908.622176 | -8.622176 | FAIL | 1324.337773 |
| 2.00 | 5 | 913.622176 | -13.622176 | FAIL | 1329.337773 |
| 2.00 | 10 | 918.622176 | -18.622176 | FAIL | 1334.337773 |
| 2.00 | 20 | 928.622176 | -28.622176 | FAIL | 1344.337773 |

Only 6/16 assumed loss corners meet the reference cap. I retain failures rather than move the cap. The 108 modules alone weigh 2.5488 kg, before busbar, capacitors, gate drive, cooling, wiring or structure.

## Precise next work

The 160 A supplier characterization point used by A9f is not a permissible pulse-current rating. Resolve RMS/peak waveform and internal parallel-path definitions from the supplier documentation, then include temperature-dependent resistance, switching energy, dead time, commutation parasitics, protection, DC-link sag and cooling in one circuit/configuration. Re-solve the A5h conductor distribution and lead/terminal geometry before inheriting the earlier field map. Supplier curves and a current/voltage/temperature waveform experiment must bound the omitted-loss budget.

P11, P39 and P40 remain OPEN. P38 keeps its prior limited MODELLED disposition. A5f's copper-volume failure and A9e's selector rejection are unchanged. A5h remains nominal CAD, not manufacturing evidence.

[Criteria](../validation/A9g_selected_winding_reclosure.md) · [Full result](../analysis/results/selected_winding_reclosure.json) · [Current review](CURRENT_REVIEW.md)

Reproduce: `python analysis/selected_winding_reclosure.py --check`.
