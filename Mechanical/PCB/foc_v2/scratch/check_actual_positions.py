import re

text = open('foc_v2.kicad_pcb', 'r', encoding='utf-8').read()
parts = text.split('(footprint ')
print("Parts:", len(parts))
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m and ref_m.group(1) in ['H3', 'J11', 'Q1', 'Q5', 'IC1', 'U10', 'D4']:
        ref = ref_m.group(1)
        at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', p)
        print(f"{ref:6s}: {at_m.groups() if at_m else 'NO AT'}")
