import math, re, json, sys
sys.path.insert(0, 'scratch')
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's write an optimizer that takes P from test_refined_zero
# and searches for zero overlaps, zero hole collisions, and zero out-of-bounds
import test_refined_zero as trz

P_base = dict(trz.P)
ALLOWED = trz.ALLOWED
HOLES = trz.HOLES
R_KO = 2.95

# Let's inspect the exact bounding boxes of all components in P_base
bboxes = {}
for ref, (x, y, rot, layer) in P_base.items():
    is_b = (layer == 'B.Cu')
    _, shapes = parse_shapes(fps[ref])
    bboxes[ref] = get_world_bbox(ref, is_b, shapes, x, y, rot)

print(f"Loaded {len(bboxes)} bounding boxes.")
