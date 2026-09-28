# A6j: common core/winding geometry

Adityavardhan Mishra · 17 September 2026

I freeze a geometry-only redesign screen. The surviving A5h CAD and A6h field
use different inner-corner geometry. Preserve the field model's 4 mm haunch;
do not delete it or inherit the old field verdict for a changed design.
Use the actual selected twelve-turn maximum-insulation rectangular envelopes,
both coil heights, and test raising the back-yoke underside by 0/0.5/1/1.5/2/3/4 mm.
Extend the two outer legs by the same amount; keep yoke thickness, separators,
payload gap, conductor section, turns and winding path unchanged.

Require no coil/core intersection and >=0.5 mm geometric coil/core clearance,
an explicitly assumed new layout margin, not a manufacturing allocation.
Choose the smallest sampled rise satisfying both coil heights. Retain failures.
Independently compute minimum distances to core rectangles and circular haunches;
compare the selected geometry's CadQuery solids, intersection and minimum distance
with the analytical result to 1e-5 mm. Core volume increase must match the two-leg
analytical increment within 1e-5 relative. Store a common resolved parameter file
for CAD and future field input, plus source hashes. Generate the selected core and
winding envelope coupon only. No new magnetic performance, thermal qualification,
full-face CAD regeneration or powered-coupon acceptance follows from this run.
