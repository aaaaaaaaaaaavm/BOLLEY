# A3d — revised 0.60 T Fluxfoil operating point

**State at declaration:** NOT RUN  
**Evidence class:** revised analytical MODEL OUTPUT after a frozen-band failure  
**Purpose:** test the smallest launcher-side operating-point change that gives the A3c payload
geometry a credible secondary-loss margin.

## Trigger

A3c passed 17 of 18 bands at 0.50 T RMS. The failure was worst-corner secondary-only shot
efficiency: 66.2% against a predeclared minimum of 70%. The band is not changed and the A3c result
is not overwritten.

## Change under test

- External travelling field: 0.50 T RMS -> **0.60 T RMS**.
- Payload fins, mass, clearance, face footprint and 48 mm wavelength: unchanged.
- Force gate, pulse, CG grid and all A3c bands: unchanged.
- Additional A3d band: imposed field shall not exceed 0.60 T RMS.

The higher field lowers required slip and therefore secondary loss. It increases symmetric normal
preload and launcher magnetizing effort; both remain visible in the output and the latter is not
claimed solved.

Inputs are frozen in `cad/fluxfoil_a3d_parameters.json`.

## Bands declared before execution

A3d inherits all 18 A3c executable bands without modification and adds:

| ID | Band | Failure action |
|---|---|---|
| A3d-1 | External travelling field is <=0.60 T RMS. | Do not continue raising field; redesign area/wavelength or reject Fluxfoil. |

## Required output

The result must reproduce all A3c quantities and bands, add the field-ceiling band, and directly
show the change in slip, current density, heat, frequency, efficiency, power and normal force from
the failed 0.50 T point.
