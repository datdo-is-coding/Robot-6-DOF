import pcbnew as p
from pathlib import Path
import json,sys
W=Path(__file__).resolve().parent;b=p.LoadBoard(str(W/'candidate/foc_v2.kicad_pcb'));b.BuildConnectivity();connectivity=b.GetConnectivity()
report=json.loads(Path(sys.argv[1]).read_text());objects={}
layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]
for f in b.GetFootprints():
 for a in f.Pads():objects[a.m_Uuid.AsString()]=a
for a in b.GetTracks():objects[a.m_Uuid.AsString()]=a
for a in b.Zones():objects[a.m_Uuid.AsString()]=a
pairs=[]
for r in report['unconnected_items']:
 ends=[]
 for index,item in enumerate(r['items']):
  o=objects.get(item['uuid']);assert o is not None,item
  pos=[item['pos']['x'],item['pos']['y']]
  if not isinstance(o,p.ZONE):
   other=r['items'][1-index]['pos']
   # KiCad returns connected vias as PCB_TRACK proxies; recover their concrete types.
   members=[objects.get(a.m_Uuid.AsString(),a) for a in [o,*connectivity.GetConnectedItems(o)]]
   anchors=[a for a in members if a.GetNetname()==o.GetNetname() and (isinstance(a,p.PCB_VIA) or isinstance(a,p.PAD) and a.GetAttribute()==p.PAD_ATTRIB_PTH)]
   if anchors:
    o=min(anchors,key=lambda a:(p.ToMM(a.GetPosition().x)-other['x'])**2+(p.ToMM(a.GetPosition().y)-other['y'])**2)
    pos=[p.ToMM(o.GetPosition().x),p.ToMM(o.GetPosition().y)]
  if isinstance(o,p.PCB_VIA):ls=['F.Cu','In1.Cu','In2.Cu','B.Cu']
  elif isinstance(o,p.PAD):ls=[b.GetLayerName(l) for l in layers if o.IsOnLayer(l)]
  elif isinstance(o,p.ZONE) and o.GetLayer()==p.In1_Cu:ls=['F.Cu','B.Cu']
  else:ls=[o.GetLayerName()]
  ends.append({'pos':pos,'layers':ls,'net':o.GetNetname(),'kind':type(o).__name__})
 assert len(ends)==2 and ends[0]['net']==ends[1]['net']
 pairs.append({'a':ends[0],'b':ends[1]})
(W/'pairs.json').write_text(json.dumps(pairs,indent=2)+'\n');print('Unconnected pairs:',len(pairs))
