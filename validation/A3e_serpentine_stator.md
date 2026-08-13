# A3e — explicit serpentine stator and pulse circuit

**State at declaration:** NOT RUN  
**Evidence class:** lumped MAGNETIC/CIRCUIT MODEL from ASSUMPTION Gen1 geometry/loss inputs  
**Purpose:** put real iron, copper, voltage, loss and mass behind A3d's 0.60 T field assumption.

## Topology under test

At every axial phase cell, one transverse flux loop crosses all four Fluxfoil slots in series,
then turns through two widened outer return legs and a back yoke. The three interior separators
carry the same flux straight across the face. This avoids A3b1's error of forcing two fin fluxes to
turn through each 2 mm interior web.

- Four independent face channels.
- Three axial phases, offset by one 16 mm cell over a 48 mm electrical wavelength.
- Nineteen cells in series per phase; 57 cells per channel; 0.912 m active length.
- Four 2.0 mm low-permeability slots in series: 8.0 mm total magnetic gap including foil.
- 20 mm face footprint, 3 mm outer legs and 3 mm back yoke.
- 0.60 T RMS slot field; 1.20 T RMS outer-leg/yoke field.
- 20 turns per cell, 45 mm mean turn length and 20 mm² copper.
- Nominal 120 V DC link with space-vector modulation.

Dimensions and assumptions are frozen in `cad/serpentine_stator_parameters.json`.

## Model

The slot MMF is $B\ell/\mu_0$. The core contribution uses a deliberately conservative 2500 A/m
at the rated outer-yoke field over a 50 mm equivalent path. Phase linkage sums nineteen identical
cell linkages; winding resistance follows copper length and area.

At each of 441 CG points, each channel receives the existing positive force allocation. Field
command scales with square root of force and caps at 0.60 T. The A3d thin-sheet solution supplies
slip and secondary loss. A 1001-step shot integration adds:

- payload mechanical power;
- foil secondary loss;
- three-phase copper loss;
- assumed core loss, 80 W/kg at rated field and 300 Hz with $B^2 f^{1.5}$ scaling; and
- 97% inverter efficiency.

Phase voltage includes winding resistance, air-gap/core real load and $2\pi fL$. The minimum DC
link follows the declared modulation utilisation. Current is prebiased before gate release.

## Bands declared before execution

| ID | Band | Failure action |
|---|---|---|
| A3e-1 | Serpentine face footprint is <=21 mm. | Reject the cross-section. |
| A3e-2 | Rated outer-leg/yoke field is <=1.20 T RMS. | Increase iron or reject. |
| A3e-3 | Rated MMF is <=4000 A-turn. | Redesign gap/path. |
| A3e-4 | Rated phase current is <=250 A RMS and copper current density <=12 A/mm². | Add turns/copper or reject. |
| A3e-5 | Active copper + electrical-steel mass is <=45 kg. | Redesign winding/core before packaging. |
| A3e-6 | Maximum phase RMS voltage is <=70 V. | Increase turns/link or reject the 120 V architecture. |
| A3e-7 | Required DC link is <=200 V preferred and <=400 V absolute. | Above preferred: redesign; above absolute: kill. |
| A3e-8 | Worst-CG 4 kg source energy is <=900 J. | Reject against BOL-R-009. |
| A3e-9 | Worst-CG peak DC power is <=15 kW for both reference and qualification shots. | Reject against BOL-R-010 or reduce duty. |
| A3e-10 | Stator-copper adiabatic rise is <=1 K per shot. | Add copper/cooling or reduce repetition. |
| A3e-11 | Maximum model frequency is <=350 Hz. | Change wavelength or inverter. |
| A3e-12 | Nominal 120 V link has >=10% margin over the model requirement. | Raise link or redesign winding. |

Paired current, voltage and power limits are stored separately, producing 15 executable bands.

## Explicit non-bands

- This is a one-dimensional magnetic circuit, not 2D/3D FEA.
- Slot leakage, axial end effects, finite foil height, mutual phase coupling, harmonics and force
  ripple are absent.
- Core H and loss are conservative assumptions, not a selected steel B-H/loss table.
- Housing, clamps, insulation, coolant, sensors, inverter, DC link, cables and gate are excluded
  from the active electromagnetic mass.
- Prebias is assumed; cold current-rise and fault interruption are not modelled.
- Provider fit, common-mode normal preload, structure, wear and force remain hardware gates.

## Required output

The result must report magnetic circuit, winding R/L/current/voltage, active mass, all 441 points
for both shots, full energy partitions, efficiency, peak power/frequency, copper rise, every band
and a disposition.
