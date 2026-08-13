# A3c — Fluxfoil travelling-field induction screen

**State at declaration:** NOT RUN  
**Evidence class:** analytical THIN-SHEET MODEL OUTPUT from ASSUMPTION geometry/material inputs  
**Purpose:** decide whether a passive aluminium reaction interface deserves an explicit stator,
circuit and field model after the shared-pole reluctance branch failed.

## Geometry under test

Each broad spacecraft face carries four continuous aluminium fins:

- 6.0 mm active height and 6.25 mm total nominal projection;
- 1.0 mm conductor thickness with 0.50 mm clearance on both sides;
- four 2.0 mm stationary slots and five 2.0 mm separators: 18.0 mm face footprint;
- 336 mm active length; and
- a 50 g shared root/capture/fastener allowance.

The ordinary corner contact rails remain continuous hard-anodized aluminium. The fins are passive,
unpowered and hard-anodized externally. The oxide does not interrupt eddy-current loops inside
each continuous conductor.

## Electromagnetic model

Two launcher stators apply a symmetric transverse travelling field to both sides of each fin. In
the conductor frame, the field travels at slip speed $u=v_s-v$. For sheet conductance $G=\sigma t$
and imposed RMS field $B_0$, the infinite thin-sheet reaction model is

$$q=\frac{G u B_0^2}{1+(\mu_0 G u/2)^2},$$

where $q$ is axial force per active sheet area. The low-slip root is used. The dimensionless sheet
reaction number is $\beta=\mu_0Gu/2$, the field at the sheet is
$B=B_0/\sqrt{1+\beta^2}$, and secondary loss is $P_2=Fu$.

The frozen field input is 0.50 T RMS and the electrical wavelength is 48 mm. Aluminium screening
values are 2.82e-8 ohm m resistivity, 2700 kg/m³ density and 900 J/(kg K) specific heat. No alloy
or supplier lot has been selected.

## Bands declared before execution

| ID | Band | Failure action |
|---|---|---|
| A3c-1 | Projection is <=6.5 mm with >=0.20 mm nominal reserve. | Reject or shorten the fin. |
| A3c-2 | Rail-edge keep-out passes and the 18 mm array uses <=25% of usable face width. | Reject the layout. |
| A3c-3 | Interface increment is <=0.25 kg preferred and <=0.40 kg absolute. | Above preferred: reserve; above absolute: reject. |
| A3c-4 | Nominal side clearance is >=0.50 mm. | Increase slot or reject tolerance stack. |
| A3c-5 | Rated force density is <=25% of the thin-sheet maximum at 0.50 T. | Increase active area/field or reject the low-slip model. |
| A3c-6 | The 255 N low-slip solution requires <=4.0 m/s slip and sheet reaction number <=0.10. | Redesign field, conductor or area. |
| A3c-7 | Rated RMS current density is <=70 MA/m². | Increase conductor volume or reject. |
| A3c-8 | Rated-channel 150 ms adiabatic rise is <=10 K. | Add thermal mass or reduce force/duty. |
| A3c-9 | Slip-frequency skin depth is >=5 conductor thicknesses. | Replace the thin-sheet approximation. |
| A3c-10 | Rated field chirp is <=100 Hz at start and <=350 Hz at qualification exit. | Change wavelength or reject switching assumption. |
| A3c-11 | One-percent total side-to-side field-amplitude mismatch leaves <=100 N normal force. | Add balance control or reject. |
| A3c-12 | Worst-CG secondary-only shot efficiency is >=70%. | Reject on rotor loss. |
| A3c-13 | Worst-CG peak air-gap power is <=10 kW. | Reject before primary-loss design against the 15 kW requirement. |

Preferred/absolute mass and each paired limit are stored as separate Booleans, producing 18
executable bands.

## Explicit non-bands

- The 0.50 T travelling field is an input. No core, winding, air-gap MMF, voltage or DC link has
  produced it.
- The infinite thin sheet omits axial end effects, finite fin height, slot harmonics and thermal
  conduction.
- Primary copper, core, switching, cable and capacitor losses are absent.
- Normal-force cancellation covers only the declared field mismatch, not mechanical gap runout or
  a failed stator side.
- Provider acceptance, root strength, vibration, debris, wear and repeated-shot temperature are
  open.

## Required output

The result must include interface dimensions/mass, the rated low-slip root, sheet field/reaction,
current density, skin depth, local heating, frequency range, normal forces, every frozen CG point,
worst shot heat/efficiency/power, all band outcomes and a disposition.
