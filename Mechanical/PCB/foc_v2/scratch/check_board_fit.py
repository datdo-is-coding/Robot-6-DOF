import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
import math

P = dict(s.P)
P['C63'] = (124.5, 76.0, 0, 'F.Cu')
P['L1']  = (123.5, 89.0, 0, 'F.Cu')
P['D4']  = (115.0, 92.5, 0, 'F.Cu')
P['C16'] = (114.5, 96.2, 90, 'F.Cu')
P['C17'] = (114.5, 100.2, 90, 'F.Cu')
P['R53'] = (118.0, 96.2, 0, 'F.Cu')
P['R54'] = (118.0, 98.5, 0, 'F.Cu')
P['J11'] = (122.0, 103.5, 270, 'F.Cu')
P['F1']  = (124.5, 121.5, 90, 'F.Cu')
P['D6']  = (126.5, 127.5, 0, 'F.Cu')

all_bboxes = {}
for ref, (x, y, rot, layer) in P.items():
    is_b = (layer == 'B.Cu')
    _, shapes = s.parse_shapes(s.fps[ref])
    all_bboxes[ref] = s.get_world_bbox(ref, is_b, shapes, x, y, rot)

min_x = min(b['x1'] for b in all_bboxes.values())
max_x = max(b['x2'] for b in all_bboxes.values())
min_y = min(b['y1'] for b in all_bboxes.values())
max_y = max(b['y2'] for b in all_bboxes.values())

print(f"Overall bounding box of all 124 components:")
print(f"  X: [{min_x:.2f}, {max_x:.2f}] (span = {max_x - min_x:.2f} mm)")
print(f"  Y: [{min_y:.2f}, {max_y:.2f}] (span = {max_y - min_y:.2f} mm)")

# List components at the extremes:
print("\nComponents with y1 < 70:")
for ref, b in all_bboxes.items():
    if b['y1'] < 70:
        print(f"  {ref:6s}: y1={b['y1']:.2f}, y2={b['y2']:.2f}, x=[{b['x1']:.2f}, {b['x2']:.2f}]")

print("\nComponents with y2 > 130:")
for ref, b in all_bboxes.items():
    if b['y2'] > 130:
        print(f"  {ref:6s}: y1={b['y1']:.2f}, y2={b['y2']:.2f}, x=[{b['x1']:.2f}, {b['x2']:.2f}]")

print("\nComponents with x1 < 68:")
for ref, b in all_bboxes.items():
    if b['x1'] < 68:
        print(f"  {ref:6s}: x1={b['x1']:.2f}, x2={b['x2']:.2f}, y=[{b['y1']:.2f}, {b['y2']:.2f}]")

print("\nComponents with x2 > 132:")
for ref, b in all_bboxes.items():
    if b['x2'] > 132:
        print(f"  {ref:6s}: x1={b['x1']:.2f}, x2={b['x2']:.2f}, y=[{b['y1']:.2f}, {b['y2']:.2f}]")
