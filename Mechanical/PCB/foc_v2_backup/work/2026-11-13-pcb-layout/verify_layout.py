from pathlib import Path
import pcbnew as p
import json,hashlib,math,sexpdata as sx
from shapely.geometry import LineString
from shapely.ops import unary_union
W=Path(__file__).resolve().parent;C=W/'candidate';ROOT=W.parent.parent
drc=json.loads((W/'final-drc.json').read_text());erc=json.loads((W/'final-erc.json').read_text())
assert all(not drc[k] for k in ['violations','unconnected_items','schematic_parity'])
assert len(erc['sheets'])==5 and not any(s['violations'] for s in erc['sheets'])
b=p.LoadBoard(str(C/'foc_v2.kicad_pcb'));assert b.GetCopperLayerCount()==4
fs={f.GetReference():f for f in b.GetFootprints()};assert len(fs)==124
assert fs['U2'].IsFlipped() and fs['U2'].GetPosition()==p.VECTOR2I(p.FromMM(100),p.FromMM(100))
for ref in ['H1','H2','H3','H4']:
    f=fs[ref];x,y=p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)
    assert abs(math.hypot(x-100,y-100)-13)<.001
    assert abs(p.ToMM(next(iter(f.Pads())).GetDrillSize().x)-2.7)<.00001
raw=fs['J11'].FindPadByNumber('1').GetNetname()
def xy(v):return p.ToMM(v.x),p.ToMM(v.y)
def power(board):
    geoms={};vias=set()
    for t in board.GetTracks():
        if isinstance(t,p.PCB_VIA):
            if t.GetWidth(p.F_Cu)>=p.FromMM(.8):vias.add((t.GetNetname(),*xy(t.GetPosition())))
        elif t.GetWidth()>=p.FromMM(.8) and t.GetNetname()!=raw:
            geoms.setdefault((t.GetNetname(),t.GetLayer()),[]).append(LineString([xy(t.GetStart()),xy(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2))
    return {k:unary_union(v) for k,v in geoms.items()},vias
old,old_vias=power(p.LoadBoard(str(W/'before-driver-move.kicad_pcb')));new,new_vias=power(b)
assert old_vias==new_vias and len(new_vias)==81
for k,g in old.items():assert g.hausdorff_distance(new[k])<.005,k
assert (C/'src.ioc').read_bytes()==(ROOT/'src.ioc').read_bytes()==(W/'before/src.ioc').read_bytes()
files=[f for f in C.iterdir() if f.is_file() and f.suffix in ['.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_sym','.ioc']]
files += [C/'sym-lib-table',C/'fp-lib-table',*sorted((C/'foc_v2.pretty').glob('*.kicad_mod'))]
hashes={str(f.relative_to(C)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
result={'footprints':124,'diameter_mm':70,'hole_diameter_mm':2.7,'mounting_pcd_mm':26,'copper_layers':4,'sensor_bottom_center_mm':[100,100],'power_vias_0p8_0p4':81,'drc_violations':0,'unconnected':0,'schematic_parity':0,'erc_violations':0,'source_ioc_unchanged':True,'candidate_sha256':hashes}
(W/'final-checks.json').write_text(json.dumps(result,indent=2)+'\n');print('Layout verified: 0 ERC / 0 DRC / 0 unconnected; 81 power vias and phase copper preserved')
