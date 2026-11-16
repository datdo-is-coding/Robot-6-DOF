"""Connect pad-bearing ground islands with safe, tented through vias."""
import repair_grid as r
from shapely.ops import unary_union
from shapely.geometry import Polygon,Point
import numpy as np
import shapely as sh
import json,math
b=r.b;p=r.p
foreign=unary_union([g for ls in r.shapes for net,g in ls if net!='GND']).buffer(.365)
avoid=unary_union([foreign,*r.drill_guards,*r.pad_guards])
anchors=[]
for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND':anchors.append(Point(r.xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2+.02))
for f in b.GetFootprints():
    for a in f.Pads():
        if a.GetNetname()=='GND' and a.GetAttribute()==p.PAD_ATTRIB_PTH:
            s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,p.F_Cu,0,p.FromMM(.005),p.ERROR_OUTSIDE);anchors.append(r.polygons(s).buffer(.02))
anchor=unary_union(anchors);added=[];failed=[]
for z in b.Zones():
    if z.GetIsRuleArea() or z.GetNetname()!='GND':continue
    layer=z.GetLayer();s=z.GetFilledPolysList(layer)
    # Remove unused floating copper; pad-bearing islands are stitched below.
    z.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
    if layer not in [p.F_Cu,p.B_Cu]:continue
    for j in range(s.OutlineCount()):
        def points(c):return [r.xy(c.CPoint(i)) for i in range(c.PointCount())]
        poly=Polygon(points(s.COutline(j)),[points(s.CHole(j,k)) for k in range(s.HoleCount(j))])
        if not poly.is_valid:poly=poly.buffer(0)
        if poly.intersects(anchor) or poly.area<.05:continue
        xmin,ymin,xmax,ymax=poly.bounds
        xs=np.arange(math.ceil(xmin*20)/20,xmax,.05);ys=np.arange(math.ceil(ymin*20)/20,ymax,.05)
        xx,yy=np.meshgrid(xs,ys);x=xx.ravel();y=yy.ravel()
        valid=sh.contains_xy(poly,x,y)&~sh.intersects_xy(avoid,x,y)&((x-100)**2+(y-100)**2<34.15**2)
        good=np.flatnonzero(valid)
        if not len(good):failed.append({'layer':b.GetLayerName(layer),'area':poly.area,'bounds':poly.bounds});continue
        target=poly.representative_point();k=min(good,key=lambda i:(x[i]-target.x)**2+(y[i]-target.y)**2)
        pos=float(x[k]),float(y[k]);v=p.PCB_VIA(b);v.SetPosition(r.vec(pos));v.SetWidth(p.FromMM(.4));v.SetDrill(p.FromMM(.2));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(b.FindNet('GND').GetNetCode());b.Add(v)
        added.append(pos);anchor=unary_union([anchor,Point(pos).buffer(.22)]);avoid=unary_union([avoid,Point(pos).buffer(.455)])
p.SaveBoard(str(r.path),b)
(r.W/'ground-stitch.json').write_text(json.dumps({'vias_added':added,'islands_without_via_space':failed},indent=2)+'\n')
print('Ground stitching:',len(added),'vias;',len(failed),'islands without free via space',flush=True)
