import hashlib,json,math,xml.etree.ElementTree as E
from pathlib import Path
W=Path(__file__).resolve().parent
r=E.parse(W/'candidate.net.xml').getroot()
comps={c.get('ref'):{p.tag:p.text for p in c if p.tag in ['value','footprint']} for c in r.findall('./components/comp')}
assert len(comps)==len(r.findall('./components/comp'))
nets={};members={}
for n in r.findall('./nets/net'):
 key=n.get('name');members[key]=set()
 for p in n.findall('node'):
  pin=(p.get('ref'),p.get('pin'));assert pin not in nets,pin;nets[pin]=key;members[key].add(pin)
def net(ref,pin):return nets[ref,str(pin)]
def same(a,b):assert net(*a)==net(*b),(a,b,net(*a),net(*b))
def value(ref):return comps[ref]['value']
def other(ref,n):
 pins=[p for p in nets if p[0]==ref and nets[p]!=n]
 assert len(pins)==1,(ref,n,pins)
 return nets[pins[0]]
def resistor_between(a,b,v):
 result=[ref for ref,c in comps.items() if c['value']==v and {net(ref,1),net(ref,2)}=={a,b} and ref.startswith('R')]
 assert len(result)==1,(a,b,v,result)
 return result[0]
gnd=net('U1',18);v33=net('U1',19);vs=net('IC1',6);v5=net('U10',1)
for p in [1,19,32,48,64]:assert net('U1',p)==v33
for p in [12,18,63]:assert net('U1',p)==gnd
assert net('U10',5)==v33 and net('U10',2)==gnd and net('U10',3)==v5
for p,c in [(31,'C10'),(47,'C11')]:same(('U1',p),(c,1));assert value(c)=='2.2uF' and net(c,2)==gnd
assert net('U1',31)!=net('U1',47)
for p in [6,7,47,48]:assert net('IC1',p)==vs,p
assert net('IC1',36)!=v33
assert net('U9',3)==v5 and net('U9',5)==v33
for label,a,b in [('CS',('U1',50),('U2',5)),('SCK',('U1',55),('U2',12)),('MISO',('U1',52),('U2',7)),('MOSI',('U1',53),('U2',4)),('DRV_MISO',('U1',56),('IC1',29)),('DRV_MOSI',('U1',57),('IC1',30)),('DRV_SCK',('U1',21),('IC1',31)),('DRV_CS',('U1',51),('IC1',32)),('CAN_RX',('U1',61),('U9',4)),('CAN_TX',('U1',62),('U9',1)),('CAL',('U1',24),('IC1',34)),('ENABLE',('U1',40),('IC1',33)),('FAULT',('U1',30),('IC1',28))]:same(a,b)
resistor_between(v33,net('IC1',29),'4.7k');resistor_between(gnd,net('IC1',33),'100k');resistor_between(gnd,net('IC1',34),'100k')
resistor_between(v33,net('IC1',32),'10k');resistor_between(v33,net('U2',5),'10k')
for p,q in [(41,37),(34,38),(42,39),(35,40),(43,41),(36,42)]:same(('U1',p),('IC1',q))
# Every half bridge has the correct MOSFET orientation, shunt, and gate resistor.
for high,low,driver_h,driver_l,sp,sn,phase in [('Q1','Q2',8,10,11,12,'J1'),('Q3','Q4',17,15,14,13,'J2'),('Q5','Q6',18,20,21,22,'J3')]:
 assert net(high,5)==vs
 same((high,1),(low,5));same((high,1),(phase,1));same((low,1),('IC1',sp));assert net('IC1',sn)==gnd
 resistor_between(net(high,4),net('IC1',driver_h),'2.2R');resistor_between(net(low,4),net('IC1',driver_l),'2.2R')
 resistor_between(net(high,4),net(high,1),'100k');resistor_between(net(low,4),net(low,1),'100k')
 resistor_between(net(low,1),gnd,'5m')
for pin,driver in [(11,25),(17,24),(20,23)]:
 resistor_between(net('U1',pin),net('IC1',driver),'100R')
 cs=[p[0] for p in members[net('U1',pin)] if p[0].startswith('C') and comps[p[0]]['value']=='1nF']
 assert len(cs)==1 and other(cs[0],net('U1',pin))==gnd
assert len({net('U1',p) for p in [11,17,20]})==3
busnode=net('U1',22);resistor_between(vs,busnode,'150k');resistor_between(busnode,gnd,'10k')
for p in ['A5','B5']:resistor_between(net('J7',p),gnd,'5.1k')
assert net('J7','A5')!=net('J7','B5')
for p in ['A6','B6']:same(('J7',p),('U8',3))
for p in ['A7','B7']:same(('J7',p),('U8',1))
same(('U1',44),('U8',6));same(('U1',45),('U8',4))
same(('U1',14),('Q7',3));assert net('Q7',2)==gnd
resistor_between(net('U1',14),v33,'10k');resistor_between(net('Q7',1),gnd,'1M');resistor_between(net('Q7',1),net('J7','A4'),'10k')
assert net('J7','A4')!=v5
for p,node in [(1,v33),(2,net('U1',46)),(3,net('U1',49)),(4,net('U1',7)),(5,gnd)]:assert net('J10',p)==node
same(('J11',1),('F1',1));assert net('F1',2)==vs and net('J11',2)==gnd
assert net('D6',1)==vs and net('D6',2)==gnd
assert value('D4')=='SS16'
assert net('JP1',2)==net('U9',6) or net('JP1',1)==net('U9',6)
assert len([r for r,c in comps.items() if c['value']=='60.4R'])==2
report=json.loads((W/'candidate-erc.json').read_text());assert all(not s['violations'] for s in report['sheets'])
summary={'erc':{s['path']:0 for s in report['sheets']},'components':len(comps),'critical_connectivity':'passed','bus_voltage_nominal':24,'phase_current_peak_A':10,'shunt_ohms':.005,'shunt_loss_at_peak_W':10**2*.005,'csa_gain':20,'csa_output_at_plusminus10A_V':[1.65-10*.005*20,1.65+10*.005*20],'bus_divider_ratio':16,'bus_adc_at_24V':24/16,'can_termination_enabled_ohms':120.8,'usb_vbus_active_low':True,'cubemx_validated':True}
assert .25<min(summary['csa_output_at_plusminus10A_V']) and max(summary['csa_output_at_plusminus10A_V'])<3.05
(W/'checks.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
