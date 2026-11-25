import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    cur = f.read()

with open('work/2026-11-13-pcb-layout/before-grid.kicad_pcb', 'r', encoding='utf-8') as f:
    bg = f.read()

cur_segs = len(re.findall(r'\(segment\b', cur))
cur_vias = len(re.findall(r'\(via\b', cur))
bg_segs = len(re.findall(r'\(segment\b', bg))
bg_vias = len(re.findall(r'\(via\b', bg))

print(f"Current foc_v2.kicad_pcb: {cur_segs} segments, {cur_vias} vias")
print(f"before-grid.kicad_pcb:     {bg_segs} segments, {bg_vias} vias")
