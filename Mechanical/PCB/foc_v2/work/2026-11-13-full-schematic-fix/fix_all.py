import copy,hashlib,json,math,re
from pathlib import Path
import sexpdata as sx
S=sx.Symbol
W=Path(__file__).resolve().parent; OUT=W/'candidate'
NAMES=['foc_v2.kicad_sch','MCU.kicad_sch','gatedrv.kicad_sch','communication.kicad_sch','hall.kicad_sch']
A={n:sx.loads((W/'before'/n).read_text()) for n in NAMES}

def children(n,k):return [x for x in n if isinstance(x,list) and x and str(x[0])==k]
def one(n,k):
 q=children(n,k);assert len(q)==1,(k,len(q));return q[0]
def pos(n):return tuple(float(x) for x in one(n,'at')[1:3])
def props(n):return {x[1]:x[2] for x in children(n,'property')}
def prop(n,k,v):
 q=[p for p in children(n,'property') if p[1]==k]
 if q:q[0][2]=v
 else:n.append([S('property'),k,v,[S('at'),*pos(n),0],[S('effects'),[S('font'),[S('size'),1,1]],[S('hide'),S('yes')]]])
def uid():
 import uuid
 return str(uuid.uuid4())
def grid(v):return round(round(float(v)/1.27)*1.27,4)
def pretty(n,depth=0):
 if not isinstance(n,list):return sx.dumps(n)
 if not any(isinstance(x,list) for x in n):return sx.dumps(n)
 i=next(j for j,x in enumerate(n) if isinstance(x,list))
 start='('+' '.join(sx.dumps(x) for x in n[:i])
 return start+'\n'+'\n'.join('\t'*(depth+1)+pretty(x,depth+1) for x in n[i:])+'\n'+'\t'*depth+')'
LIBCACHE={}
def extract_symbol(lib,part):
 path=Path('/usr/share/kicad/symbols')/(lib+'.kicad_sym');text=path.read_text()
 start=text.index('\t(symbol '+sx.dumps(part)+'\n')+1
 depth=0;quote=False;escape=False
 for i in range(start,len(text)):
  c=text[i]
  if quote:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':quote=False
  elif c=='"':quote=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:return sx.loads(text[start:i+1])
 raise ValueError(part)
def library(libid):
 if libid in LIBCACHE:return copy.deepcopy(LIBCACHE[libid])
 lib,part=libid.split(':',1);node=extract_symbol(lib,part)
 ext=children(node,'extends')
 if ext:
  base=library(lib+':'+ext[0][1]);old=base[1].split(':',1)[-1]
  for unit in children(base,'symbol'):unit[1]=str(unit[1]).replace(old+'_',part+'_',1)
  for p in children(node,'property'):
   base[:]=[x for x in base if not(isinstance(x,list) and str(x[0])=='property' and x[1]==p[1])]
   base.append(p)
  node=base
 node[1]=libid;LIBCACHE[libid]=copy.deepcopy(node);return node
ROOTID=one(A['foc_v2.kicad_sch'],'uuid')[1]
SHEETIDS={props(x)['Sheetfile']:one(x,'uuid')[1] for x in children(A['foc_v2.kicad_sch'],'sheet')}
used=set()
for root in A.values():
 for x in children(root,'symbol'):used.add(props(x).get('Reference',''))
def ref(prefix):
 vals=[int(r[len(prefix):]) for r in used if r.startswith(prefix) and r[len(prefix):].isdigit()]
 result=prefix+str(max(vals,default=0)+1);used.add(result);return result
