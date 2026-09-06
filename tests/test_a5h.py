"""I inject violated A5h geometry bands so the evaluator must fail."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import gen3_12turn_detailed_fit as gate
class FrozenBandTests(unittest.TestCase):
    def test_each_violation_changes_the_verdict(self):
        original=gate.ROOT
        mutations={'turn_solid_count_per_cell':11,'coil_core_intersection_mm3':1e-3,
                   'coil_to_fluxrelay_radial_clearance_mm':0.49,'mean_turn_length_relative_error':0.006}
        try:
            for field,value in mutations.items():
                with self.subTest(field=field),tempfile.TemporaryDirectory() as directory:
                    root=Path(directory);(root/'cad').mkdir()
                    data=json.loads((ROOT/'cad/BUILD_GEN3_12TURN.json').read_text())
                    data['fit_checks'][field]=value
                    (root/'cad/BUILD_GEN3_12TURN.json').write_text(json.dumps(data))
                    (root/'cad/gen3_12turn_detailed_parameters.json').write_bytes((ROOT/'cad/gen3_12turn_detailed_parameters.json').read_bytes())
                    gate.ROOT=root
                    self.assertFalse(gate.calculate()['screen_pass'])
        finally: gate.ROOT=original
if __name__=='__main__':unittest.main()
