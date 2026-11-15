"""Build the four-layer motor-back PCB from the saved schematic netlist."""
import sys
sys.path.append('/usr/lib/python3/dist-packages')
import pcbnew as p
import math, json, copy, xml.etree.ElementTree as E
from pathlib import Path
from shapely.geometry import Point, Polygon, box, LineString
from shapely.ops import polygonize, unary_union

W=Path(__file__).resolve().parent
OUT=W/'candidate'
ROOT=W.parent.parent
mm=p.FromMM
def v(x,y):return p.VECTOR2I(mm(x),mm(y))
def xy(q):return (p.ToMM(q.x),p.ToMM(q.y))
source=E.parse(W/'kelvin.net.xml').getroot()
components={c.get('ref'):c for c in source.findall('./components/comp')}
board=p.BOARD();board.SetFileName(str(OUT/'foc_v2.kicad_pcb'));board.SetCopperLayerCount(4)
root_uuid='b5c0d4be-7ad7-4dae-8125-334a612efd8d'
networks={};pin_net={};pin_data={}
for n in source.findall('./nets/net'):
 ni=p.NETINFO_ITEM(board,n.get('name'));board.Add(ni);networks[n.get('name')]=ni
 for node in n.findall('node'):
  key=(node.get('ref'),node.get('pin'));assert key not in pin_net
  pin_net[key]=ni;pin_data[key]=node.attrib
fps={}
for ref,c in components.items():
 lib,name=c.findtext('footprint').split(':',1)
 f=p.FootprintLoad(str(OUT/'foc_v2.pretty') if lib=='foc_v2' else '/usr/share/kicad/footprints/'+lib+'.pretty',name);assert f,ref
 f.SetFPID(p.LIB_ID(lib,name));f.SetReference(ref);f.SetValue(c.findtext('value'))
 f.SetPath(p.KIID_PATH('/'+root_uuid+c.find('sheetpath').get('tstamps')+c.findtext('tstamps')))
 f.SetSheetname(c.find('sheetpath').get('names'));f.SetSheetfile({'/MCU/':'MCU.kicad_sch','/GATE_DRV/':'gatedrv.kicad_sch','/COMMUNICATION/':'communication.kicad_sch','/HALL/':'hall.kicad_sch'}[c.find('sheetpath').get('names')])
 for field in c.findall('./fields/field'):
  if field.get('name') not in ['Reference','Value','Footprint']:
   f.SetField(field.get('name'),field.text or '')
 for key,tag in [('Description','description'),('Datasheet','datasheet')]:
  if c.find(tag) is not None:f.SetField(key,c.findtext(tag) or '')
 excluded=any(x.get('name')=='exclude_from_bom' for x in c.findall('property'))
 attrs=f.GetAttributes() & ~p.FP_EXCLUDE_FROM_BOM
 if excluded:attrs|=p.FP_EXCLUDE_FROM_BOM
 f.SetAttributes(attrs)
 board.Add(f);fps[ref]=f
 for pad in f.Pads():
  key=(ref,pad.GetNumber())
  if key in pin_net:
   pad.SetNet(pin_net[key]);data=pin_data[key]
   if data.get('pinfunction'):pad.SetPinFunction(data['pinfunction'])
   if data.get('pintype'):pad.SetPinType(data['pintype'])
 f.Value().SetVisible(False);f.Reference().SetTextSize(v(.65,.65));f.Reference().SetTextThickness(mm(.10))
 for field in f.GetFields():
  if field.GetName() not in ['Reference','Value']:field.SetVisible(False)
 # Packing considers courtyards, never text bounding boxes.
 f.SetPosition(v(0,0))

def place(ref,x,y,angle=0,bottom=False):
 f=fps[ref];f.SetPosition(v(x,y))
 if bottom and not f.IsFlipped():f.Flip(f.GetPosition(),False)
 f.SetOrientationDegrees(angle)
 return f

