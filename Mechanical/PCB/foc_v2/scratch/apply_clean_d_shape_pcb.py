import math
import sys
import re
import subprocess
import json

sys.path.insert(0, 'scratch')
from verify_all_clean import P
from flip_utils import flip_footprint_layers_to_back, flip_footprint_layers_to_front

P_clean = dict(P)

# 1. Adjust C_BUS1 to be well inside circle:
P_clean['C_BUS1'] = (84.0, 71.0, 0, 'F.Cu')

# 2. South Connectors: Front faces flush with flat cut Y = 123.50
P_clean['J8']  = (75.0, 114.30, 0, 'F.Cu')   # CAN_IN (3-pin)
P_clean['J9']  = (86.5, 114.30, 0, 'F.Cu')   # CAN_OUT (3-pin)
P_clean['J7']  = (100.0, 119.71, 0, 'F.Cu')  # Type-C
P_clean['J10'] = (111.5, 114.30, 0, 'F.Cu')  # SWD (5-pin)

# 3. CAN Bus Subsystem: Deep inside West wing
P_clean['U9']  = (76.0, 101.0, 0, 'F.Cu')
P_clean['JP1'] = (76.0, 105.0, 0, 'F.Cu')
P_clean['R45'] = (76.0, 107.5, 0, 'F.Cu')
P_clean['R46'] = (76.0, 109.5, 0, 'F.Cu')
P_clean['C60'] = (71.5, 99.0, 90, 'F.Cu')
P_clean['C61'] = (71.5, 101.5, 90, 'F.Cu')
P_clean['C62'] = (71.5, 104.0, 90, 'F.Cu')

# 4. Power Input Subsystem: Deep inside East wing
P_clean['J11'] = (120.5, 101.0, 270, 'F.Cu') # XT30
P_clean['F1']  = (122.0, 111.0, 90, 'F.Cu')   # Fuse 10A
P_clean['D6']  = (122.0, 117.0, 90, 'F.Cu')   # TVS Diode

# 5. Status LEDs & Resistors (West area X = 80.0, Y in [105 .. 112])
P_clean['D1']  = (80.0, 105.0, 0, 'F.Cu')
P_clean['R33'] = (82.5, 105.0, 0, 'F.Cu')
P_clean['D2']  = (80.0, 107.5, 0, 'F.Cu')
P_clean['R35'] = (82.5, 107.5, 0, 'F.Cu')
P_clean['D3']  = (80.0, 110.0, 0, 'F.Cu')
P_clean['R36'] = (82.5, 110.0, 0, 'F.Cu')

# 6. USB Circuit Passives on B.Cu (aligned near J7 at Y = 117.5..120.5)
P_clean['U8']  = (96.0, 118.0, 0, 'B.Cu')
P_clean['C59'] = (100.0, 117.5, 0, 'B.Cu')
P_clean['Q7']  = (104.0, 118.0, 0, 'B.Cu')
P_clean['R40'] = (95.0, 120.5, 0, 'B.Cu')
P_clean['R41'] = (98.0, 120.5, 0, 'B.Cu')
P_clean['R42'] = (102.0, 120.5, 0, 'B.Cu')
P_clean['R43'] = (105.0, 120.5, 0, 'B.Cu')

# 7. Motor wire pads (North: deep inside board, complete circular pads)
P_clean['J1'] = (88.0, 71.0, 0, 'F.Cu')
P_clean['J2'] = (100.0, 71.0, 0, 'F.Cu')
P_clean['J3'] = (112.0, 71.0, 0, 'F.Cu')

# Load foc_v2.kicad_pcb
with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update footprints
parts = text.split('(footprint ')
new_parts = [parts[0]]

for chunk in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', chunk)
    if not ref_m or ref_m.group(1) not in P_clean:
        new_parts.append(chunk)
        continue
    
    ref = ref_m.group(1)
    x, y, rot, layer = P_clean[ref]
    
    # replace (at ...)
    def repl_at(m):
        if rot == 0:
            return f"\n\t\t(at {x:.4f} {y:.4f})"
        else:
            return f"\n\t\t(at {x:.4f} {y:.4f} {rot:.1f})"
    
    chunk = re.sub(r'\n\s*\(at\s+[-\d.]+\s+[-\d.]+(?:\s+[-\d.]+)?\)', repl_at, chunk, count=1)
    
    # apply layer flip if needed
    if layer == 'B.Cu':
        chunk = flip_footprint_layers_to_back(chunk)
    else:
        chunk = flip_footprint_layers_to_front(chunk)
        
    new_parts.append(chunk)

new_text = "(footprint ".join(new_parts)

# 2. Update Edge.Cuts to Pure D-Shape:
# Remove all existing gr_line and gr_arc on Edge.Cuts
new_text = re.sub(
    r'\t\(gr_(?:line|arc)\n(?:\t\t[^\n]+\n)*?\t\t\(layer "Edge\.Cuts"\)\n(?:\t\t[^\n]+\n)*?\t\)\n?',
    '',
    new_text
)

# Mathematical D-Shape:
# Center: (100, 100), R = 35.0 mm.
# Flat cut: Y = 123.5 mm.
# dy = 23.5 => dx = sqrt(35^2 - 23.5^2) = 25.93742 mm.
# Left: (74.0626, 123.5)
# Right: (125.9374, 123.5)

d_shape_edge_cuts = """\t(gr_line
\t\t(start 74.0626 123.5)
\t\t(end 125.9374 123.5)
\t\t(stroke
\t\t\t(width 0.05)
\t\t\t(type default)
\t\t)
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-south-chord-line")
\t)
\t(gr_arc
\t\t(start 125.9374 123.5)
\t\t(mid 100 65)
\t\t(end 74.0626 123.5)
\t\t(stroke
\t\t\t(width 0.05)
\t\t\t(type default)
\t\t)
\t\t(layer "Edge.Cuts")
\t\t(uuid "edge-circular-arc-r35")
\t)
"""

# Insert before final closing parenthesis
if new_text.rstrip().endswith(')'):
    idx = new_text.rfind(')')
    new_text = new_text[:idx] + d_shape_edge_cuts + ")\n"

# Clean up any misplaced silk text
new_text = re.sub(
    r'\t\(gr_text "SWD"\n\t\t\(at 89 69\.2 0\)\n\t\t\(layer "B\.SilkS"\)[\s\S]*?\t\)\n?',
    '',
    new_text
)

with open('foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Saved clean D-shape foc_v2.kicad_pcb successfully!")
