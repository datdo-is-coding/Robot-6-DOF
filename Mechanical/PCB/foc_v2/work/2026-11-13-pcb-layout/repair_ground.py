"""Connect small pad-bearing GND islands that have no room for a local via."""
import repair_grid as r
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
import json,math
b=r.b;p=r.p;r.guides[:]=[[] for _ in r.layers]
anchors=[];ports=[];pads=[]
for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND':
        pos=r.xy(t.GetPosition());ports.append(pos);anchors.append(Point(pos).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2+.02))
for f in b.GetFootprints():
    for a in f.Pads():
        if a.GetNetname()!='GND':continue
        if a.GetAttribute()==p.PAD_ATTRIB_PTH:
            pos=r.xy(a.GetPosition());ports.append(pos)
            s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,p.F_Cu,0,p.FromMM(.003),p.ERROR_OUTSIDE);anchors.append(r.polygons(s).buffer(.02))
        elif a.GetAttribute()==p.PAD_ATTRIB_SMD:
            s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,f.GetLayer(),0,p.FromMM(.003),p.ERROR_OUTSIDE)
            pads.append((a,f.GetLayer(),r.polygons(s)))
anchor=unary_union(anchors);results=[]
for z in b.Zones():
    if z.GetIsRuleArea() or z.GetNetname()!='GND' or z.GetLayer() not in [p.F_Cu,p.B_Cu]:continue
    layer=z.GetLayer();s=z.GetFilledPolysList(layer)
    def points(c):return [r.xy(c.CPoint(j)) for j in range(c.PointCount())]
    for j in range(s.OutlineCount()):
        poly=Polygon(points(s.COutline(j)),[points(s.CHole(j,k)) for k in range(s.HoleCount(j))])
        if not poly.is_valid:poly=poly.buffer(0)
        if poly.intersects(anchor) or poly.area<.05:continue
        sources=[a for a,l,g in pads if l==layer and poly.distance(g)<.003]
        if not sources:continue
        done=False
        for a in sources:
            pos=r.xy(a.GetPosition())
            for dest in sorted(set(ports),key=lambda v:math.dist(pos,v))[:4]:
                pair={'a':{'pos':pos,'layers':[b.GetLayerName(layer)],'net':'GND','kind':'PAD'},'b':{'pos':dest,'layers':[b.GetLayerName(l) for l in r.layers],'net':'GND','kind':'PCB_VIA'}}
                route,detail=r.connect(pair)
                if route:
                    r.commit(route,pair);done=True;break
            if done:break
        ref=sources[0].GetParentFootprint().GetReference()+'.'+sources[0].GetNumber()
        result={'source':ref,'area':poly.area,'ok':done};results.append(result);print(result,flush=True)
(r.W/'ground-repairs.json').write_text(json.dumps(results,indent=2)+'\n')
