import pcbnew as p
from pathlib import Path
W=Path(__file__).resolve().parent;OUT=W/'candidate';mm=p.FromMM
b=p.LoadBoard(str(OUT/'foc_v2.kicad_pcb'))
def vec(a):return p.VECTOR2I(mm(a[0]),mm(a[1]))
def route(net,pts,width,layer):
 for a,z in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(vec(a));t.SetEnd(vec(z));t.SetWidth(mm(width));t.SetLayer(layer);t.SetNetCode(b.FindNet(net).GetNetCode());t.SetLocked(True);b.Add(t)
def via(net,x,y,dia=.8,drill=.4):
 v=p.PCB_VIA(b);v.SetPosition(vec((x,y)));v.SetWidth(mm(dia));v.SetDrill(mm(drill));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(b.FindNet(net).GetNetCode());v.SetLocked(True);b.Add(v)
via('VS',103.5,105.8,.6,.3)
route('VS',[(103.5875,107.8),(103.5,105.8)],.2,p.F_Cu)
route('VS',[(103.5,105.8),(104.8,105.8),(104.8,97),(108,94.5),(113,92.5)],.2,p.In2_Cu)
for x in [120.2,121.2,122.2]:
 for y in [106.5,107.5,108.5]:via('VS',x,y)
route('VS',[(119.05,111.6),(121.2,107.5)],2.4,p.F_Cu)
route('VS',[(121.2,107.5),(125.5,104.5),(127,97.08)],2.4,p.In2_Cu)
for x in [126.6,127.6,128.6]:
 for y in [112.4,113.4,114.4]:via('GND',x,y)
route('GND',[(124.95,111.6),(127.6,113.4)],3,p.F_Cu)
for t in b.GetTracks():t.SetLocked(True)
b.BuildConnectivity();p.SaveBoard(str(OUT/'foc_v2.kicad_pcb'),b)
print('Bus divider and TVS connected; all power, ground-return and bypass routes fixed.')
