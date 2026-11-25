import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(C_BULK1|C63)"', block)
    if ref_m:
        print(f"=== {ref_m.group(1)} ===")
        for line in block.split('\n'):
            if any(k in line for k in ['fp_circle', 'fp_line', 'pad', 'CrtYd', 'layer']):
                print("  ", line.strip())
        break
