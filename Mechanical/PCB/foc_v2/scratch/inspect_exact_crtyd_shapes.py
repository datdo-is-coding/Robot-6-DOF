import math, sys
sys.path.insert(0, 'scratch')
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's inspect J7 and J10 courtyard shapes directly
_, s7 = parse_shapes(fps['J7'])
_, s10 = parse_shapes(fps['J10'])

print("J7 shapes:")
for sh in s7:
    print(" ", sh)

print("J10 shapes:")
for sh in s10:
    print(" ", sh)
