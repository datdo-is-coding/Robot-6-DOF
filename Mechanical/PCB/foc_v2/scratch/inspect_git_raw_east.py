import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's inspect where F1, J11, L1, D4 were in git_raw:
with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
parts = text.split('(footprint ')
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m and ref_m.group(1) in ['J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58']:
        ref = ref_m.group(1)
        at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', p)
        print(f"{ref:5s}: {at_m.group(0)}")