pwr_count=1000
class Sheet:
 def __init__(self,name):self.name=name;self.r=A[name]
 def symbols(self):return children(self.r,'symbol')
 def sym(self,r):return next(x for x in self.symbols() if props(x).get('Reference')==r)
 def remove(self,x):self.r.remove(x)
 def cache(self,libid,definition=None):
  lib=one(self.r,'lib_symbols')
  if not any(x[1]==libid for x in children(lib,'symbol')):lib.append(definition or library(libid))
 def pins(self,n):
  libid=one(n,'lib_id')[1];lib=next(x for x in children(one(self.r,'lib_symbols'),'symbol') if x[1]==libid)
  x,y,angle=one(n,'at')[1:];theta=math.radians(angle);result={}
  for unit in children(lib,'symbol'):
   for p in children(unit,'pin'):
    px,py=one(p,'at')[1:3]
    result[str(one(p,'number')[1])]=(round(x+px*math.cos(theta)-py*math.sin(theta),4),round(y-px*math.sin(theta)-py*math.cos(theta),4))
  return result
 def wire(self,a,b):
  a=tuple(round(x,4) for x in a);b=tuple(round(x,4) for x in b)
  if a==b:return
  assert a[0]==b[0] or a[1]==b[1],(a,b)
  self.r.append([S('wire'),[S('pts'),[S('xy'),*a],[S('xy'),*b]],[S('stroke'),[S('width'),0],[S('type'),S('default')]],[S('uuid'),uid()]])
 def junction(self,p):self.r.append([S('junction'),[S('at'),*p],[S('diameter'),0],[S('color'),0,0,0,0],[S('uuid'),uid()]])
 def label(self,name,p,angle=0,kind='label',shape='input'):
  n=[S(kind),name]
  if kind=='hierarchical_label':n.append([S('shape'),S(shape)])
  n.extend([[S('at'),*p,angle],[S('effects'),[S('font'),[S('size'),1.0,1.0]],[S('justify'),S('right' if angle==180 else 'left'),S('bottom')]],[S('uuid'),uid()]])
  self.r.append(n);return n
 def nc(self,p):self.r.append([S('no_connect'),[S('at'),*p],[S('uuid'),uid()]])
 def note(self,text,p):self.r.append([S('text'),text,[S('at'),*p,0],[S('effects'),[S('font'),[S('size'),1.27,1.27]],[S('justify'),S('left')]],[S('uuid'),uid()]])
 def add(self,libid,r,value,p,angle=0,fp=None):
  self.cache(libid);lib=next(x for x in children(one(self.r,'lib_symbols'),'symbol') if x[1]==libid)
  defaults=props(lib);x,y=p
  n=[S('symbol'),[S('lib_id'),libid],[S('at'),x,y,angle],[S('unit'),1],[S('in_bom'),S('yes')],[S('on_board'),S('yes')],[S('dnp'),S('no')],[S('uuid'),uid()]]
  for key,val,px,py,hide in [('Reference',r,x+2.54,y-2.54,False),('Value',value,x+2.54,y,False),('Footprint',fp if fp is not None else defaults.get('Footprint',''),x,y,True),('Datasheet',defaults.get('Datasheet',''),x,y,True)]:
   effect=[S('effects'),[S('font'),[S('size'),1.0,1.0]],[S('justify'),S('left')]]
   if hide:effect.append([S('hide'),S('yes')])
   if key in ['Reference','Value']:
    template=next(a for a in children(lib,'property') if a[1]==key)
    local=one(template,'at');theta=math.radians(angle)
    px=round(x+local[1]*math.cos(theta)-local[2]*math.sin(theta),4)
    py=round(y-local[1]*math.sin(theta)-local[2]*math.cos(theta),4)
   if angle==90 and key in ['Reference','Value'] and libid in ['Device:R','Device:Fuse','Device:C']:
    px=x;py=y+(-5.08 if key=='Reference' else -2.54);effect=[S('effects'),[S('font'),[S('size'),1.0,1.0]]]
   elif key in ['Reference','Value'] and libid in ['Device:R','Device:C','Device:C_Polarized','Device:D_Zener','Jumper:SolderJumper_2_Open']:
    px=x+2.54;py=y+(-1.27 if key=='Reference' else 1.27)
   n.append([S('property'),key,val,[S('at'),round(px,4),round(py,4),angle if key in ['Reference','Value'] else 0],effect])
  for unit in children(lib,'symbol'):
   for pin in children(unit,'pin'):n.append([S('pin'),str(one(pin,'number')[1]),[S('uuid'),uid()]])
  n.append([S('instances'),[S('project'),'foc_v2',[S('path'),'/'+ROOTID+'/'+SHEETIDS[self.name],[S('reference'),r],[S('unit'),1]]]])
  self.r.append(n);return n
 def power(self,name,p):
  global pwr_count
  pwr_count+=1
  n=self.add('power:'+name,'#PWR'+str(pwr_count),name,p)
  one(n,'in_bom')[1]=S('yes')
  for a in children(n,'property'):
   if a[1]=='Reference':one(a,'effects').append([S('hide'),S('yes')])
  # Standard power symbols have their own orientation and text anchors.
  for a in children(n,'property'):
   if a[1]=='Value':one(a,'at')[1:3]=[p[0],p[1]+(3.81 if name=='GND' else -3.81)];one(a,'effects')[:]=[S('effects'),[S('font'),[S('size'),1,1]]]
  return n
 def tie(self,n,pin,name,delta=(-5.08,0),power=False):
  q=self.pins(n)[str(pin)];p=(round(q[0]+delta[0],4),round(q[1]+delta[1],4));self.wire(q,p)
  self.power(name,p) if power else self.label(name,p,180 if delta[0]<0 else 0)
  return p
 def erase_region(self,x1,y1,x2,y2,types):
  for n in list(self.r):
   if not isinstance(n,list) or str(n[0]) not in types:continue
   pts=[pos(n)] if children(n,'at') else [tuple(x[1:3]) for x in one(n,'pts')[1:]]
   if pts and all(x1<=x<=x2 and y1<=y<=y2 for x,y in pts):self.r.remove(n)
 def save(self):
  # Remove unused cached library definitions so ERC compares the actual symbols.
  ids={one(n,'lib_id')[1] for n in self.symbols()};lib=one(self.r,'lib_symbols')
  lib[:]=[lib[0]]+[n for n in children(lib,'symbol') if n[1] in ids]
  (OUT/self.name).write_text(pretty(self.r)+'\n')

