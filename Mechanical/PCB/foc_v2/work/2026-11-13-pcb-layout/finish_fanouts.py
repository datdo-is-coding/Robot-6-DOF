"""Make final pad escapes while moving only narrow inner-layer signal tracks."""
import repair_grid as r
import sexpdata as sx
from shapely.geometry import Point,LineString
from shapely.ops import unary_union
import json,math,csv,sys
p=r.p;b=r.b;b.BuildConnectivity();conn=b.GetConnectivity()
report=json.loads((r.W/'remaining-fanouts-drc.json').read_text())
objects={a.m_Uuid.AsString():a for f in b.GetFootprints() for a in f.Pads()}
objects.update({a.m_Uuid.AsString():a for a in b.GetTracks()})
def members(o):return [objects.get(a.m_Uuid.AsString(),a) for a in [o,*conn.GetConnectedItems(o)]]
def has_port(items):return any(isinstance(a,p.PCB_VIA) or isinstance(a,p.PAD) and a.GetAttribute()==p.PAD_ATTRIB_PTH for a in items)
targets=[]
for pair in report['unconnected_items']:
    for item in pair['items']:
        o=objects.get(item['uuid'])
        if o is None:continue
        items=members(o)
        if has_port(items):continue
        pads=[a for a in items if isinstance(a,p.PAD) and a.GetNetname()==o.GetNetname()]
        if pads:targets.append(pads[0])
for f in b.GetFootprints():
    for a in f.Pads():
        if (f.GetReference(),a.GetNumber()) in [('U1','18'),('C52','2'),('U10','2')] and not has_port(members(a)):targets.append(a)
static=[[] for _ in r.layers];soft=[];smd=[]
for f in b.GetFootprints():
    for a in f.Pads():
        for i,l in enumerate(r.layers):
            if a.IsOnLayer(l):
                s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,l,0,p.FromMM(.001),p.ERROR_OUTSIDE);g=r.polygons(s);static[i].append((a.GetNetname(),g))
                if a.GetAttribute()==p.PAD_ATTRIB_SMD:smd.append(g)
        if a.GetAttribute()==p.PAD_ATTRIB_NPTH:
            s=p.SHAPE_POLY_SET();a.TransformHoleToPolygon(s,0,p.FromMM(.001),p.ERROR_OUTSIDE)
            for ls in static:ls.append((None,r.polygons(s)))
for t in b.GetTracks():
    net=t.GetNetname()
    if isinstance(t,p.PCB_VIA):
        for ls in static:ls.append((net,Point(r.xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2)))
    else:
        s=p.SHAPE_POLY_SET();t.TransformShapeToPolygon(s,t.GetLayer(),0,p.FromMM(.001),p.ERROR_OUTSIDE);g=r.polygons(s);i=r.layers.index(t.GetLayer())
        if t.GetLayer() in [p.In1_Cu,p.In2_Cu,p.B_Cu] and t.GetWidth()<p.FromMM(.8):soft.append((t.m_Uuid.AsString(),net,g,p.ToMM(t.GetLength())))
        else:static[i].append((net,g))
for z in b.Zones():
    if z.GetIsRuleArea():
        for i,l in enumerate(r.layers):
            if z.IsOnLayer(l):static[i].append((None,r.polygons(z.Outline())))
