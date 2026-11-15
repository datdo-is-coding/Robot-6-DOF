"""Create manufacturable escapes for isolated IC pads, documenting VIPPO fallbacks."""
import repair_grid as r
from shapely.geometry import Point,LineString
from shapely.ops import unary_union
import json,math,csv,sys
p=r.p;b=r.b;b.BuildConnectivity();conn=b.GetConnectivity()
report=json.loads((r.W/'0p4-control-drc.json').read_text())
byid={a.m_Uuid.AsString():a for f in b.GetFootprints() for a in f.Pads()}
byid.update({a.m_Uuid.AsString():a for a in b.GetTracks()})
targets=[]
for pair in report['unconnected_items']:
    for item in pair['items']:
        o=byid.get(item['uuid'])
        if o is None:continue
        members=[o,*conn.GetConnectedItems(o)]
        if any(isinstance(a,p.PCB_VIA) or isinstance(a,p.PAD) and a.GetAttribute()==p.PAD_ATTRIB_PTH for a in members):continue
        candidates=[a for a in members if isinstance(a,p.PAD) and a.GetNetname()==o.GetNetname()]
        if candidates:targets.append(candidates[0])
for f in b.GetFootprints():
    for a in f.Pads():
        if (f.GetReference(),a.GetNumber()) in [('U1','18'),('R34','1'),('C52','2'),('U10','2'),('C21','1')]:targets.append(a)
seen=set();records=[]
pad_geoms=[]
for f in b.GetFootprints():
    for a in f.Pads():
        if a.GetAttribute()==p.PAD_ATTRIB_SMD:
            s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,f.GetLayer(),0,p.FromMM(.001),p.ERROR_OUTSIDE);pad_geoms.append(r.polygons(s))
all_smd=unary_union(pad_geoms)
for a in targets:
    uid=a.m_Uuid.AsString()
    if uid in seen:continue
    seen.add(uid);f=a.GetParentFootprint();net=a.GetNetname();pos=r.xy(a.GetPosition());layer=f.GetLayer();li=r.layers.index(layer)
    foreign=[unary_union([g for n,g in ls if n!=net]) for ls in r.shapes]
    hole_guard=unary_union(r.drill_guards)
    copper=unary_union(foreign)
    cx,cy=r.xy(f.GetPosition());dx,dy=pos[0]-cx,pos[1]-cy
    ux,uy=(math.copysign(1,dx),0) if abs(dx)>abs(dy) else (0,math.copysign(1,dy))
    s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,layer,0,p.FromMM(.001),p.ERROR_OUTSIDE);poly=r.polygons(s)
    xmin,ymin,xmax,ymax=poly.bounds;half=(xmax-xmin)/2 if ux else (ymax-ymin)/2
    candidates=[]
    for direction in [1,-1]:
        for extra in [.21,.26,.31,.41,.51,.71,1.01]:
            for side in [0,.05,-.05,.1,-.1,.2,-.2]:
                length=direction*(half+extra);candidates.append((pos[0]+ux*length-uy*side,pos[1]+uy*length+ux*side,False))
    # Filled and copper-capped vias are used only when a normal escape cannot fit.
    for along in [0,.1,-.1,.2,-.2,half+.15,-half-.15,half+.1,-half-.1]:
        for side in [0,.025,-.025]:candidates.append((pos[0]+ux*along-uy*side,pos[1]+uy*along+ux*side,True))
    found=None
    for x,y,vippo in candidates:
        pt=Point(x,y)
        if math.hypot(x-100,y-100)>34.15 or pt.distance(copper)<.351 or hole_guard.intersects(pt):continue
        if not vippo and pt.distance(all_smd)<.2:continue
        line=LineString([pos,(x,y)])
        if line.distance(foreign[li])<.226:continue
        found=(x,y,vippo);break
    ref=f.GetReference()+'.'+a.GetNumber()
    if found is None:print(ref,net,'no escape',flush=True);continue
    x,y,vippo=found;v=p.PCB_VIA(b);v.SetPosition(r.vec((x,y)));v.SetWidth(p.FromMM(.4));v.SetDrill(p.FromMM(.2));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(a.GetNetCode())
    if vippo:v.SetFillingMode(p.FILLING_MODE_FILLED);v.SetCappingMode(p.CAPPING_MODE_CAPPED)
    b.Add(v);r.add_shape(Point(x,y).buffer(.2),net,range(4));r.drill_guards.append(Point(x,y).buffer(.455))
    if math.dist(pos,(x,y))>1e-6:
        t=p.PCB_TRACK(b);t.SetStart(r.vec(pos));t.SetEnd(r.vec((x,y)));t.SetWidth(p.FromMM(.15));t.SetLayer(layer);t.SetNetCode(a.GetNetCode());b.Add(t);r.add_shape(LineString([pos,(x,y)]).buffer(.075),net,[li])
    row={'pad':ref,'net':net,'x_mm':x,'y_mm':y,'filled_and_copper_capped':vippo};records.append(row);print(row,flush=True)
p.SaveBoard(str(r.path),b)
(r.W/'pad-escape-vias.json').write_text(json.dumps(records,indent=2)+'\n')
with (r.W/'VIPPO_REQUIRED.csv').open('w') as out:
    writer=csv.DictWriter(out,fieldnames=['pad','net','x_mm','y_mm','filled_and_copper_capped']);writer.writeheader();writer.writerows(a for a in records if a['filled_and_copper_capped'])
