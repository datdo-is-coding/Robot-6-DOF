import re
import sys
sys.path.insert(0, 'scratch')
from apply_p_final import P_final
from flip_utils import flip_footprint_layers_to_back, flip_footprint_layers_to_front

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
    
    # Flip child layers based on target layer
    if layer == 'B.Cu':
        chunk_new = flip_footprint_layers_to_back(chunk_new)
    elif layer == 'F.Cu':
        chunk_new = flip_footprint_layers_to_front(chunk_new)
        
    new_parts.append(chunk_new)

content_str = "(footprint ".join(new_parts)

with open('foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(content_str)

print("Saved foc_v2.kicad_pcb with properly flipped child layers!")
