"""Keep the 3-mm input bus clear of the LDO ground escape."""
import pcbnew as p, sexpdata as sx
from pathlib import Path
from shapely.geometry import Point,LineString
from shapely.ops import unary_union
W=Path(__file__).resolve().parent;q=W/'candidate/foc_v2.kicad_pcb';b=p.LoadBoard(str(q));mm=p.FromMM
net=next(a.GetNetname() for f in b.GetFootprints() if f.GetReference()=='J11' for a in f.Pads() if a.GetNumber()=='1')
points=[(112.5,116.5),(112.5,120),(121.5,120),(124.4,115),(124.4,109),(127,107),(130.4,107)]
new=LineString(points).buffer(1.5);drop=set()
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
def polys(s):
    from shapely.geometry import Polygon
    return unary_union([Polygon([xy(s.COutline(i).CPoint(j)) for j in range(s.COutline(i).PointCount())]) for i in range(s.OutlineCount())])
for f in b.GetFootprints():
    for a in f.Pads():
        if a.GetNetname()==net or not a.IsOnLayer(p.B_Cu):continue
        s=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(s,p.B_Cu,0,mm(.001),p.ERROR_OUTSIDE);g=polys(s)
        if a.GetAttribute()==p.PAD_ATTRIB_NPTH:a.TransformHoleToPolygon(s,0,mm(.001),p.ERROR_OUTSIDE);g=polys(s)
        assert new.distance(g)>=.15-1e-6,('Input bus hits pad',f.GetReference(),a.GetNumber(),new.distance(g))
for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA):g=Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2);width=p.ToMM(t.GetWidth(p.F_Cu))
    elif t.GetLayer()==p.B_Cu:
        g=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2);width=p.ToMM(t.GetWidth())
    else:continue
    if t.GetNetname()==net:
        if not isinstance(t,p.PCB_VIA):drop.add(t.m_Uuid.AsString())
        continue
    if new.distance(g)<.15:
        assert width<.8,('Input bus hits fixed power',t.GetNetname(),new.distance(g))
        drop.add(t.m_Uuid.AsString())
data=sx.loads(q.read_text())
def sub(n,k):return next((a for a in n if isinstance(a,list) and a and str(a[0])==k),None)
data[:]=[a for a in data if not(isinstance(a,list) and a and str(a[0]) in ['segment','via'] and sub(a,'uuid') and sub(a,'uuid')[1] in drop)];q.write_text(sx.dumps(data)+'\n')
b=p.LoadBoard(str(q))
for a,z in zip(points,points[1:]):
    t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(mm(a[0]),mm(a[1])));t.SetEnd(p.VECTOR2I(mm(z[0]),mm(z[1])));t.SetWidth(mm(3));t.SetLayer(p.B_Cu);t.SetNetCode(b.FindNet(net).GetNetCode());t.SetLocked(True);b.Add(t)
p.SaveBoard(str(q),b);print('Input bus kept at 3 mm; copper objects moved/reconnected:',len(drop),flush=True)
