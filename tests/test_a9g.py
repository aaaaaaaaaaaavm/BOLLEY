"""Independent energy limits and turn scaling for the selected partition."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import selected_winding_reclosure as selected

class ReclosureTests(unittest.TestCase):
    def test_rli_identity_and_no_input_mutation(self):
        a=selected.a9
        p,b,c=a.load(a.INPUT),a.load(a.BASE_INPUT),a.load(a.A7C_RESULT)
        before=copy.deepcopy(c)
        sp,_,sc=selected.scaled_inputs(p,b,c,12)
        self.assertEqual(c,before)
        self.assertAlmostEqual(sp["fixed"]["rated_phase_current_a"]*12,1520)
        self.assertAlmostEqual(sc["corners"][0]["phase_resistance_ohm"]*(380/3)**2,c["corners"][0]["phase_resistance_ohm"]*380**2)
        self.assertAlmostEqual(sc["sectional"]["phase_inductance_h"]*(380/3)**2,c["sectional"]["phase_inductance_h"]*380**2)

    def test_cap_boundary_and_failure_retention(self):
        self.assertTrue(selected.loss_case(870,20,1,10,900)["pass"])
        failed=selected.loss_case(870,20,1,10.01,900)
        self.assertFalse(failed["pass"])
        self.assertLess(failed["remaining_margin_j"],0)

    def test_negative_loss_rejected(self):
        with self.assertRaises(ValueError):selected.loss_case(870,20,1,-1,900)

    def test_declared_checks(self):
        d=selected.calculate()
        self.assertTrue(d["verification_passed"])
        self.assertEqual(len(d["loss_sensitivity"]),16)
        self.assertEqual(d["open_items"],["P11","P39","P40"])

if __name__=="__main__":unittest.main()
