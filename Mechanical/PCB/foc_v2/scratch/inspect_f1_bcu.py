from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')
is_b, shapes = parse_shapes(fps['F1'])
b = get_world_bbox('F1', True, shapes, 122.0, 105.0, 90)
print("F1 on B.Cu at (122, 105, rot=90):", b)
corners = [(b['x1'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y1']), (b['x2'], b['y2'])]
import math
print("Corners max dist:", max(math.hypot(x-100, y-100) for x, y in corners))