anchors={
 'U2':(100,100,0,True), 'C14':(100,103.4,0,True), 'R61':(103.3,100,90,True),
 'U1':(100,117.8,0), 'IC1':(100,94,0),
 'Q1':(80.5,94,90),'Q2':(80.5,101.5,90),'R47':(82,111,0),
 'Q3':(95,77.5,180),'Q4':(102.5,77.5,180),'R48':(110.5,77.5,0),
 'Q5':(118,95,90),'Q6':(118,102.5,90),'R49':(111.2,103.5,180),
 'C_BULK1':(81,84,0),'C63':(115.5,86,0),
 'F1':(127,107,90),'J11':(112.5,116.5,180),'J7':(100,130,0),
 'J8':(69,100,270),'J9':(74,115,270),'J10':(83.5,72,90),
 'J1':(75,93,0),'J2':(101,70.5,0),'J3':(125,81,0),'R3':(98.2,73.5,0),
 'L1':(100,86,0),
 'NT1':(80.45,111,180),'NT2':(83.55,111,0),
 'NT3':(108.95,77.5,180),'NT4':(112.05,77.5,0),
 'NT5':(112.75,103.5,0),'NT6':(109.65,103.5,180),
}
for ref,args in anchors.items():place(ref,*args)

# Four non-plated M2.5 clearance holes on the requested 26-mm pitch circle.
for i,angle in enumerate([45,135,225,315],1):
 x=100+13*math.cos(math.radians(angle));y=100+13*math.sin(math.radians(angle))
 f=p.FootprintLoad('/usr/share/kicad/footprints/MountingHole.pretty','MountingHole_2.7mm_M2.5')
 f.SetReference('H'+str(i));f.SetValue('M2.5 PCD26');f.SetAttributes(p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
 board.Add(f);f.SetPosition(v(x,y));fps['H'+str(i)]=f
 f.Value().SetVisible(False);f.Reference().SetTextSize(v(.7,.7));f.Reference().SetTextThickness(mm(.1))

def courtyard(f):
 if f.GetReference().startswith('NT'):return Polygon()
 f.BuildCourtyardCaches();s=f.GetCourtyard(p.B_Cu if f.IsFlipped() else p.F_Cu)
 polys=[]
 for i in range(s.OutlineCount()):
  chain=s.COutline(i);pts=[xy(chain.CPoint(j)) for j in range(chain.PointCount())]
  if len(pts)>2:polys.append(Polygon(pts))
 if polys:return unary_union(polys)
 a=f.GetBoundingBox(False,False)
 return box(p.ToMM(a.GetX()),p.ToMM(a.GetY()),p.ToMM(a.GetRight()),p.ToMM(a.GetBottom()))

disk=Point(100,100).buffer(34.8,quad_segs=96)
hole_clear=[Point(xy(f.GetPosition())).buffer(3.0,quad_segs=32) for r,f in fps.items() if r.startswith('H')]
placed=set(anchors)|{r for r in fps if r.startswith('H')}
geoms={r:courtyard(fps[r]) for r in placed}

def overlaps(ref,g):
 bottom=fps[ref].IsFlipped()
 expanded=g.buffer(.10)
 for r in placed:
  if r==ref:continue
  # Through-hole hardware occupies both faces.
  if fps[r].IsFlipped()!=bottom and not r.startswith('H') and r not in ['J11','F1','C_BULK1','C63','J10','J1','J2','J3']:continue
  if expanded.intersects(geoms[r]):return r
 return None

# Place small critical components before the freely movable bias resistors.
targets={
 'C19':(94.7,92.2),'C18':(94.4,94.6),'C12':(94.2,88.3),'C13':(97,88.8),'C17':(94.2,96.6),
 'C15':(98,89.5),'D4':(103.5,88.7),'C16':(105,85),'R6':(95,89),'R9':(93,89),
 'C20':(104.8,90.7),'C21':(105,95.8),
 'C_BUS1':(76.8,89),'C_BUS2':(89.8,75.9),'C_BUS3':(122.8,90.7),
 'R1':(84.7,96.1),'R2':(84.7,103.5),'R3':(98,74.3),'R4':(105.5,74.3),'R5':(122.2,97),'R7':(122.2,104.5),
 'R55':(85,98),'R56':(85,101),'R57':(98.1,81.2),'R58':(105.5,81),'R59':(114.2,96.5),'R60':(114.2,103.5),
 'C1':(87.2,105.8),'C2':(111,80.4),'C3':(111.2,100.5),
 'Y1':(89.5,116.7),'C8':(88,115.2),'C9':(89.7,115.4),'C7':(91.5,117.1),'R32':(92,116),
 'C50':(97.25,125),'C51':(104,125),'C52':(108,114),'C4':(96.25,110.3),'C5':(92,120.5),'C6':(92,122.5),'FB1':(91,122.5),
 'C10':(106,124.5),'C11':(108,115),'C53':(92,114.05),
 'U10':(111,114.8),'C57':(112.6,112.7),'C58':(108.5,115.5),
 'U8':(100,123.5),'R40':(96,127),'R41':(94.5,127),'C59':(96,130),'Q7':(108,128),
 'U9':(78.5,115),'C60':(79,117.5),'C61':(79.5,118),'R45':(79,120),'R46':(79,122),'C62':(81,123),'JP1':(81,125),
 'R37':(92,118.8),'R38':(94,123),'R39':(95.5,124),'C54':(92,120),'C55':(95,124.5),'C56':(96,125),
 'R53':(108.5,111.8),'R54':(107.5,113),'C64':(107.6,114.5),
 'D6':(122,112),'TP1':(105,86.7),'TP2':(96.5,101.5),'TP3':(96.5,98.5),
}

def pin_neighbours(ref):
 ns={net.GetNetname() for (r,_),net in pin_net.items() if r==ref and net.GetNetname() not in ['GND','+3V3','+5V','VS']}
 out=[]
 for (r,num),net in pin_net.items():
  if r in placed and net.GetNetname() in ns and r!=ref:
   out.append(xy(fps[r].GetPosition()))
 return out

def auto_place(ref):
 f=fps[ref];neighbours=pin_neighbours(ref)
 if ref in targets:tx,ty=targets[ref]
 elif neighbours:tx=sum(x for x,y in neighbours)/len(neighbours);ty=sum(y for x,y in neighbours)/len(neighbours)
 else:
  sheet=components[ref].find('sheetpath').get('names');tx,ty={'/MCU/':(100,111),'/GATE_DRV/':(102,93),'/COMMUNICATION/':(87,114),'/HALL/':(100,100)}[sheet]
 choices=[]
 for dx in range(-40,41):
  for dy in range(-40,41):
   d=dx*dx+dy*dy
   if d<=1600:choices.append((d,tx+dx*.4,ty+dy*.4))
 choices.sort()
 for _,x,y in choices:
  for a in [0,90,180,270]:
   f.SetPosition(v(round(x,3),round(y,3)));f.SetOrientationDegrees(a);g=courtyard(f)
   if not disk.covers(g):continue
   if any(g.intersects(h) for h in hole_clear):continue
   if overlaps(ref,g):continue
   # Keep all front components clear of the rotor magnet centre.
   if g.intersects(Point(100,100).buffer(3.3)) and ref not in ['TP2','TP3']:continue
   placed.add(ref);geoms[ref]=g
   return
 p.SaveBoard(str(OUT/'partial.kicad_pcb'),board)
 raise RuntimeError('No valid placement: '+ref)

for r in ['D6','U8','U9','U10','Y1']+[r for r in targets if r not in ['D6','U8','U9','U10','Y1']]:
 if r not in placed:auto_place(r)
for r in fps:
 if r not in placed:auto_place(r)

# A true circular outline; keep the sensor's package centre exactly on its axis.
edge=p.PCB_SHAPE();edge.SetShape(p.SHAPE_T_CIRCLE);edge.SetCenter(v(100,100));edge.SetEnd(v(135,100));edge.SetLayer(p.Edge_Cuts);edge.SetWidth(mm(.05));board.Add(edge)
for f in fps.values():
 f.Reference().SetLayer(p.B_Fab if f.IsFlipped() else p.F_Fab);f.Reference().SetTextSize(v(1,1));f.Reference().SetTextThickness(mm(.15))
 f.SetLocked(True)
board.BuildConnectivity();p.SaveBoard(str(OUT/'foc_v2.kicad_pcb'),board)
placement={r:{'x':xy(f.GetPosition())[0],'y':xy(f.GetPosition())[1],'rotation':f.GetOrientationDegrees(),'side':'B' if f.IsFlipped() else 'F'} for r,f in fps.items()}
(W/'placement.json').write_text(json.dumps(placement,indent=2)+'\n')
conflicts=[]
for r in placed:
 bad=overlaps(r,geoms[r])
 if bad:conflicts.append((r,bad))
assert len(fps)==len(components)+4
assert xy(fps['U2'].GetPosition())==(100.,100.) and fps['U2'].IsFlipped()
print('Placed',len(fps),'footprints; mechanical diameter 70 mm; 4 x 2.7 mm on PCD26; overlaps:',conflicts)
(W/'placement-conflicts.json').write_text(json.dumps(conflicts,indent=2)+'\n')
