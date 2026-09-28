# A6j-R2: raise both windings with the yoke

Adityavardhan Mishra · 17 September 2026

I retain A6j-R1: all seven yoke-only cases fail because the lower winding retains
0.30 mm clearance to the separator tips. Raising the yoke cannot fix that gap.
The complete rejected screen is in validation/results/A6j_R1_yoke_only_rejected.json.

Before executing the revised geometry, add exactly 0.25 mm to both coil start
heights. Preserve the wire cross section, turn count, mean path, interlayer gap,
haunch radius, yoke thickness and all original physical acceptance bands.
Repeat the same seven yoke rises and all A6j geometric/solid-volume checks.
The 0.5 mm coupon layout clearance remains unchanged. This translation has no
mass change in the modeled conductor slices but changes the field, so no old
magnetic result can be inherited. Use A6j-R2 as the named common geometry candidate.
