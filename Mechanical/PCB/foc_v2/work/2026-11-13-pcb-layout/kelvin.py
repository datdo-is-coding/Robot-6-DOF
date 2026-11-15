"""Give the six shunt sense traces their own nets and copper pickup points."""
import runpy, copy, json, hashlib
from pathlib import Path
W=Path(__file__).resolve().parent;ROOT=W.parent.parent;OUT=W/'candidate'
g=runpy.run_path(str(W.parent/'2026-11-13-full-schematic-fix/fix_all.py'))
sx=g['sx'];S=g['S'];ch=g['children'];one=g['one'];pos=g['pos'];props=g['props'];prop=g['prop']
g['A']['gatedrv.kicad_sch']=sx.loads((ROOT/'gatedrv.kicad_sch').read_text())
# Class methods retain the module namespace returned by runpy.
g['Sheet'].save.__globals__['OUT']=OUT
m=g['Sheet']('gatedrv.kicad_sch');drv=m.sym('IC1');pins=m.pins(drv)
prop(m.sym('J11'),'Footprint','foc_v2:AMASS_XT30PW-M_Edge_NoSilk')
for pin,name in [('12','SNA'),('13','SNB'),('22','SNC')]:
 start=pins[pin]
 wire=next(n for n in ch(m.r,'wire') if start in [tuple(q[1:3]) for q in one(n,'pts')[1:]])
 ps=[tuple(q[1:3]) for q in one(wire,'pts')[1:]];end=next(q for q in ps if q!=start)
 ground=next(n for n in m.symbols() if props(n).get('Value')=='GND' and pos(n)==end)
 m.remove(ground);m.label(name,end,90 if pin in ['13','22'] else 0)
for n in ch(m.r,'label'):
 if n[1] in ['SPA','SPB','SPC'] and pos(n)[0]<185:n[1]='CSA_'+n[1]
for i,(a,b) in enumerate([('CSA_SPA','SPA'),('SNA','GND'),('CSA_SPB','SPB'),('SNB','GND'),('CSA_SPC','SPC'),('SNC','GND')],1):
 x=round(45.72+45.72*(i-1),4)
 n=m.add('Device:NetTie_2','NT'+str(i),'KELVIN_'+a,(x,254),fp='foc_v2:NetTie_Kelvin')
 one(n,'in_bom')[1]=S('no');m.tie(n,'1',a,(-5.08,0));m.tie(n,'2',b,(5.08,0),b=='GND')
m.note('Kelvin copper pickups at the inner shunt pads: NT1-NT6 are copper only, no assembled parts.',(30.48,243.84))
m.save()
lib=OUT/'foc_v2.pretty';lib.mkdir(exist_ok=True)
(lib/'NetTie_Kelvin.kicad_mod').write_text('''(footprint "NetTie_Kelvin" (version 20260206) (generator "pcbnew")
 (layer "F.Cu") (descr "Copper-only Kelvin pickup; pad 2 sits at the inner edge of a shunt power pad")
 (attr smd exclude_from_pos_files exclude_from_bom allow_missing_courtyard)
 (property "Reference" "NT" (at 0 -1) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
 (property "Value" "NetTie_Kelvin" (at 0 1) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15))))
 (net_tie_pad_groups "1,2")
 (fp_line (start 0 0) (end 0.65 0) (stroke (width 0.25) (type solid)) (layer "F.Cu"))
 (pad "1" smd rect (at 0 0) (size 0.35 0.35) (layers "F.Cu"))
 (pad "2" smd rect (at 0.65 0) (size 0.35 0.35) (layers "F.Cu"))
)\n''')
(OUT/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "foc_v2") (type "KiCad") (uri "${KIPRJMOD}/foc_v2.pretty") (options "") (descr "Copper Kelvin pickups")))\n')
print('Six copper-only Kelvin pickups added; MCU pin allocation unchanged.')
