import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
cx, cy = 100.0, 100.0
r = 35.0

# Print the bounding box of F1 at rot=0, 90, 180, 270
_, shapes = parse_shapes(fps['F1'])
for rot in [0, 90, 180, 270]:
    b = get_world_bbox('F1', False, shapes, 0, 0, rot)
    print(f"F1 at rot={rot}: w={b['w']:.2f}, h={b['h']:.2f}, X=[{b['x1']:.2f}, {b['x2']:.2f}], Y=[{b['y1']:.2f}, {b['y2']:.2f}]")