RFP='Resistor_SMD:R_0603_1608Metric';CFP='Capacitor_SMD:C_0603_1608Metric'

def rename_symbol(n,new):
 old=props(n)['Reference'];prop(n,'Reference',new)
 def walk(v):
  if isinstance(v,list):
   if v and str(v[0])=='reference' and v[1]==old:v[1]=new
   for x in v:walk(x)
 walk(n)


def fix_mcu():
 m=Sheet('MCU.kicad_sch')
 for old in ['R1','R2','R3','R4','R5','C1','C2','C3']:
  rename_symbol(m.sym(old),ref(old[0]))
 for r in ['C10','C11']:prop(m.sym(r),'Value','2.2uF');prop(m.sym(r),'Voltage','6.3V');prop(m.sym(r),'Dielectric','X7R, low ESR')
 prop(m.sym('FB1'),'Value','600R@100MHz')
 prop(m.sym('Y1'),'Load capacitance','18pF');prop(m.sym('Y1'),'ESR','60R max')
 # VBAT is not an unused GPIO: tie it to VDD.
 p=m.pins(m.sym('U1'))['1']
 for n in list(children(m.r,'no_connect')):
  if pos(n)==p:m.remove(n)
 m.wire(p,(p[0],49.53));m.power('+3V3',(p[0],49.53))
 c=m.add('Device:C',ref('C'),'100nF',(53.34,54.61),fp=CFP);m.tie(c,'1','+3V3',(0,-2.54),True);m.tie(c,'2','GND',(0,2.54),True)
 # A five-pin SWD header includes target reference and reset.
 m.erase_region(198,25,240,48,{'symbol','wire','no_connect','label','junction'})
 j=m.add('Connector_Generic:Conn_01x05','J10','SWD',(220.98,35.56),fp='Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical')
 used.add('J10')
 for pin,name in [('1','+3V3'),('2','SWDIO'),('3','SWCLK'),('4','NRST'),('5','GND')]:m.tie(j,pin,name,(-12.7,0),name in ['+3V3','GND'])
 # Route current inputs through an RC at the MCU ADC pins.
 for n in list(children(m.r,'hierarchical_label')):
  if n[1] in ['ISENSE1_A','ISENSE1_B','ISENSE1_C']:
   phase=n[1][-1];n[0]=S('label');n[1]='ADC_I'+phase
   n[:]=[x for x in n if not(isinstance(x,list) and str(x[0])=='shape')]
  elif n[1]=='IO_PC4':n[1]='CSA_CAL1';one(n,'shape')[1]=S('output')
 for phase,x in zip('ABC',[40.64,92.71,144.78]):
  y=175.26;input_x=round(x-15.24,4);node_x=round(x+10.16,4);output_x=round(x+12.7,4)
  r=m.add('Device:R',ref('R'),'100R',(x,y),90,RFP);ps=m.pins(r);left=min(ps.values());right=max(ps.values());m.wire((input_x,y),left);m.label('ISENSE1_'+phase,(input_x,y),180,'hierarchical_label','input');m.wire(right,(output_x,y));m.label('ADC_I'+phase,(output_x,y))
  c=m.add('Device:C',ref('C'),'1nF',(node_x,round(y+5.08,4)),fp=CFP);m.wire((node_x,y),m.pins(c)['1']);m.junction((node_x,y));m.tie(c,'2','GND',(0,2.54),True)
 # PA0 was checked in CubeMX before this change.
 p=m.pins(m.sym('U1'))['14']
 for n in list(children(m.r,'no_connect')):
  if pos(n)==p:m.remove(n)
 m.wire(p,(132.08,p[1]));m.label('USB_VBUS',(132.08,p[1]),0,'hierarchical_label','input')
 # 5 V from the existing DRV8323 buck, followed by a real 3.3 V regulator.
 u=m.add('Regulator_Linear:AP2112K-3.3','U10','AP2112K-3.3',(210.82,139.7))
 pins=m.pins(u);print('LDO pins',pins)
 m.tie(u,'1','+5V',(-10.16,0),True);m.tie(u,'5','+3V3',(10.16,0),True);m.tie(u,'2','GND',(0,5.08),True);m.nc(pins['4'])
 vin=pins['1'];en=pins['3'];m.wire(en,(round(vin[0]-5.08,4),en[1]));m.wire((round(vin[0]-5.08,4),en[1]),(round(vin[0]-5.08,4),vin[1]));m.junction((round(vin[0]-5.08,4),vin[1]))
 for x,rail,value in [(185.42,'+5V','1uF'),(238.76,'+3V3','4.7uF')]:
  c=m.add('Device:C',ref('C'),value,(x,147.32),fp=CFP);m.tie(c,'1',rail,(0,-2.54),True);m.tie(c,'2','GND',(0,2.54),True);prop(c,'Voltage','10V')
 m.note('VCAP1/2: 2.2uF each, low ESR; place next to MCU.',(110.49,158.75));m.note('12MHz crystal: CL=18pF, C8/C9=33pF incl. stray C.',(110.49,163.83));m.note('USB: connect internal pull-up only when PA0 USB_VBUS=0.',(110.49,168.91))
 m.save()


