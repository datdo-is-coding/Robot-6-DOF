import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

# Let's inspect where J11, F1, D6, L1, D4, U10 can fit on F.Cu
# Let's test a concrete layout in scratch/test_east_combos.py
