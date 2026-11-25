import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')

import sys
sys.path.insert(0, 'scratch')
from verify_all_clean import P

new_parts = [parts[0]]

for chunk in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', chunk)
    if not ref_m or ref_m.group(1) not in P:
        new_parts.append(chunk)
        continue
    
    ref = ref_m.group(1)
    x, y, rot, layer = P[ref]
    
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

# Remove old standalone Edge.Cuts lines
edge_block_pattern = r'\s*\(gr_(?:line|arc)\s*\n(?:\s+\([^\n]+\n)*?\s+\(layer\s+"Edge\.Cuts"\)[\s\S]*?\n\s*\)'
content_str = re.sub(edge_block_pattern, '', content_str)

# Watertight Edge.Cuts with flat cuts
new_edge_cuts = """
\t(gr_line
\t\t(start 69.0 132.5)
\t\t(end 131.0 132.5)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-south-flat-line")
\t)
\t(gr_line
\t\t(start 131.0 132.5)
\t\t(end 136.0 125.0)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-se-chamfer")
\t)
\t(gr_line
\t\t(start 136.0 125.0)
\t\t(end 136.0 92.0)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-east-flat-line")
\t)
\t(gr_line
\t\t(start 136.0 92.0)
\t\t(end 134.0712 92.0)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-ne-trans")
\t)
\t(gr_arc
\t\t(start 134.0712 92.0)
\t\t(mid 100.0 65.0)
\t\t(end 65.9288 92.0)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-north-circle-arc")
\t)
\t(gr_line
\t\t(start 65.9288 92.0)
\t\t(end 65.0 92.0)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-nw-trans")
\t)
\t(gr_line
\t\t(start 65.0 92.0)
\t\t(end 65.0 125.0)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-west-flat-line")
\t)
\t(gr_line
\t\t(start 65.0 125.0)
\t\t(end 69.0 132.5)
\t\t(stroke (width 0.05) (type default))
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-sw-chamfer")
\t)
"""

idx = content_str.rfind(')')
if idx != -1:
    content_str = content_str[:idx] + new_edge_cuts + "\n)\n"

with open('foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(content_str)

print("Saved pristine foc_v2.kicad_pcb successfully!")
