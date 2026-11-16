"""Route the fixed high-current paths before routing small signals."""
import pcbnew as p
from pathlib import Path
W=Path(__file__).resolve().parent;OUT=W/'candidate'
b=p.LoadBoard(str(OUT/'foc_v2.kicad_pcb'))
mm=p.FromMM
def vec(a):return p.VECTOR2I(mm(a[0]),mm(a[1]))
def code(net):return b.FindNet(net).GetNetCode()
def route(net,points,width,layer=p.F_Cu):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(vec(a));t.SetEnd(vec(z));t.SetWidth(mm(width));t.SetLayer(layer);t.SetNetCode(code(net));t.SetLocked(True);b.Add(t)
def vias(net,xs,ys):
 for x in xs:
  for y in ys:
   v=p.PCB_VIA(b);v.SetPosition(vec((x,y)));v.SetWidth(mm(.8));v.SetDrill(mm(.4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(code(net));v.SetLocked(True);b.Add(v)

# Three compact switching cells, with the source leads joined before widening.
for net,xs,y,tip in [('/GATE_DRV/SHA',[78.595,81.135],96.9,(80,100.45)),('/GATE_DRV/SHC',[116.095,118.635],97.9,(117.5,101.45))]:
 route(net,[(xs[0],y),(xs[1],y)],.8)
 route(net,[(tip[0],y),tip],3)
route('/GATE_DRV/SHB',[(97.9,76.865),(97.9,79.405)],.8)
route('/GATE_DRV/SHB',[(97.9,78.2),(101.45,78.2)],3)
route('/GATE_DRV/SHA',[(80,99.2),(75,99.2),(75,93)],3)
route('/GATE_DRV/SHB',[(101,78.2),(101,70.5)],2.5)

# Source-to-shunt paths taper only at the resistor's terminal.
route('/GATE_DRV/SPA',[(78.595,104.4),(81.135,104.4)],.8)
route('/GATE_DRV/SPA',[(79.0375,104.4),(79.0375,109)],2.8)
route('/GATE_DRV/SPA',[(79.0375,109),(79.0375,111)],1.8)
route('/GATE_DRV/SPB',[(105.4,76.865),(105.4,79.405)],.8)
route('/GATE_DRV/SPB',[(105.4,78.2),(106.5,77.5)],2.5)
route('/GATE_DRV/SPB',[(106.5,77.5),(107.5375,77.5)],1.8)
route('/GATE_DRV/SPC',[(116.095,105.4),(118.635,105.4)],.8)
route('/GATE_DRV/SPC',[(117.5,105.8),(114.1625,105.8)],2.8)
route('/GATE_DRV/SPC',[(114.1625,105.8),(114.1625,103.5)],1.8)

# Phase C crosses to the rear using nine parallel 0.4-mm drilled vias.
vias('/GATE_DRV/SHC',[121.1,122.1,123.1],[100.2,101.2,102.2])
route('/GATE_DRV/SHC',[(117.5,101.2),(123.1,101.2)],3)
route('/GATE_DRV/SHC',[(122.1,101.2),(123.8,101.2),(123.8,83),(125,81)],3,p.B_Cu)

# Vias sit outside the MOSFET solder pads, avoiding via-in-pad solder loss.
for xs,ys,drain,hub in [([84,85,86],[90.5,91.5,92.5],(80.5,92.95),(85,91.5)),([89.5,90.5,91.5],[79.5,80.5,81.5],(93.95,77.5),(90.5,80.5)),([113,114,115],[90.5,91.5,92.5],(118,93.95),(114,91.5))]:
 vias('VS',xs,ys);route('VS',[drain,hub],3)
route('VS',[(81,84),(85,91.5)],3,p.In2_Cu)
route('VS',[(81,84),(86,79),(93.95,77.5),(115.5,86)],3,p.In2_Cu)
route('VS',[(93.95,77.5),(90.5,80.5)],3,p.In2_Cu)
route('VS',[(115.5,86),(114,91.5)],3,p.In2_Cu)
route('VS',[(127,97.08),(130.4,97.08),(130,90.5),(115.5,90.5),(115.5,86)],3,p.In2_Cu)
raw=next(pad.GetNetname() for f in b.GetFootprints() if f.GetReference()=='F1' for pad in f.Pads() if pad.GetNumber()=='1')
route(raw,[(127,107),(130.4,107)],3,p.B_Cu)
route(raw,[(127,107),(125,111),(114,111),(112.5,116.5)],3,p.B_Cu)

b.BuildConnectivity();p.SaveBoard(str(OUT/'foc_v2.kicad_pcb'),b)
p.SaveBoard(str(W/'power-routed.kicad_pcb'),b)
assert all(t.GetWidth(p.F_Cu)>=mm(.8) if isinstance(t,p.PCB_VIA) else t.GetWidth()>=mm(.8) for t in b.GetTracks())
print('Power paths fixed:',len(list(b.GetTracks())),'segments/vias. Kelvin pickups remain separate sense nets.')
