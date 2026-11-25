import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by (footprint
tokens = text.split('(footprint ')
print(f"Total parts: {len(tokens)}")
for t in tokens[1:]:
    ref_m = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"', t)
    if ref_m:
        ref = ref_m.group(1)
        if ref in ['C63', 'C_BULK1', 'J11', 'F1', 'D6', 'L1', 'D4', 'IC1', 'U1']:
            at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', t)
            rot = at_m.group(3) if at_m and at_m.group(3) else '0'
            print(f"{ref:8s}: at ({at_m.group(1)}, {at_m.group(2)}, {rot})")
