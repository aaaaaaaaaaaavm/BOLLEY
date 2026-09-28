"""A6j: retain the field haunch and reconcile a transverse CAD candidate."""
import argparse,copy,hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
import gen2_field as field
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/results/core_winding_reconciliation.json'
DOC=ROOT/'docs/CORE_WINDING_RECONCILIATION.md'
PARAM=ROOT/'cad/core_winding_reconciled_parameters.json'
CAD=ROOT/'cad/exports/core_reconciliation'


def inputs(rise):
    field.INPUT=ROOT/'cad/gen27_field_parameters.json';p=field.load();g=p['geometry']
    g['back_yoke_z_m']=[z+rise*.001 for z in g['back_yoke_z_m']]
    g['outer_leg_z_m'][1]+=rise*.001
    winding=json.loads((ROOT/'cad/gen3_12turn_detailed_parameters.json').read_text())['selected_winding']
    s=json.loads((ROOT/'cad/gen3_parameters.json').read_text())['stator']
    cy=-s['core_face_footprint_mm']/2+s['outer_return_leg_width_mm']/2
    rects=[]
    for placement in (0,1):
        height=winding['lower_coil_start_above_payload_face_mm']+placement*(3*winding['insulated_overall_width_mm']+winding['interlayer_radial_clearance_mm'])
        wires=[]
        for layer in range(3):
            z=height+layer*winding['insulated_overall_width_mm']
            for turn in range(4):
                a=winding['inner_transverse_span_mm']/2+turn*winding['insulated_overall_thickness_mm'];b=a+winding['insulated_overall_thickness_mm']
                for sign in (-1,1):
                    y=sorted((cy+sign*a,cy+sign*b));wires.append([*y,z,z+winding['insulated_overall_width_mm']])
        rects.append(wires)
    return dict(field=p,wires_mm=rects,rise_mm=rise,axial_depth_mm=g['tooth_axial_depth_m']*1000)


def core_parts(d):
    g=d['field']['geometry'];rects=[]
    for yy in g['outer_leg_intervals_y_m']:rects.append([*yy,*g['outer_leg_z_m']])
    for yy in g['separator_intervals_y_m']:rects.append([*yy,*g['separator_z_m']])
    rects.append([*g['back_yoke_y_m'],*g['back_yoke_z_m']])
    rects=[[v*1000 for v in r] for r in rects]
    r=g['inner_corner_fillet_radius_m']*1000;top=g['back_yoke_z_m'][0]*1000
    left=g['outer_leg_intervals_y_m'][0][1]*1000;right=g['outer_leg_intervals_y_m'][-1][0]*1000
    return rects,[(left,top-r,r,1),(right,top-r,r,-1)]


def rect_distance(a,b):
    return math.hypot(max(a[0]-b[1],b[0]-a[1],0),max(a[2]-b[3],b[2]-a[3],0))


def haunch_distance(w,h):
    edge,z0,r,sign=h
    aa=sorted([sign*(w[0]-edge),sign*(w[1]-edge)]);a=[*aa,w[2]-z0,w[3]-z0]
    lo,hi=max(a[0],0),min(a[1],r);bottom,top=max(a[2],0),min(a[3],r)
    if lo<=hi and bottom<=top and max((x-r)**2+z*z for x in (lo,hi) for z in (bottom,top))>=r*r:return 0.
    # Boundary of square-minus-circle: left edge, top edge and circular arc.
    straight=min(rect_distance(a,[0,0,0,r]),rect_distance(a,[0,r,r,r]))
    def f(theta):
        x,z=r+r*math.cos(theta),r*math.sin(theta)
        return rect_distance(a,[x,x,z,z])
    result=minimize_scalar(f,bounds=(math.pi/2,math.pi),method='bounded',options={'xatol':1e-14})
    return min(straight,result.fun,f(math.pi/2),f(math.pi))


def distances(d):
    rects,haunches=core_parts(d)
    return [min(min(rect_distance(w,r) for r in rects) for w in wires) if not haunches else
        min(min([rect_distance(w,r) for r in rects]+[haunch_distance(w,h) for h in haunches]) for w in wires)
        for wires in d['wires_mm']]


def solids(d):
    import cadquery as cq
    depth=d['axial_depth_mm'];rects,haunches=core_parts(d)
    def box(r):return cq.Solid.makeBox(depth,r[1]-r[0],r[3]-r[2],cq.Vector(0,r[0],r[2]))
    shapes=[box(r) for r in rects]
    for edge,z0,r,sign in haunches:
        yy=sorted((edge,edge+sign*r));square=box([*yy,z0,z0+r])
        circle=cq.Solid.makeCylinder(r,depth,cq.Vector(0,edge+sign*r,z0),cq.Vector(1,0,0))
        shapes.append(square.cut(circle))
    core=shapes[0].fuse(*shapes[1:]).clean()
    return cq,core,[cq.Compound.makeCompound([box(w) for w in wires]) for wires in d['wires_mm']]