def fix_comm():
 m=Sheet('communication.kicad_sch')
 # Keep the connector and protection ICs; rebuild the short signal networks cleanly.
 keep={props(n)['Reference']:copy.deepcopy(n) for n in m.symbols() if props(n)['Reference'] in {'J7','U8','U9','J8','J9'}}
 m.r[:]=[n for n in m.r if not(isinstance(n,list) and str(n[0]) in {'symbol','wire','junction','label','hierarchical_label','no_connect','text'})]
 # Reload the official USB symbol: SH is the actual shield pad name.
 lib=one(m.r,'lib_symbols');lib[:]=[lib[0]]+[n for n in children(lib,'symbol') if n[1]!='Connector:USB_C_Receptacle_USB2.0_16P']
 def existing(r,p):
  n=keep[r];old=pos(n);dx=p[0]-old[0];dy=p[1]-old[1]
  for a in [one(n,'at')]+[one(v,'at') for v in children(n,'property')]:a[1]=round(a[1]+dx,4);a[2]=round(a[2]+dy,4)
  if r=='J7':
   m.cache('Connector:USB_C_Receptacle_USB2.0_16P')
   for pin in children(n,'pin'):
    if pin[1]=='S1':pin[1]='SH'
  m.r.append(n);return n
 j=existing('J7',(35.56,55.88));u=existing('U8',(91.44,58.42))
 pj=m.pins(j);pu=m.pins(u)
 # Each orientation uses both D+ and both D- contacts.
 for pins,net in [(['A6','B6'],'USB_DP_CONN'),(['A7','B7'],'USB_DM_CONN')]:
  for pin in pins:m.tie(j,pin,net,(7.62,0))
 for pin,net in [('1','USB_DM_CONN'),('6','USB_N'),('3','USB_DP_CONN'),('4','USB_P')]:m.tie(u,pin,net,(-7.62,0) if pin in ['1','3'] else (7.62,0))
 m.tie(j,'A4','VBUS',(7.62,0));m.tie(u,'5','VBUS',(0,-5.08));m.tie(u,'2','GND',(0,5.08),True)
 c=m.add('Device:C',ref('C'),'100nF',(111.76,34.29),fp=CFP);m.tie(c,'1','VBUS',(0,-2.54));m.tie(c,'2','GND',(0,2.54),True);prop(c,'Voltage','10V')
 m.tie(j,'A1','GND',(0,5.08),True);m.tie(j,'SH','GND',(0,5.08),True)
 for p in ['A8','B8']:m.nc(pj[p])
 for pin,x in [('A5',60.96),('B5',73.66)]:
  q=pj[pin];r=m.add('Device:R',ref('R'),'5.1k',(x,35.56),fp=RFP)
  name='CC1' if pin=='A5' else 'CC2';m.tie(j,pin,name,(7.62,0));m.tie(r,'1',name,(0,-2.54));m.tie(r,'2','GND',(0,2.54),True)
 for name,y in [('USB_N',54.61),('USB_P',67.31)]:
  m.wire((121.92,y),(144.78,y));m.label(name,(121.92,y),180);m.label(name,(144.78,y),0,'hierarchical_label','bidirectional')
 # A MOSFET detector prevents VBUS from injecting into an unpowered PA0.
 q=m.add('Transistor_FET:2N7002',ref('Q'),'2N7002',(187.96,50.8),fp='Package_TO_SOT_SMD:SOT-23')
 m.tie(q,'1','VBUS_GATE',(-5.08,0));m.tie(q,'2','GND',(0,5.08),True)
 d=m.pins(q)['3'];m.wire(d,(d[0],38.1));m.wire((d[0],38.1),(213.36,38.1));m.label('USB_VBUS',(213.36,38.1),0,'hierarchical_label','output')
 r=m.add('Device:R',ref('R'),'10k',(203.2,29.21),fp=RFP);m.tie(r,'1','+3V3',(0,-2.54),True);m.wire(m.pins(r)['2'],(203.2,38.1));m.junction((203.2,38.1))
 r=m.add('Device:R',ref('R'),'10k',(162.56,39.37),90,RFP);pp=m.pins(r);m.wire((152.4,39.37),min(pp.values()));m.label('VBUS',(152.4,39.37),180);m.wire(max(pp.values()),(175.26,39.37));m.label('VBUS_GATE',(175.26,39.37))
 r=m.add('Device:R',ref('R'),'1M',(162.56,58.42),fp=RFP);m.tie(r,'1','VBUS_GATE',(0,-2.54));m.tie(r,'2','GND',(0,2.54),True)
 # CAN, with one optional 120-ohm split termination instead of 40 ohms.
 u=existing('U9',(76.2,125.73));p=m.pins(u)
 for pin,name,shape in [('1','CAN_TX','input'),('4','CAN_RX','output')]:
  q=p[pin];end=(round(q[0]-12.7,4),q[1]);m.wire(q,end);m.label(name,end,180,'hierarchical_label',shape)
 for pin,name in [('3','+5V'),('5','+3V3')]:m.tie(u,pin,name,(0,-7.62) if pin=='3' else (-5.08,0),True)
 grounded=set()
 for pin in ['2','8','9']:
  if p[pin] in grounded:continue
  grounded.add(p[pin]);m.tie(u,pin,'GND',(0,5.08) if pin in ['2','9'] else (-5.08,0),True)
 for pin,name in [('7','CAN_H'),('6','CAN_L')]:m.tie(u,pin,name,(7.62,0))
 for x,rail in [(40.64,'+3V3'),(58.42,'+5V')]:
  c=m.add('Device:C',ref('C'),'100nF',(x,101.6),fp=CFP);m.tie(c,'1',rail,(0,-2.54),True);m.tie(c,'2','GND',(0,2.54),True)
 for r,y in [('J8',111.76),('J9',139.7)]:
  j=existing(r,(226.06,y))
  for pin,name in [('1','CAN_H'),('2','CAN_L'),('3','GND')]:m.tie(j,pin,name,(-12.7,0),name=='GND')
  m.nc(m.pins(j)['MP'])
 ra=m.add('Device:R',ref('R'),'60.4R',(147.32,116.84),fp=RFP);rb=m.add('Device:R',ref('R'),'60.4R',(147.32,132.08),fp=RFP)
 m.tie(ra,'1','CAN_H',(0,-2.54));m.wire(m.pins(ra)['2'],m.pins(rb)['1']);m.wire((147.32,124.46),(167.64,124.46));m.junction((147.32,124.46))
 c=m.add('Device:C',ref('C'),'4.7nF',(167.64,132.08),fp=CFP);m.wire((167.64,124.46),m.pins(c)['1']);m.tie(c,'2','GND',(0,2.54),True)
 jp=m.add('Jumper:SolderJumper_2_Open','JP1','TERM_ENABLE',(147.32,147.32),90,'Jumper:SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm')
 pp=m.pins(jp);top=min(pp.values(),key=lambda p:p[1]);bot=max(pp.values(),key=lambda p:p[1]);m.wire(m.pins(rb)['2'],top);end=(bot[0],round(bot[1]+2.54,4));m.wire(bot,end);m.label('CAN_L',end)
 m.note('JP1: bridge only at a CAN-bus end (120.8R total).',(119.38,163.83));m.note('USB-C: self powered from 24V bus; no USB-to-5V back-feed.',(25.4,83.82));m.note('CC1/CC2: independent 5.1k Rd. Internal STM32 USB termination.',(25.4,88.9));m.note('PA0 USB_VBUS: LOW when cable VBUS is present.',(155,76.2))
 m.save()


