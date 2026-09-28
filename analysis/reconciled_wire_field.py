"""A6k: fresh wire-resolved field on the common A6j-R2 geometry."""
import argparse,copy,hashlib,json
from pathlib import Path
import numpy as np
import gen2_field as e
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/results/reconciled_wire_field.json'
DOC=ROOT/'docs/RECONCILED_WIRE_FIELD.md'
BASE_LOAD=e.load;BASE_BOUNDARIES=e.geometry_boundaries;BASE_CLASSIFY=e.classify_elements
KEYS=('mesh_mean_field_convergence','mesh_coenergy_convergence','outer_boundary_sensitivity','source_current_closure','nonlinear_convergence')


def parameters(index):
    shared=json.loads((ROOT/'cad/core_winding_reconciled_parameters.json').read_text())
    p=shared['field'];sel=json.loads((ROOT/'cad/gen3_12turn_detailed_parameters.json').read_text())['selected_winding']
    w,t=sel['bare_width_mm']*.001,sel['bare_thickness_mm']*.001
    p['wire_rectangles']=[]
    for n,rect in enumerate(shared['wires_mm'][index]):
        y=(rect[0]+rect[1])*.0005;z=(rect[2]+rect[3])*.0005
        p['wire_rectangles'].append(dict(y=[y-t/2,y+t/2],z=[z-w/2,z+w/2],sign=1 if n%2==0 else -1))
    p['excitation'].update(turns=12,phase_current_rms_a=1520/12,copper_area_per_turn_m2=w*t,source_current_density_rms_a_m2=(1520/12)/(w*t))
    for key in ('a3g_per_cell_inductance_h','a8b_active_window_phase_inductance_h'):p['targets'][key]*=9
    return p


def boundaries(p):
    y,z=BASE_BOUNDARIES(p)
    for w in p['wire_rectangles']:y.extend(w['y']);z.extend(w['z'])
    return y,z


def classify(centres,p):
    tags,_=BASE_CLASSIFY(centres,p);source=np.zeros(centres.shape[1])
    for w in p['wire_rectangles']:
        mask=e.in_rectangle(centres[0],centres[1],w['y'],w['z'])
        if np.any(tags[mask]!=0):raise ValueError('COPPER_INTERSECTS_CORE')
        if np.any(source[mask]!=0):raise ValueError('CONDUCTOR_OVERLAP')
        source[mask]=w['sign']*p['excitation']['source_current_density_rms_a_m2']
    return tags,source


def hashes():
    paths=['analysis/reconciled_wire_field.py','analysis/gen2_field.py','cad/core_winding_reconciled_parameters.json','cad/gen3_12turn_detailed_parameters.json','validation/A6k_reconciled_wire_field.md']
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}


def report(d):
    lines=['# Fresh wire-resolved field of the reconciled geometry','','Adityavardhan Mishra · 17 September 2026','',
        'I test the actual twelve bare-wire transverse sections on A6j-R2: 0.25 mm winding lift and 2 mm yoke/outer-leg rise, retaining the 4 mm haunch. This is a fresh nonlinear field calculation, not a transferred A6h verdict.','',
        '| Placement | Mean field, fine (T) | Numerical checks | Failed physical/model bands |','|---|---:|---|---|']
    for row in d['placements']:
        result=row['result'];mean=result['mesh_results']['fine']['mean_tooth_slice_field_rms_t']
        lines.append(f"| {row['name']} | {mean:.6f} | {'pass' if row['numerical_pass'] else 'fail'} | {', '.join(result['failed_bands']) or 'none'} |")
    lines+=['',f"Disposition: **{d['disposition']}**.",'',
        'The current-source integral, convergence and physical bands remain distinct. A geometry clearance pass cannot repair magnetic performance. No selected powered coupon, end-lead geometry, transient force/current, hot switching, protection or thermal validation follows from this transverse RMS-equivalent magnetostatic model.','',
        '[Criteria](../validation/A6k_reconciled_wire_field.md) · [Full resolved inputs and mesh results](../analysis/results/reconciled_wire_field.json) · [Geometry](CORE_WINDING_RECONCILIATION.md)','']
    return '\n'.join(lines)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');a=parser.parse_args()
    if a.check:
        d=json.loads(OUT.read_text());assert d['source_sha256']==hashes() and DOC.read_text()==report(d)
        for index,row in enumerate(d['placements']):assert row['parameters']==parameters(index)
        print(d['disposition']);raise SystemExit(0)
    rows=[]
    try:
        e.GATE_LABEL='A6k';e.geometry_boundaries=boundaries;e.classify_elements=classify
        for index,name in enumerate(('lower','upper')):
            p=parameters(index);e.load=lambda:p;np.random.seed(0)
            result,solutions=e.calculate()
            source=all(abs(s.metrics['source_current_positive_a']/1520-1)<=1e-8 and abs(s.metrics['source_current_negative_a']/1520+1)<=1e-8 for s in solutions.values())
            rows.append(dict(name=name,parameters=p,result=result,source_integral_pass=source,numerical_pass=source and all(result['bands'][k] for k in KEYS)))
            (ROOT/f'validation/results/A6k_{name}_completed.json').write_text(json.dumps(rows[-1],indent=2,sort_keys=True)+'\n')
            del solutions
    finally:e.load=BASE_LOAD;e.geometry_boundaries=BASE_BOUNDARIES;e.classify_elements=BASE_CLASSIFY
    numerical=all(r['numerical_pass'] for r in rows);physical=all(r['result']['screen_pass'] for r in rows)
    d=dict(study='A6k',placements=rows,numerical_pass=numerical,physical_pass=physical,source_sha256=hashes(),
        disposition='NUMERICS_UNRESOLVED' if not numerical else 'PASS_TRANSVERSE_SCREEN_ONLY' if physical else 'REJECT_POWERED_COUPON_PROMOTION')
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');DOC.write_text(report(d));print(d['disposition'])
