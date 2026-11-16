"""Join any remaining isolated inner ground region to the main return."""
import repair_grid as r
from shapely.geometry import Polygon,Point
import math,json
b=r.b;p=r.p;r.guides[:]=[[] for _ in r.layers];b.BuildConnectivity();conn=b.GetConnectivity()
ports=[]
for v in b.GetTracks():
    if isinstance(v,p.PCB_VIA) and v.GetNetname()=='GND':ports.append((v,Point(r.xy(v.GetPosition())).buffer(p.ToMM(v.GetWidth(p.F_Cu))/2+.002)))
for f in b.GetFootprints():
    for a in f.Pads():
        if a.GetNetname()=='GND' and a.GetAttribute()==p.PAD_ATTRIB_PTH:
            s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,p.In1_Cu,0,p.FromMM(.001),p.ERROR_OUTSIDE);ports.append((a,r.polygons(s).buffer(.002)))
polys=[]
for z in b.Zones():
    if z.GetIsRuleArea() or z.GetNetname()!='GND' or not z.IsOnLayer(p.In1_Cu):continue
    s=z.GetFilledPolysList(p.In1_Cu)
    def pts(c):return [r.xy(c.CPoint(j)) for j in range(c.PointCount())]
    for j in range(s.OutlineCount()):
        g=Polygon(pts(s.COutline(j)),[pts(s.CHole(j,k)) for k in range(s.HoleCount(j))])
        if not g.is_valid:g=g.buffer(0)
        polys.append(g)
polys.sort(key=lambda g:g.area,reverse=True);assert polys
main=[a for a,g in ports if g.intersects(polys[0])];assert main
main_ids={a.m_Uuid.AsString() for a in main};results=[]
for g in polys[1:]:
    sources=[a for a,shape in ports if shape.intersects(g)]
    if sources and any(main_ids.intersection(a.m_Uuid.AsString() for a in conn.GetConnectedItems(source)) for source in sources):continue
    if sources:
        choices=sorted([(math.dist(r.xy(a.GetPosition()),r.xy(z.GetPosition())),a,z) for a in sources for z in main],key=lambda a:a[0])
    else:
        point=g.representative_point();choices=[(point.distance(Point(r.xy(z.GetPosition()))),(point.x,point.y),z) for z in main];choices.sort(key=lambda a:a[0])
    ok=False
    for _,a,z in choices[:8]:
        is_item=hasattr(a,'GetPosition');pos=r.xy(a.GetPosition()) if is_item else a
        pair={'a':{'pos':pos,'layers':[b.GetLayerName(l) for l in r.layers] if is_item else ['In1.Cu'],'net':'GND','kind':'PCB_VIA' if is_item else 'ZONE'},'b':{'pos':r.xy(z.GetPosition()),'layers':[b.GetLayerName(l) for l in r.layers],'net':'GND','kind':'PCB_VIA'}}
        route,detail=r.connect(pair)
        if route:r.commit(route,pair);ok=True;break
    record={'area':g.area,'connected':ok,'detail':detail};results.append(record);print(record,flush=True)
(r.W/'ground-bridges.json').write_text(json.dumps(results,indent=2)+'\n')