def fix_gate():
 m=Sheet('gatedrv.kicad_sch')
 # Normalize all instance and wire positions together; do not alter library geometry.
 def walk_coords(n):
  if not isinstance(n,list):return
  if n and str(n[0]) in {'at','xy'} and len(n)>=3:
   n[1]=grid(n[1]);n[2]=grid(n[2])
  for x in n:walk_coords(x)
 for n in m.r:
  if isinstance(n,list) and str(n[0]) not in {'lib_symbols','sheet_instances'}:walk_coords(n)
 drv=m.sym('IC1');lib=next(n for n in children(one(m.r,'lib_symbols'),'symbol') if n[1]==one(drv,'lib_id')[1])
 new_id='foc_v2:DRV8323RSRGZR';lib[1]=new_id;one(drv,'lib_id')[1]=new_id
 types={1:'input',2:'power_in',3:'passive',4:'passive',5:'power_out',6:'power_in',7:'power_in',8:'output',9:'input',10:'output',11:'input',12:'input',13:'input',14:'input',15:'output',16:'input',17:'output',18:'output',19:'input',20:'output',21:'input',22:'input',23:'output',24:'output',25:'output',26:'power_in',27:'power_in',28:'open_collector',29:'open_collector',30:'input',31:'input',32:'input',33:'input',34:'input',35:'power_in',36:'power_out',37:'input',38:'input',39:'input',40:'input',41:'input',42:'input',43:'power_in',44:'passive',45:'output',46:'no_connect',47:'power_in',48:'input',49:'power_in'}
 for unit in children(lib,'symbol'):
  for pin in children(unit,'pin'):pin[1]=S(types[int(one(pin,'number')[1])])
 prop(drv,'Footprint','Package_DFN_QFN:Texas_RGZ0048A_VQFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm_ThermalVias')
 custom=copy.deepcopy(lib);custom[1]='DRV8323RSRGZR';(OUT/'foc_v2.kicad_sym').write_text(pretty([S('kicad_symbol_lib'),[S('version'),20241209],[S('generator'),'kicad_symbol_editor'],custom])+'\n')
 (OUT/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "foc_v2") (type "KiCad") (uri "${KIPRJMOD}/foc_v2.kicad_sym") (options "") (descr "Project DRV8323RS with electrical pin types")))\n')
 m.cache('Diode:SS16');one(m.sym('D4'),'lib_id')[1]='Diode:SS16'
 prop(m.sym('D4'),'Value','SS16');prop(m.sym('D4'),'Footprint','Diode_SMD:D_SMA');prop(m.sym('D4'),'Datasheet',props(library('Diode:SS16')).get('Datasheet',''))
 prop(m.sym('L1'),'Footprint','Inductor_SMD:L_Bourns_SRN6045TA');prop(m.sym('L1'),'Saturation current','1.5A minimum')
 for r in ['R_SA','R_SB','R_SC']:
  n=m.sym(r);prop(n,'Value','5m');prop(n,'Power','3W');prop(n,'Tolerance','1%');prop(n,'Manufacturer Part Number','WSLP2512R0050FEA');prop(n,'Function','Phase '+r[-1]+' shunt');rename_symbol(n,ref('R'))
 for r in ['C_BUS1','C_BUS2','C_BUS3','C12','C13','C17','C_BULK1']:prop(m.sym(r),'Voltage','50V')
 prop(m.sym('C16'),'Value','22uF');prop(m.sym('C16'),'Voltage','10V')
 prop(m.sym('C_BULK1'),'Footprint','Capacitor_THT:CP_Radial_D10.0mm_P5.00mm');prop(m.sym('C_BULK1'),'Ripple current','1.5A RMS minimum')
 c=m.add('Device:C_Polarized',ref('C'),'470uF',(182.88,64.77),fp='Capacitor_THT:CP_Radial_D10.0mm_P5.00mm');prop(c,'Voltage','50V');prop(c,'Ripple current','1.5A RMS minimum');m.tie(c,'1','VS',(0,-2.54),True);m.tie(c,'2','GND',(0,2.54),True)
 for r in ['J1','J2','J3']:prop(m.sym(r),'Footprint','Connector_Wire:SolderWire-1sqmm_1x01_D1.4mm_OD2.7mm')
 # Ground-side Kelvin points are GND, not conflicting net aliases.
 for n in list(children(m.r,'label')):
  if n[1] in ['SNA','SNB','SNC']:
   p=pos(n);m.remove(n)
   if p[1]==160.02:
    for wire in list(children(m.r,'wire')):
     points=[tuple(q[1:3]) for q in one(wire,'pts')[1:]]
     if p in points:m.remove(wire)
    continue
   m.power('GND',p)
 # Rebuild the two bus ends with explicit junctions and source connections.
 for y in [50.8,175.26]:
  for n in list(children(m.r,'wire')):
   ps=[tuple(p[1:3]) for p in one(n,'pts')[1:]]
   if all(p[1]==y and p[0]>=185 for p in ps) and min(p[0] for p in ps)<=195.58:m.remove(n)
  for n in list(m.symbols()):
   if pos(n)[1]==y and 189<=pos(n)[0]<=195.58:m.remove(n)
  m.wire((195.58,y),(320.04,y));m.junction((195.58,y))
  target=(195.58,43.18) if y==50.8 else (195.58,177.8);m.wire((195.58,y),target);m.power('VS' if y==50.8 else 'GND',target)
 for n in list(m.symbols()):
  if props(n).get('Reference') in ['#FLG04','#FLG05']:m.remove(n)
 # Relocate enable/fault resistors away from the interface labels.
 for reference,y,rail in [('R10',88.9,'GND'),('R8',101.6,'+3V3')]:
  m.remove(m.sym(reference))
  for n in list(children(m.r,'wire')):
   ps=[tuple(p[1:3]) for p in one(n,'pts')[1:]]
   if all(p[1]==y and 142.24<=p[0]<=180.34 for p in ps):m.remove(n)
  for n in list(m.symbols()):
   if props(n).get('Value')==rail and pos(n) in [(165.1,y),(175.26,y)]:m.remove(n)
  m.wire((142.24,y),(152.4,y))
 r=m.add('Device:R','R10','100k',(154.94,160.02),fp=RFP);m.tie(r,'1','EN_GATE1',(0,-2.54));m.tie(r,'2','GND',(0,2.54),True)
 r=m.add('Device:R','R8','10k',(172.72,160.02),fp=RFP);m.tie(r,'1','+3V3',(0,-2.54),True);m.tie(r,'2','NFAULT1',(0,2.54))
 # CAL is a real MCU-controlled input instead of being permanently grounded.
 cal=m.pins(drv)['34']
 for n in list(children(m.r,'wire')):
  ps=[tuple(p[1:3]) for p in one(n,'pts')[1:]]
  if cal in ps:
   end=ps[1] if ps[0]==cal else ps[0];m.remove(n)
   for sym in list(m.symbols()):
    if props(sym).get('Value')=='GND' and pos(sym)==end:m.remove(sym)
 m.wire(cal,(152.4,cal[1]));m.label('CSA_CAL1',(152.4,cal[1]),0,'hierarchical_label','input')
 r=m.add('Device:R',ref('R'),'100k',(137.16,160.02),fp=RFP);m.tie(r,'1','CSA_CAL1',(0,-2.54));m.tie(r,'2','GND',(0,2.54),True)
 # The DRV SDO output is open drain; add the required pull-up.
 r=m.add('Device:R',ref('R'),'4.7k',(190.5,160.02),fp=RFP);m.tie(r,'1','+3V3',(0,-2.54),True);m.tie(r,'2','SPI1_MISO',(0,2.54))
 r=m.add('Device:R',ref('R'),'10k',(119.38,160.02),fp=RFP);m.tie(r,'1','+3V3',(0,-2.54),True);m.tie(r,'2','SPI1_SS0',(0,2.54))
 # 24-V bus input, replaceable 10-A fuse, and transient suppression.
 j=m.add('Connector:Conn_01x02_Pin','J11','24V_IN',(40.64,190.5),0,'Connector_AMASS:AMASS_XT30PW-M_1x02_P2.50mm_Horizontal');p=m.pins(j)
 f=m.add('Device:Fuse','F1','10A 58V',(62.23,p['1'][1]),90,'Fuse:Fuseholder_Blade_Mini_Keystone_3568');pf=m.pins(f);left=min(pf.values());right=max(pf.values());m.wire(p['1'],left);m.wire(right,(76.2,right[1]));m.power('VS',(76.2,right[1]));m.tie(j,'2','GND',(0,7.62),True)
 for start,end in [((76.2,190.5),(83.82,190.5)),((45.72,198.12),(50.8,198.12))]:
  m.wire(start,end);m.junction(start);flag=m.add('power:PWR_FLAG',ref('#FLG'),'PWR_FLAG',end)
  for p in children(flag,'property'):
   if p[1] in ['Reference','Value']:one(p,'effects').append([S('hide'),S('yes')])
 d=m.add('Device:D_Zener',ref('D'),'SMBJ30A',(91.44,198.12),270,'Diode_SMD:D_SMB');pd=m.pins(d);top=min(pd,key=lambda k:pd[k][1]);bot=max(pd,key=lambda k:pd[k][1]);assert top=='1';m.tie(d,top,'VS',(0,-2.54),True);m.tie(d,bot,'GND',(0,2.54),True)
 # Voltage ADC: 150k/10k = 1/16, 24 V -> 1.5 V; 10 nF anti-alias filter.
 rt=m.add('Device:R',ref('R'),'150k',(132.08,193.04),fp='Resistor_SMD:R_0805_2012Metric');rb=m.add('Device:R',ref('R'),'10k',(132.08,208.28),fp=RFP)
 m.tie(rt,'1','VS',(0,-2.54),True);m.wire(m.pins(rt)['2'],m.pins(rb)['1']);m.wire((132.08,200.66),(157.48,200.66));m.junction((132.08,200.66));m.label('PV_SENSE',(157.48,200.66),0,'hierarchical_label','output');m.tie(rb,'2','GND',(0,2.54),True)
 c=m.add('Device:C',ref('C'),'10nF',(149.86,208.28),fp=CFP);m.wire((149.86,200.66),m.pins(c)['1']);m.junction((149.86,200.66));m.tie(c,'2','GND',(0,2.54),True)
 # Connect the hold-off resistors directly to each MOSFET gate after its 2.2R.
 for high,low in [('Q1','Q2'),('Q3','Q4'),('Q5','Q6')]:
  for q,y in [(high,83.82),(low,129.54)]:
   p=m.pins(m.sym(q));x=p['4'][0]
   r=m.add('Device:R',ref('R'),'100k',(x,y),fp=RFP);rp=m.pins(r)
   m.wire(p['4'],rp['1']);m.wire(rp['2'],(p['1'][0],rp['2'][1]));m.junction(p['4']);m.junction((p['1'][0],rp['2'][1]))
   for field in children(m.sym(q),'property'):
    if field[1] in ['Reference','Value']:
     one(field,'at')[1:]=[pos(m.sym(q))[0]+2.54,pos(m.sym(q))[1]+(-7.62 if field[1]=='Reference' else 7.62),0]
  for rname in ['R1','R2'] if high=='Q1' else (['R3','R4'] if high=='Q3' else ['R5','R7']):
   n=m.sym(rname);x,y=pos(n)
   for field in children(n,'property'):
    if field[1] in ['Reference','Value']:
     one(field,'at')[1:]=[x,y+(-5.08 if field[1]=='Reference' else -2.54),90]
     one(field,'effects')[:]=[S('effects'),[S('font'),[S('size'),1,1]]]
 n=m.sym('C_BULK1');x,y=pos(n)
 for field in children(n,'property'):
  if field[1] in ['Reference','Value']:
   one(field,'at')[1:]=[x+2.54,y+(-1.27 if field[1]=='Reference' else 1.27),0]
   one(field,'effects')[:]=[S('effects'),[S('font'),[S('size'),1,1]],[S('justify'),S('left')]]
 for refname in ['C_BUS1','C_BUS2','C_BUS3']:
  n=m.sym(refname);x,y=pos(n)
  for field in children(n,'property'):
   if field[1] in ['Reference','Value']:
    one(field,'at')[1:]=[x+2.54,y+(-1.27 if field[1]=='Reference' else 1.27),0]
    one(field,'effects')[:]=[S('effects'),[S('font'),[S('size'),1,1]],[S('justify'),S('left')]]
 # Keep the low-side sense labels away from gate hold-off resistor fields.
 for label in children(m.r,'label'):
  if label[1] in ['SPA','SPB','SPC'] and pos(label)[1]==129.54 and pos(label)[0]>=200:
   p=pos(label)
   for wire in list(children(m.r,'wire')):
    if p in [tuple(q[1:3]) for q in one(wire,'pts')[1:]]:m.remove(wire)
   one(label,'at')[1:3]=[round(p[0]+17.78,4),p[1]]
 m.note('24V nominal / 10A peak phase. Shunts: 5mR 3W, Kelvin sense.',(30.48,228.6));m.note('CSA gain 20: 100mV/A, zero at 1.65V; calibrate with PC4 before PWM.',(30.48,233.68));m.note('Use a bus supply that accepts regeneration, or an external brake clamp.',(30.48,238.76));m.note('100k gate-source resistors: place beside each MOSFET.',(205.74,218.44))
 m.save()