all_smd=unary_union(smd);removed=set();seen=set();records=[]
for a in targets:
    uid=a.m_Uuid.AsString()
    if uid in seen:continue
    seen.add(uid);f=a.GetParentFootprint();net=a.GetNetname();pos=r.xy(a.GetPosition());li=r.layers.index(f.GetLayer())
    foreign=[unary_union([g for n,g in ls if n!=net]) for ls in static];copper=unary_union(foreign);holes=unary_union(r.drill_guards)
    dx,dy=pos[0]-r.xy(f.GetPosition())[0],pos[1]-r.xy(f.GetPosition())[1]
    ux,uy=(math.copysign(1,dx),0) if abs(dx)>abs(dy) else (0,math.copysign(1,dy))
    s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,f.GetLayer(),0,p.FromMM(.001),p.ERROR_OUTSIDE);poly=r.polygons(s);xmin,ymin,xmax,ymax=poly.bounds;half=(xmax-xmin)/2 if ux else (ymax-ymin)/2
    candidates=[]
    for direction in [1,-1]:
        for extra in [.21,.31,.51,.71,1.01,1.51,2.01]:
            for side in [0,.05,-.05,.1,-.1,.2,-.2,.4,-.4]:
                q=direction*(half+extra);candidates.append((pos[0]+ux*q-uy*side,pos[1]+uy*q+ux*side,False))
    for q in [0,.1,-.1,.2,-.2,half+.15,-half-.15,half+.1,-half-.1]:
        for side in [0,.025,-.025]:candidates.append((pos[0]+ux*q-uy*side,pos[1]+uy*q+ux*side,True))
    best=None
    for x,y,vip in candidates:
        pt=Point(x,y)
        if math.hypot(x-100,y-100)>34.15 or pt.distance(copper)<.35-1e-7 or holes.intersects(pt):continue
        if not vip and pt.distance(all_smd)<.2:continue
        if LineString([pos,(x,y)]).distance(foreign[li])<.226:continue
        cuts=[(u,length) for u,n,g,length in soft if u not in removed and n!=net and g.distance(pt)<.351]
        score=3*vip+sum(1+min(length,20)/20 for _,length in cuts)+.05*math.dist(pos,(x,y))
        if best is None or score<best[0]:best=(score,x,y,vip,[u for u,_ in cuts])
    ref=f.GetReference()+'.'+a.GetNumber()
    if best is None:print(ref,'NO STATICALLY CLEAR ESCAPE',flush=True);continue
    _,x,y,vip,cuts=best;removed.update(cuts)
    v=p.PCB_VIA(b);v.SetPosition(r.vec((x,y)));v.SetWidth(p.FromMM(.4));v.SetDrill(p.FromMM(.2));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(a.GetNetCode())
    if vip:v.SetFillingMode(p.FILLING_MODE_FILLED);v.SetCappingMode(p.CAPPING_MODE_CAPPED)
    b.Add(v);r.drill_guards.append(Point(x,y).buffer(.455))
    for ls in static:ls.append((net,Point(x,y).buffer(.2)))
    if math.dist(pos,(x,y))>1e-6:
        t=p.PCB_TRACK(b);t.SetStart(r.vec(pos));t.SetEnd(r.vec((x,y)));t.SetWidth(p.FromMM(.15));t.SetLayer(f.GetLayer());t.SetNetCode(a.GetNetCode());b.Add(t);static[li].append((net,LineString([pos,(x,y)]).buffer(.075)))
    row={'pad':ref,'net':net,'x_mm':x,'y_mm':y,'filled_and_copper_capped':vip};records.append(row);print(row,'inner tracks to reconnect',len(cuts),flush=True)
p.SaveBoard(str(r.path),b)
data=sx.loads(r.path.read_text())
def sub(n,k):return next((a for a in n if isinstance(a,list) and a and str(a[0])==k),None)
data[:]=[a for a in data if not(isinstance(a,list) and a and str(a[0]) in ['segment','arc'] and sub(a,'uuid') and sub(a,'uuid')[1] in removed)];r.path.write_text(sx.dumps(data)+'\n')
previous=json.loads((r.W/'pad-escape-vias.json').read_text());previous.extend(records);(r.W/'pad-escape-vias.json').write_text(json.dumps(previous,indent=2)+'\n')
with (r.W/'VIPPO_REQUIRED.csv').open('w') as out:
    writer=csv.DictWriter(out,fieldnames=['pad','net','x_mm','y_mm','filled_and_copper_capped']);writer.writeheader();writer.writerows(a for a in previous if a['filled_and_copper_capped'])
(r.W/'fanout-inner-repairs.json').write_text(json.dumps({'new_escapes':records,'inner_tracks_removed':sorted(removed)},indent=2)+'\n')
