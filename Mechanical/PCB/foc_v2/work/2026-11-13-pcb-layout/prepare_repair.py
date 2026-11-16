import sys
import pcbnew as p
from pathlib import Path
from shapely.geometry import Point,LineString
import math
import sexpdata as sx,uuid
W=Path(__file__).resolve().parent;q=W/'candidate/foc_v2.kicad_pcb';b=p.LoadBoard(str(q));mm=p.FromMM
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
holes=[xy(f.GetPosition()) for f in b.GetFootprints() if f.GetReference().startswith('H')]
removed=[]
for t in list(b.GetTracks()):
 if isinstance(t,p.PCB_VIA):g=Point(xy(t.GetPosition())).buffer(p.ToMM(t.GetWidth(p.F_Cu))/2)
 elif t.GetLayer() in [p.F_Cu,p.B_Cu]:g=LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2)
 else:continue
 if any(g.distance(Point(c))<3.01 for c in holes):
  assert isinstance(t,p.PCB_VIA) or t.GetWidth()<mm(.8),'Critical power path intersects screw head'
  removed.append((t.GetNetname(),t.m_Uuid.AsString()))
data=sx.loads(q.read_text());drop={u for _,u in removed}
def sub(n,k):return next((a for a in n if isinstance(a,list) and a and str(a[0])==k),None)
data[:]=[n for n in data if not(isinstance(n,list) and n and str(n[0]) in ['segment','via'] and sub(n,'uuid') and sub(n,'uuid')[1] in drop)]
for n in data:
 if isinstance(n,list) and n and str(n[0])=='segment' and float(sub(n,'width')[1])<.15:sub(n,'width')[1]=.15
for centre in holes:
 for layer in [p.F_Cu,p.B_Cu]:
  pts=[]
  for i in range(64):
   a=2*math.pi*i/64;pts.append([sx.Symbol('xy'),round(centre[0]+3*math.cos(a),6),round(centre[1]+3*math.sin(a),6)])
  text=f'(zone (net 0) (net_name "") (layer "{b.GetLayerName(layer)}") (uuid "{uuid.uuid4()}") (name "M2.5 screw head clearance") (hatch edge 0.5) (keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) (footprints allowed)))'
  z=sx.loads(text);z.append([sx.Symbol('polygon'),[sx.Symbol('pts'),*pts]]);data.append(z)
q.write_text(sx.dumps(data)+'\n');print('Protected four screw-head regions; removed',len(removed),'signal/auxiliary copper items for rerouting.')
