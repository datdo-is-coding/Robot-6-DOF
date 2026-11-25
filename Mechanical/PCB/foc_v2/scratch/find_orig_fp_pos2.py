import sexpdata

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    # let's find each (footprint ...)
    text = f.read()

import re
# Match each (footprint "..." ...)
# In KiCad 8/9/10, footprint starts with (footprint "..." and ends at closing paren
fps = re.findall(r'\(footprint\s+\"([^\"]+)\"([\s\S]*?\n  \))', text)
print(f"Found {len(fps)} footprints")
for fp_type, body in fps:
    ref_m = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"', body)
    if ref_m:
        ref = ref_m.group(1)
        if ref in ['C63', 'C_BULK1', 'J11', 'F1', 'D6', 'L1', 'D4']:
            at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', body)
            rot = at_m.group(3) if at_m and at_m.group(3) else '0'
            print(f"{ref:8s}: at ({at_m.group(1)}, {at_m.group(2)}, {rot})")
