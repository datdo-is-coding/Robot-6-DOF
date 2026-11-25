import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(H[1-4])"', block)
    if ref_m:
        print(f"=== {ref_m.group(1)} ===")
        print(block)
        break
