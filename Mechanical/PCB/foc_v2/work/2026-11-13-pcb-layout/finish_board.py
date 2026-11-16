"""Apply fabrication notes and assembly markings after routing is complete."""
from pathlib import Path
import sexpdata as sx
import pcbnew as p
import xml.etree.ElementTree as ET
import json,csv
W=Path(__file__).resolve().parent
q=W/'candidate/foc_v2.kicad_pcb'
S=sx.Symbol
def sub(n,k):return next((a for a in n if isinstance(a,list) and a and str(a[0])==k),None)
data=sx.loads(q.read_text());setup=sub(data,'setup')
managed={'U','V','W','SWD','+24V','GND','MA730','FOC 24V / 10A pk','D70  4x2.7 PCD26','2oz Cu  4 layers  1.6mm','VIPPO: resin fill + copper cap vias in VIPPO_REQUIRED.csv'}
data[:]=[a for a in data if not(isinstance(a,list) and len(a)>1 and str(a[0])=='gr_text' and a[1] in managed)]
for node in data:
    if not(isinstance(node,list) and node and str(node[0])=='footprint'):continue
    ref=next((a[2] for a in node if isinstance(a,list) and len(a)>2 and str(a[0])=='property' and a[1]=='Reference'),None)
    if ref=='U2':
        for a in node:
            if isinstance(a,list) and a and str(a[0])=='model':a[1]=a[1].replace('EP1.75x1.75mm.step','EP1.7x1.7mm.step')
setup[:]=[a for a in setup if not(isinstance(a,list) and a and str(a[0])=='stackup')]
stack=[S('stackup')]
def layer(name,kind,thickness=None,dielectric=False):
    a=[S('layer'),name,[S('type'),kind]]
    if thickness is not None:a.append([S('thickness'),thickness])
    if dielectric:a.extend([[S('material'),'FR4'],[S('epsilon_r'),4.5],[S('loss_tangent'),.02]])
    stack.append(a)
layer('F.SilkS','Top Silk Screen')
layer('F.Paste','Top Solder Paste')
layer('F.Mask','Top Solder Mask',.01)
layer('F.Cu','copper',.07)
layer('dielectric 1','prepreg',.2,True)
layer('In1.Cu','copper',.07)
layer('dielectric 2','core',.9,True)
layer('In2.Cu','copper',.07)
layer('dielectric 3','prepreg',.2,True)
layer('B.Cu','copper',.07)
layer('B.Mask','Bottom Solder Mask',.01)
layer('B.Paste','Bottom Solder Paste')
layer('B.SilkS','Bottom Silk Screen')
stack.extend([[S('copper_finish'),'ENIG'],[S('dielectric_constraints'),S('no')],[S('edge_connector'),S('no')],[S('castellated_pads'),S('no')],[S('edge_plating'),S('no')]])
setup.append(stack);q.write_text(sx.dumps(data)+'\n')
b=p.LoadBoard(str(q))
parts={a.get('ref'):a for a in ET.parse(W/'final.net.xml').getroot().findall('./components/comp')}
for f in b.GetFootprints():
    source=parts.get(f.GetReference())
    if source is not None:
        for field in source.findall('./fields/field'):
            if field.get('name') not in ['Reference','Value','Footprint']:f.SetField(field.get('name'),field.text or '')
    if f.GetReference() in ['C10','C11','D4','C12','C13','C16','C17']:
        for field in f.GetFields():
            if 'LCSC' in field.GetName().upper():field.SetText('')
    for field in f.GetFields():
        if field.GetName() not in ['Reference','Value']:field.SetVisible(False)
for z in b.Zones():
    if z.GetZoneName()=='Continuous ground reference':z.SetZoneName('GND reference pour')
def label(text,x,y,size,layer):
    t=p.PCB_TEXT(b);t.SetText(text);t.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));t.SetTextSize(p.VECTOR2I(p.FromMM(size),p.FromMM(size)));t.SetTextThickness(p.FromMM(.15));t.SetLayer(layer);t.SetMirrored(layer==p.B_SilkS);b.Add(t)
label('U',71.7,93,1,p.F_SilkS)
label('V',101,67.4,1,p.F_SilkS)
label('W',128,81,1,p.F_SilkS)
label('SWD',89,69.2,.8,p.F_SilkS)
label('+24V',112.5,113.4,.8,p.B_SilkS)
label('GND',117.5,113.4,.8,p.B_SilkS)
label('MA730',100,105.9,.8,p.B_SilkS)
label('FOC 24V / 10A pk',100,119,1,p.B_SilkS)
label('D70  4x2.7 PCD26',100,121.5,.8,p.B_SilkS)
label('2oz Cu  4 layers  1.6mm',100,124,.8,p.B_SilkS)
label('VIPPO: resin fill + copper cap vias in VIPPO_REQUIRED.csv',100,142,1,p.Cmts_User)
b.BuildConnectivity();p.SaveBoard(str(q),b)
assert len([f for f in b.GetFootprints() if f.GetReference().startswith('H') and f.GetReference()[1:].isdigit()])==4
sensor=next(f for f in b.GetFootprints() if f.GetReference()=='U2')
assert sensor.IsFlipped() and sensor.GetPosition()==p.VECTOR2I(p.FromMM(100),p.FromMM(100))
previous=json.loads((W/'pad-escape-vias.json').read_text());rows=[]
for v in b.GetTracks():
    if not isinstance(v,p.PCB_VIA) or v.GetFillingMode()!=p.FILLING_MODE_FILLED:continue
    assert v.GetCappingMode()==p.CAPPING_MODE_CAPPED
    x,y=p.ToMM(v.GetPosition().x),p.ToMM(v.GetPosition().y)
    match=next((a for a in previous if abs(a['x_mm']-x)<.001 and abs(a['y_mm']-y)<.001 and a['net']==v.GetNetname()),{})
    rows.append({'pad':match.get('pad',''),'net':v.GetNetname(),'x_mm':round(x,6),'y_mm':round(y,6),'via_diameter_mm':p.ToMM(v.GetWidth(p.F_Cu)),'finished_hole_mm':p.ToMM(v.GetDrill()),'process':'RESIN FILLED AND COPPER CAPPED'})
with (W/'VIPPO_REQUIRED.csv').open('w') as out:
    writer=csv.DictWriter(out,fieldnames=['pad','net','x_mm','y_mm','via_diameter_mm','finished_hole_mm','process']);writer.writeheader();writer.writerows(rows)
print('Applied 4-layer 1.6-mm / 70-um copper stack and assembly markings')
