"""Geometry checks at feature boundaries and the retained rejected layout."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import core_winding_reconciliation as g
import reconciled_wire_field as f

class GeometryTests(unittest.TestCase):
    def test_haunch_boundary_and_mirror(self):
        h=(0,0,4,1)
        self.assertEqual(g.haunch_distance([0,.1,3,3.1],h),0)
        self.assertGreater(g.haunch_distance([3,3.1,0,.1],h),0)
        self.assertAlmostEqual(g.haunch_distance([3,3.1,0,.1],h),g.haunch_distance([-3.1,-3,0,.1],(0,0,4,-1)),places=10)
    def test_lower_clearance_translation(self):
        d=g.inputs(2)
        self.assertAlmostEqual(g.distances(d)[0],.55,places=8)
        for wires in d['wires_mm']:
            for w in wires:w[2]-=.25;w[3]-=.25
        self.assertAlmostEqual(g.distances(d)[0],.30,places=8)
    def test_original_haunch_conflict_not_erased(self):
        self.assertLess(min(g.distances(g.inputs(0))),.5)
        self.assertGreaterEqual(min(g.distances(g.inputs(2))),.5)
    def test_wire_current_integral(self):
        for index in (0,1):
            p=f.parameters(index);totals={-1:0.,1:0.}
            for w in p['wire_rectangles']:
                totals[w['sign']]+=(w['y'][1]-w['y'][0])*(w['z'][1]-w['z'][0])*p['excitation']['source_current_density_rms_a_m2']
            for v in totals.values():self.assertAlmostEqual(v,1520,places=7)

if __name__=='__main__':unittest.main()
