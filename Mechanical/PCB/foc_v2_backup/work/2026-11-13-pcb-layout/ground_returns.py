import pcbnew as p
from pathlib import Path
W=Path(__file__).resolve().parent;OUT=W/'candidate';mm=p.FromMM
b=p.LoadBoard(str(W/'power-routed.kicad_pcb'));net=b.FindNet('GND').GetNetCode()
def v(a):return p.VECTOR2I(mm(a[0]),mm(a[1]))
def route(points,width):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(v(a));t.SetEnd(v(z));t.SetWidth(mm(width));t.SetLayer(p.F_Cu);t.SetNetCode(net);t.SetLocked(True);b.Add(t)
for xs,ys in [([83.2,84.3,85.4],[113.5,114.6,115.7]),([115.2,116.3,117.4],[74.9,76,77.1]),([106.5,107.5,108.5],[98.5,99.5,100.5])]:
 for x in xs:
  for y in ys:
   a=p.PCB_VIA(b);a.SetPosition(v((x,y)));a.SetWidth(mm(.8));a.SetDrill(mm(.4));a.SetViaType(p.VIATYPE_THROUGH);a.SetLayerPair(p.F_Cu,p.B_Cu);a.SetNetCode(net);a.SetLocked(True);b.Add(a)
route([(84.9625,111),(84.9625,112.9)],1.8);route([(84.9625,112.9),(84.3,114.6)],2.7)
route([(113.4625,77.5),(115,77.5)],1.8);route([(115,77.5),(116.3,76)],2.7)
route([(108.2375,103.5),(108.2375,101.2)],1.8);route([(108.2375,101.2),(107.5,99.5)],2.7)
b.BuildConnectivity();p.SaveBoard(str(OUT/'foc_v2.kicad_pcb'),b)
print('Three high-current ground returns: 27 additional parallel 0.4-mm vias.')