def provenance():
    paths=['analysis/core_winding_reconciliation.py','analysis/gen2_field.py','cad/gen3_parameters.json','cad/gen3_12turn_detailed_parameters.json','validation/A6j_core_winding_reconciliation.md']
    name='cad/gen27_field_parameters.json'
    while name:
        paths.append(name);name=json.loads((ROOT/name).read_text()).get('extends')
    return {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in paths}


def build():
    cases=[]
    for rise in (0,.5,1,1.5,2,3,4):
        d=inputs(rise);clearances=distances(d)
        cases.append(dict(rise_mm=rise,clearance_mm=clearances,accepted=min(clearances)>=.5))
    accepted=[r for r in cases if r['accepted']];selected=accepted[0] if accepted else None
    if selected is None:raise ValueError('NO_GEOMETRY_CANDIDATE')
    d=inputs(selected['rise_mm']);cq,core,wires=solids(d);_,oldcore,_=solids(inputs(0))
    exact=[core.distance(w) for w in wires];overlap=[core.intersect(w).Volume() for w in wires]
    g=d['field']['geometry'];expected=sum((b-a)*1000 for a,b in g['outer_leg_intervals_y_m'])*selected['rise_mm']*d['axial_depth_mm']
    volume=core.Volume()-oldcore.Volume()
    check=dict(clearance_agreement=max(abs(x-y) for x,y in zip(exact,selected['clearance_mm']))<=1e-5,
        no_intersection=max(overlap)<=1e-6,core_increment=abs(volume/expected-1)<=1e-5,
        original_geometry_rejected=not cases[0]['accepted'],valid_solids=core.isValid() and all(w.isValid() for w in wires))
    CAD.mkdir(parents=True,exist_ok=True)
    cq.exporters.export(core,str(CAD/'Core_With_Haunch.step'))
    for name,w in zip(('Lower','Upper'),wires):cq.exporters.export(cq.Compound.makeCompound([core,w]),str(CAD/(name+'_Transverse_Coupon.step')))
    PARAM.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    return dict(study='A6j',cases=cases,selected=selected,exact_clearance_mm=exact,intersection_mm3=overlap,
        core_volume_increment_mm3=volume,analytical_increment_mm3=expected,verification=check,
        scope='GEOMETRY_ONLY_NO_NEW_FIELD_ACCEPTANCE',cadquery_version=cq.__version__,source_sha256=provenance(),
        artifact_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [PARAM,*sorted(CAD.glob('*.step'))]})


def report(d):
    out=['# Common core and winding geometry candidate','','Adityavardhan Mishra · 17 September 2026','',
        'I retain the inherited 4 mm inner haunch and the existing twelve-turn winding. Raising the back yoke and extending the outer legs provides a geometry-only candidate. The original arrangement is retained as a rejected case.','',
        '| Back-yoke rise (mm) | Lower clearance (mm) | Upper clearance (mm) | 0.5 mm assumed layout margin |','|---:|---:|---:|---|']
    for r in d['cases']:out.append(f"| {r['rise_mm']:g} | {r['clearance_mm'][0]:.6f} | {r['clearance_mm'][1]:.6f} | {'pass' if r['accepted'] else 'fail'} |")
    out+=['',f"The smallest sampled passing rise is **{d['selected']['rise_mm']:g} mm**. Exact solid clearance is {d['exact_clearance_mm'][0]:.6f} / {d['exact_clearance_mm'][1]:.6f} mm for the lower/upper slices. The per-cell core volume increases by {d['core_volume_increment_mm3']:.6f} mm³. This has a mass and magnetic-path penalty; no installed mass advantage is claimed.",'',
        'The resolved parameter file defines both the revised field geometry and the conductor envelopes used to generate the three STEP coupon references. Coordinates are transverse millimetres from the payload face, with axial depth equal to one tooth. These are straight conductor slices, not closed three-dimensional turns, full-face assemblies or terminal geometry.','',
        'New magnetic analysis is required for this exact geometry. A6h cannot be inherited. Previously reported A6i results are not available in this working copy; its reported failures are not replaced by this geometric clearance result. Hot drive, end effects, protection, thermal duty and the 0.20 mm payload lane gap remain open. No powered coupon is released.','',
        f"Geometric verification: {'PASS' if all(d['verification'].values()) else 'FAIL'}.",'',
        '[Criteria](../validation/A6j_core_winding_reconciliation.md) · [Results](../analysis/results/core_winding_reconciliation.json) · [Common parameters](../cad/core_winding_reconciled_parameters.json) · [STEP references](../cad/exports/core_reconciliation)','']
    return '\n'.join(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.check:
        d=json.loads(OUT.read_text());assert d['source_sha256']==provenance() and DOC.read_text()==report(d)
        assert all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in d['artifact_sha256'].items())
        for r in d['cases']:assert np.allclose(distances(inputs(r['rise_mm'])),r['clearance_mm'],rtol=0,atol=1e-8)
    else:
        d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');DOC.write_text(report(d))
    print(d['selected'],d['verification']);assert all(d['verification'].values())
