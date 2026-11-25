import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Split properly by footprints
# In KiCad 7/8/9/10, top level footprints start with \t(footprint
tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
print(f"Total footprint blocks found: {len(tokens)-1}")

fps = {}
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if ref_m:
        ref = ref_m.group(1)
        at_m = re.search(r'\(at\s+([^\)]+)\)', block)
        fps[ref] = at_m.group(1) if at_m else 'unknown'

refs = ['J1', 'J2', 'J3', 'J7', 'J8', 'J9', 'J10', 'H1', 'H2', 'H3', 'H4', 'C_BULK1', 'C63', 'IC1', 'U1', 'U2']
for r in refs:
    print(f"{r:8s}: {fps.get(r, 'NOT FOUND')}")
