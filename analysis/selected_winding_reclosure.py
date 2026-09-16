"""A9g: ideal-current-tracking 12-turn reclosure and omitted-loss budget."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from common import ROOT, RESULTS, compare_json, dump_json
import sectional_drive as a9
from sectional_drive_a9b import corrected_resolution

OUTPUT=RESULTS/"selected_winding_reclosure.json"
DOC=ROOT/"docs/SELECTED_WINDING_RECLOSURE.md"

def scaled_inputs(parameters,base,circuit,turns):
    p,b,c=copy.deepcopy(parameters),copy.deepcopy(base),copy.deepcopy(circuit)
    scale=turns/p["fixed"]["turns_per_cell"]
    if not isinstance(turns,int) or turns<=0:raise ValueError("positive integer turns required")
    p["fixed"]["turns_per_cell"]=turns
    p["fixed"]["rated_phase_current_a"]/=scale
    p["fixed"]["conductor_area_per_turn_mm2"]/=scale
    c["rated"]["phase_current_rms_a"]/=scale
    c["sectional"]["phase_inductance_h"]*=scale**2
    p["fixed"]["a6h_three_cell_phase_inductance_h"]=c["sectional"]["phase_inductance_h"]
    for k in ("a7c_phase_resistance_nominal_ohm","a7c_phase_resistance_hot_ohm"):
        p["fixed"][k]*=scale**2
    for corner in c["corners"]:
        corner["phase_resistance_ohm"]*=scale**2
        for name in ("reference","qualification"):
            corner[name]["maximum_required_dc_link_v"]*=scale
    return p,b,c

def loss_case(noninverter,conduction,multiplier,extra,cap):
    if min(noninverter,conduction,extra)<0 or multiplier<1:raise ValueError("invalid loss assumption")
    energy=noninverter+conduction*multiplier+extra
    return {"source_energy_j":energy,"remaining_margin_j":cap-energy,"pass":energy<=cap}

def calculate():
    p=a9.load(a9.INPUT);base=a9.load(a9.BASE_INPUT);circuit=a9.load(a9.A7C_RESULT)
    trade=a9.load(ROOT/"analysis/turn_current_exchange_parameters.json")
    selected=a9.load(RESULTS/"turn_current_exchange.json")["selected_candidate"]
    path=a9.load(RESULTS/"gen3_12turn_path_fit.json")["selected_candidate"]
    cad=a9.load(ROOT/"cad/gen3_12turn_detailed_parameters.json")["selected_winding"]
    fit=a9.load(RESULTS/"gen3_12turn_detailed_fit.json")
    turns=selected["turns_per_cell"];scale=turns/p["fixed"]["turns_per_cell"]
    if turns!=cad["turns_per_cell"] or not math.isclose(path["bare_area_per_turn_mm2"],selected["conductor_area_per_turn_mm2"],rel_tol=1e-12):
        raise ValueError("selected winding geometry/electrical partition mismatch")
    sp,sb,sc=scaled_inputs(p,base,circuit,turns)
    resolutions=[];identities=[]
    for n in (100,200):
        original=corrected_resolution(a9.calculate_resolution(p,base,circuit,n),p["bands"])[0]
        fresh=corrected_resolution(a9.calculate_resolution(sp,sb,sc,n),p["bands"])[0]
        before,after=a9.maxima(original),a9.maxima(fresh)
        checks={}
        for key,value in before.items():
            factor=1/scale if "current" in key else scale if "dc_link" in key else 1
            checks[key]=math.isclose(after[key],value*factor,rel_tol=1e-9,abs_tol=1e-8)
        identities.append(checks);resolutions.append(fresh)
    coarse,fine=map(a9.maxima,resolutions)
    convergence={k:math.isclose(coarse[k],fine[k],rel_tol=0.01,abs_tol=1e-8) for k in fine}
    b=trade["baseline"];module=trade["supplier_module"]
    parallel=selected["minimum_parallel_modules_per_phase_per_local_bridge"]
    phase_path=b["active_abc_modules_per_face"]*module["combined_half_bridge_effective_phase_path_ohm_25c"]/parallel
    conduction={name:b["phases_per_face"]*phase_path*b[f"{name}_sum_face_channel_current_squared_a2"]/scale**2*b["shot_time_s"] for name in ("reference","qualification")}
    losses=[]
    for multiplier,extra in itertools.product((1.0,1.25,1.5,2.0),(0.0,5.0,10.0,20.0)):
        row={"conduction_multiplier_assumption":multiplier,"additional_loss_j_assumption":extra}
        for name,cap in (("reference",900.0),("qualification",1500.0)):
            row[name]=loss_case(b[f"{name}_noninverter_machine_energy_j"],conduction[name],multiplier,extra,cap)
        losses.append(row)
    loss_identity=all(abs(losses[0][name]["source_energy_j"]-selected[f"{name}_source_energy_j"])<=1e-8 for name in ("reference","qualification"))
    verification=all(all(c.values()) for c in identities) and all(convergence.values()) and loss_identity and fit["screen_pass"]
    sources=["analysis/selected_winding_reclosure.py","analysis/sectional_drive.py","analysis/sectional_drive_a9b.py",
        "analysis/sectional_drive_parameters.json","cad/fluxbridge_parameters.json","analysis/results/gen27_cage_circuit.json",
        "analysis/turn_current_exchange_parameters.json","analysis/results/turn_current_exchange.json",
        "cad/gen3_12turn_detailed_parameters.json","analysis/results/gen3_12turn_path_fit.json",
        "analysis/results/gen3_12turn_detailed_fit.json","validation/A9g_selected_winding_reclosure.md"]
    return {"study":"A9g","evidence":"IDEAL_CURRENT_TRACKING_RECLOSURE_AND_ASSUMED_LOSS_SENSITIVITY",
        "source_sha256":{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in sources},
        "turns":turns,"rated_phase_current_a":sp["fixed"]["rated_phase_current_a"],
        "resolutions":resolutions,"scaling_identity_checks":identities,"convergence_checks":convergence,
        "a9f_conduction_identity":loss_identity,"controlling":fine,
        "healthy_10pct_voltage_margin_passed":48/fine["maximum_required_dc_link_v"]-1>=0.1,
        "loss_sensitivity":losses,"passing_reference_loss_corners":sum(x["reference"]["pass"] for x in losses),
        "reference_added_loss_limit_j":900-selected["reference_source_energy_j"],
        "reference_conduction_multiplier_limit":(900-b["reference_noninverter_machine_energy_j"])/conduction["reference"],
        "module_only_mass_kg":selected["module_only_mass_kg"],"installed_module_count":selected["installed_onsemi_module_count"],
        "verification_passed":verification,"screen_pass":verification,"open_items":["P11","P39","P40"],
        "disposition":"BOUNDED_RECLOSURE_ONLY_HOT_SWITCHING_AND_FIELD_OPEN"}

def report(d):
    f=d["controlling"]
    lines=["# Selected twelve-turn drive: what the remaining margin buys", "",
        "I rerun the existing time-domain handoff envelope at A9f's twelve-turn partition and reconcile it with the A5h nominal winding. This is ideal-current tracking and fixed-MMF scaling. I have not solved the individual conductors' nonlinear field or selected a qualified pulse-power chain.", "",
        f"Verification: **{'PASS' if d['verification_passed'] else 'FAIL'}**. Rated phase current: **{d['rated_phase_current_a']:.6f} A**. The generic-inverter A9 envelope's physical bands pass at both resolutions: **{all(r['pass'] for r in d['resolutions'])}**. The local-bridge energy accounting is reported separately below.", "",
        f"The conservative link envelope is **{f['maximum_required_dc_link_v']:.6f} V healthy** and **{f['maximum_failed_cell_required_dc_link_v']:.6f} V with failed-cell compensation**. A9f's 10% healthy margin: **{'PASS' if d['healthy_10pct_voltage_margin_passed'] else 'FAIL'}**. R and L rise by nine, current falls by three and the calculated voltage rises by three; ideal winding and magnetic energy are unchanged.", "",
        f"At the A9f 25 C conduction point, only **{d['reference_added_loss_limit_j']:.6f} J** remains below the 900 J reference cap. With no other added loss, the allowed conduction-resistance multiplier is **{d['reference_conduction_multiplier_limit']:.6f}**. Neither value is a thermal rating.", "",
        "| Assumed conduction multiplier | Added loss (J) | Reference source (J) | Margin (J) | Reference cap | Qualification source (J) |",
        "|---:|---:|---:|---:|---|---:|"]
    for x in d["loss_sensitivity"]:
        r=x["reference"]
        lines.append(f"| {x['conduction_multiplier_assumption']:.2f} | {x['additional_loss_j_assumption']:.0f} | {r['source_energy_j']:.6f} | {r['remaining_margin_j']:.6f} | {'PASS' if r['pass'] else 'FAIL'} | {x['qualification']['source_energy_j']:.6f} |")
    lines += ["", f"Only {d['passing_reference_loss_corners']}/16 assumed loss corners meet the reference cap. I retain failures rather than move the cap. The {d['installed_module_count']} modules alone weigh {d['module_only_mass_kg']:.4f} kg, before busbar, capacitors, gate drive, cooling, wiring or structure.", "",
        "## Precise next work", "",
        "The 160 A supplier characterization point used by A9f is not a permissible pulse-current rating. Resolve RMS/peak waveform and internal parallel-path definitions from the supplier documentation, then include temperature-dependent resistance, switching energy, dead time, commutation parasitics, protection, DC-link sag and cooling in one circuit/configuration. Re-solve the A5h conductor distribution and lead/terminal geometry before inheriting the earlier field map. Supplier curves and a current/voltage/temperature waveform experiment must bound the omitted-loss budget.", "",
        "P11, P39 and P40 remain OPEN. P38 keeps its prior limited MODELLED disposition. A5f's copper-volume failure and A9e's selector rejection are unchanged. A5h remains nominal CAD, not manufacturing evidence.", "",
        "[Criteria](../validation/A9g_selected_winding_reclosure.md) · [Full result](../analysis/results/selected_winding_reclosure.json) · [Current review](CURRENT_REVIEW.md)", "",
        "Reproduce: `python analysis/selected_winding_reclosure.py --check`.", ""]
    return "\n".join(lines)

def main():
    p=argparse.ArgumentParser();p.add_argument("--write",action="store_true");p.add_argument("--check",action="store_true");a=p.parse_args();d=calculate()
    if a.write:dump_json(OUTPUT,d);DOC.write_text(report(d))
    elif a.check:
        compare_json(OUTPUT,d)
        if DOC.read_text()!=report(a9.load(OUTPUT)):raise SystemExit("A9g report stale")
    else:print(json.dumps(d,indent=2))
    if not d["verification_passed"]:raise SystemExit("A9g verification failed; retain result")
    print(f"A9g: numerical verification PASS; {d['passing_reference_loss_corners']}/16 assumed reference-loss corners pass")

if __name__=="__main__":main()