def fix_hall():
 m=Sheet('hall.kicad_sch')
 r=m.add('Device:R',ref('R'),'10k',(111.76,63.5),fp=RFP);m.tie(r,'1','+3V3',(0,-2.54),True);m.tie(r,'2','HALL_CS',(0,2.54))
 m.save()


def fix_root():
 m=Sheet('foc_v2.kicad_sch');sheets={props(n)['Sheetname']:n for n in children(m.r,'sheet')}
 def pin(sheet,name):return next(n for n in children(sheets[sheet],'pin') if n[1]==name)
 def newpin(sheet,name,kind,p,angle=180):
  n=[S('pin'),name,S(kind),[S('at'),*p,angle],[S('uuid'),uid()],[S('effects'),[S('font'),[S('size'),1.27,1.27]],[S('justify'),S('right' if angle==0 else 'left')]]];sheets[sheet].append(n);return n
 cal=pin('MCU','IO_PC4');old=pos(cal);cal[1]='CSA_CAL1';cal[2]=S('output');one(cal,'at')[1:]=[158.75,124.46,0];one(one(cal,'effects'),'justify')[1]=S('right')
 pv=pin('MCU','PV_SENSE');one(pv,'at')[1:]=[158.75,129.54,0];one(one(pv,'effects'),'justify')[1]=S('right')
 for n in list(children(m.r,'no_connect')):
  if pos(n)==old:m.remove(n)
 newpin('GATE_DRV','CSA_CAL1','input',(187.96,124.46));newpin('GATE_DRV','PV_SENSE','output',(187.96,129.54))
 newpin('MCU','USB_VBUS','input',(158.75,71.12),0);newpin('COMMUNICATION','USB_VBUS','output',(158.75,33.02),0)
 for name in ['CSA_CAL1','PV_SENSE']:m.wire(pos(pin('MCU',name)),pos(pin('GATE_DRV',name)))
 m.wire((158.75,33.02),(170.18,33.02));m.wire((170.18,33.02),(170.18,71.12));m.wire((170.18,71.12),(158.75,71.12))
 for name in ['MCU','GATE_DRV']:
  one(sheets[name],'size')[2]=76.2 if name=='MCU' else 71.12
  for p in children(sheets[name],'property'):
   if p[1]=='Sheetfile':one(p,'at')[2]=138.43
 for n in children(m.r,'text'):
  if n[1].startswith('DRV8323:'):one(n,'at')[2]=144.78
 m.save()


