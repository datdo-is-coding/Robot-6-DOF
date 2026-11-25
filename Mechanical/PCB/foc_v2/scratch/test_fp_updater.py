import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
print(f"Total footprint parts: {len(parts) - 1}")

import sys
sys.path.insert(0, 'scratch')
from verify_all_clean import P

updated_count = 0
new_parts = [parts[0]]

for chunk in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', chunk)
    if not ref_m:
        new_parts.append(chunk)
        continue
    
    ref = ref_m.group(1)
    if ref not in P:
        print(f"Warning: {ref} not in P!")
        new_parts.append(chunk)
        continue
    
    x, y, rot, layer = P[ref]
    
    # 1. Update (at X Y ROT)
    # Match the first (at ...) before (property or (pad
    # Typically: \n\s+\(at\s+[0-9.-]+\s+[0-9.-]+(?:\s+[0-9.-]+)?\)
    def repl_at(m):
        if rot == 0:
            return f"\n\t\t(at {x:.4f} {y:.4f})"
        else:
            return f"\n\t\t(at {x:.4f} {y:.4f} {rot:.1f})"
    
    chunk_new = re.sub(r'\n\s+\(at\s+[0-9.-]+\s+[0-9.-]+(?:\s+[0-9.-]+)?\)', repl_at, chunk, count=1)
    
    # 2. Update (layer "...")
    def repl_layer(m):
        return f'\n\t\t(layer "{layer}")'
    chunk_new = re.sub(r'\n\s+\(layer\s+"[^"]+"\)', repl_layer, chunk_new, count=1)
    
    new_parts.append(chunk_new)
    updated_count += 1

print(f"Successfully updated {updated_count} / {len(P)} footprints!")

# Let's verify by re-checking positions in the joined text
new_text = "(footprint ".join(new_parts)
check_parts = new_text.split('(footprint ')
for p in check_parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m and ref_m.group(1) in ['H3', 'J11', 'Q1', 'Q5', 'IC1', 'U10', 'D4', 'L1', 'C16']:
        ref = ref_m.group(1)
        at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', p)
        print(f"{ref:6s}: target={P[ref]} -> got={at_m.groups() if at_m else 'NO AT'}")
