import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
from verify_all_clean import P

P_final = dict(P)

# Refined positions for 0 DRC overlaps
P_final['R51'] = (86.0, 94.5, 0, 'F.Cu')
P_final['R52'] = (86.0, 96.5, 0, 'F.Cu')

P_final['R9']  = (89.8, 93.6, 0, 'F.Cu')
P_final['R10'] = (89.8, 95.4, 0, 'F.Cu')
P_final['R50'] = (89.8, 97.2, 0, 'F.Cu')

P_final['C12'] = (93.5, 96.5, 0, 'F.Cu')

P_final['U8']  = (96.0, 118.0, 0, 'B.Cu')
P_final['C59'] = (100.0, 118.0, 0, 'B.Cu')
P_final['Q7']  = (104.0, 118.0, 0, 'B.Cu')

P_final['R40'] = (94.5, 120.5, 0, 'B.Cu')
P_final['R41'] = (98.0, 120.5, 0, 'B.Cu')
P_final['R42'] = (101.5, 120.5, 0, 'B.Cu')
P_final['R43'] = (105.0, 120.5, 0, 'B.Cu')

# Update foc_v2.kicad_pcb
import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
new_parts = [parts[0]]

for chunk in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', chunk)
    if not ref_m or ref_m.group(1) not in P_final:
        new_parts.append(chunk)
        continue
    
    ref = ref_m.group(1)
    x, y, rot, layer = P_final[ref]
    
    def repl_at(m):
        if rot == 0:
            return f"\n\t\t(at {x:.4f} {y:.4f})"
        else:
            return f"\n\t\t(at {x:.4f} {y:.4f} {rot:.1f})"
    
    chunk_new = re.sub(r'\n\s+\(at\s+[0-9.-]+\s+[0-9.-]+(?:\s+[0-9.-]+)?\)', repl_at, chunk, count=1)
    
    def repl_layer(m):
        return f'\n\t\t(layer "{layer}")'
    chunk_new = re.sub(r'\n\s+\(layer\s+"[^"]+"\)', repl_layer, chunk_new, count=1)
    
    new_parts.append(chunk_new)

content_str = "(footprint ".join(new_parts)

with open('foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(content_str)

print("Updated foc_v2.kicad_pcb with P_final successfully!")