def main():
 v=json.loads((W/'cubemx-validation.json').read_text())[0]['result']['structuredContent'];assert v['valid'],v.get('diagnostics')
 assert hashlib.sha256((OUT/'src.ioc').read_bytes()).hexdigest()==v['source_sha256']
 fix_mcu();fix_comm();fix_gate();fix_root();fix_hall()
 power_counts={'#PWR':0,'#FLG':0}
 for name in NAMES:
  sheet=Sheet(name)
  for n in sheet.symbols():
   current=props(n).get('Reference','')
   for prefix in power_counts:
    if current.startswith(prefix):
     power_counts[prefix]+=1;rename_symbol(n,prefix+str(power_counts[prefix]).zfill(3));break
  sheet.save()
 p=json.loads((W/'before/foc_v2.kicad_pro').read_text());p['schematic']['reuse_designators']=False
 (OUT/'foc_v2.kicad_pro').write_text(json.dumps(p,indent=2)+'\n')
 allrefs=[props(n)['Reference'] for r in A.values() for n in children(r,'symbol') if not props(n).get('Reference','').startswith('#')]
 assert len(allrefs)==len(set(allrefs)),[r for r in allrefs if allrefs.count(r)>1]
 print('All sheets updated; unique component references:',len(allrefs))
if __name__=='__main__':main()
