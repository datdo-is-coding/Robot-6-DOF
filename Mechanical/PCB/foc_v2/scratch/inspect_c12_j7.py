import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

# Inspect C12 and IC1
_, ic1_shapes = s.parse_shapes(s.fps['IC1'])
b_ic1 = s.get_world_bbox('IC1', False, ic1_shapes, 100.0, 93.5, 0)
print(f"IC1 box: x=[{b_ic1['x1']:.2f}, {b_ic1['x2']:.2f}], y=[{b_ic1['y1']:.2f}, {b_ic1['y2']:.2f}]")

_, c12_shapes = s.parse_shapes(s.fps['C12'])
x, y, rot, layer = s.P['C12']
b_c12 = s.get_world_bbox('C12', False, c12_shapes, x, y, rot)
print(f"C12 at ({x}, {y}, {rot}): box: x=[{b_c12['x1']:.2f}, {b_c12['x2']:.2f}], y=[{b_c12['y1']:.2f}, {b_c12['y2']:.2f}]")

# Inspect J7 B.CrtYd
_, j7_shapes = s.parse_shapes(s.fps['J7'])
b_j7_f = s.get_world_bbox('J7', False, j7_shapes, 100.0, 128.0, 0)
b_j7_b = s.get_world_bbox('J7', True, j7_shapes, 100.0, 128.0, 0)
print(f"J7 F.CrtYd: x=[{b_j7_f['x1']:.2f}, {b_j7_f['x2']:.2f}], y=[{b_j7_f['y1']:.2f}, {b_j7_f['y2']:.2f}]")
print(f"J7 B.CrtYd: x=[{b_j7_b['x1']:.2f}, {b_j7_b['x2']:.2f}], y=[{b_j7_b['y1']:.2f}, {b_j7_b['y2']:.2f}]")
