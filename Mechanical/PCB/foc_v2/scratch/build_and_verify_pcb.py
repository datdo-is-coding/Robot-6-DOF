import re
import json
import subprocess
import os
import sys

sys.path.insert(0, 'scratch')
from verify_all_clean import P

pcb_file = 'foc_v2.kicad_pcb'
with open(pcb_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update footprints
# Parse all (footprint ...) blocks
def update_footprints(content, P):
    # Footprint pattern
    # We will iterate through all references in P and replace their (at ...) and (layer ...)
    for ref, (x, y, rot, layer) in P.items():
        # Find footprint block with Reference "ref"
        pattern = r'(\(footprint\s+"[^"]+"[\s\S]*?\(property\s+"Reference"\s+"' + re.escape(ref) + r'"[\s\S]*?\n\t\))'
        m = re.search(pattern, content)
        if not m:
            # Try alternate indentation
            pattern = r'(\(footprint\s+"[^"]+"[\s\S]*?\(property\s+"Reference"\s+"' + re.escape(ref) + r'"[\s\S]*?\n  \))'
            m = re.search(pattern, content)
        if not m:
            print(f"Warning: footprint {ref} not found!")
            continue
        
        block = m.group(1)
        
        # Replace the main (at X Y ROT)
        # Note: the first (at ...) in the footprint is the footprint location
        # (at x y [rot])
        # Be careful not to replace (at ...) inside properties or pads!
        at_sub_pattern = r'(\(footprint\s+"[^"]+"\s*\n(?:\s+\([^\n]+\n)*?\s+\(at\s+)[0-9.-]+\s+[0-9.-]+(?:\s+[0-9.-]+)?(\))'
        
        def repl_at(match):
            prefix = match.group(1)
            suffix = match.group(2)
            if rot == 0:
                return f"{prefix}{x:.4f} {y:.4f}{suffix}"
            else:
                return f"{prefix}{x:.4f} {y:.4f} {rot:.1f}{suffix}"
        
        new_block = re.sub(at_sub_pattern, repl_at, block, count=1)
        
        # Replace main (layer "...")
        layer_sub_pattern = r'(\(footprint\s+"[^"]+"\s*\n(?:\s+\([^\n]+\n)*?\s+\(layer\s+)"[^"]+"(\))'
        new_block = re.sub(layer_sub_pattern, r'\1"' + layer + r'"\2', new_block, count=1)
        
        content = content.replace(block, new_block, 1)
        
    return content

print("Updating footprint positions...")
content = update_footprints(content, P)

# 2. Update Edge.Cuts
# Remove existing Edge.Cuts shapes outside footprints
print("Updating Edge.Cuts shapes...")
lines = content.splitlines(keepends=True)
new_lines = []
skip = False
for line in lines:
    if '(gr_' in line and not skip:
        # Check if this gr_ block is Edge.Cuts
        # peek ahead
        pass
    new_lines.append(line)

# Let's remove all standalone (gr_line ...) and (gr_arc ...) on layer "Edge.Cuts"
content_str = "".join(new_lines)
edge_block_pattern = r'\s*\(gr_(?:line|arc)\s*\n(?:\s+\([^\n]+\n)*?\s+\(layer\s+"Edge\.Cuts"\)[\s\S]*?\n\s*\)'
content_str = re.sub(edge_block_pattern, '', content_str)

# Define our new watertight Edge.Cuts segments
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

# Insert new_edge_cuts right before the final closing paren
idx = content_str.rfind(')')
if idx != -1:
    content_str = content_str[:idx] + new_edge_cuts + "\n)\n"

# Write out the updated PCB
with open(pcb_file, 'w', encoding='utf-8') as f:
    f.write(content_str)

print("Updated foc_v2.kicad_pcb successfully!")
