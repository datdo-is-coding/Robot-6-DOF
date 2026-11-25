import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(C_BULK1|C63)"', p)
    if ref_m:
        print(f"=== {ref_m.group(1)} ===")
        print(p[:400])
