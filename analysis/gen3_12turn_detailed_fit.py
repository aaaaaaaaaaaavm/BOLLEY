"""Evaluate my A5h CAD against its frozen ten bands."""
import argparse
import json
from common import ROOT, RESULTS, compare_json, dump_json
OUTPUT=RESULTS/"gen3_12turn_detailed_fit.json"
def calculate():
    manifest=json.loads((ROOT/"cad/BUILD_GEN3_12TURN.json").read_text())
    p=json.loads((ROOT/"cad/gen3_12turn_detailed_parameters.json").read_text())
    f,b=manifest["fit_checks"],p["bands"]
    checks={
        "turn_solids":f["turn_solid_count_per_cell"]==b["required_turn_solid_count_per_cell"],
        "face_solids":f["full_face_turn_solid_count"]==b["required_full_face_turn_solid_count"],
        "coil_core":f["coil_core_intersection_mm3"]<=b["maximum_coil_core_intersection_mm3"],
        "consecutive_cells":f["consecutive_cell_coil_intersection_mm3"]<=b["maximum_adjacent_coil_intersection_mm3"],
        "same_layer":f["same_layer_coil_intersection_mm3"]<=b["maximum_same_layer_coil_intersection_mm3"],
        "fluxrelay_clearance":f["coil_to_fluxrelay_radial_clearance_mm"]>=b["minimum_coil_to_fluxrelay_radial_clearance_mm"],
        "interlayer_clearance":f["interlayer_radial_clearance_mm"]>=b["minimum_interlayer_radial_clearance_mm"],
        "yoke_clearance":f["upper_coil_to_back_yoke_clearance_mm"]>=b["minimum_upper_coil_to_back_yoke_clearance_mm"],
        "copper_volume":abs(f["analytical_copper_volume_relative_error"])<=b["maximum_analytical_copper_volume_relative_error"],
        "mean_turn_length":abs(f["mean_turn_length_relative_error"])<=b["maximum_mean_turn_length_relative_error"],
    }
    return {"evidence":"A5h nominal conductor-envelope CAD, not manufacturing or electrical qualification",
            "source_manifest":"cad/BUILD_GEN3_12TURN.json","checks":checks,"band_count":len(checks),
            "band_pass_count":sum(checks.values()),"screen_pass":all(checks.values()),"fit_checks":f}
def main():
    p=argparse.ArgumentParser();p.add_argument("--write",action="store_true");p.add_argument("--check",action="store_true");a=p.parse_args();r=calculate()
    if a.write: dump_json(OUTPUT,r)
    elif a.check: compare_json(OUTPUT,r)
    else: print(json.dumps(r,indent=2))
if __name__=="__main__": main()
