import math
import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

_, j11_shapes = s.parse_shapes(s.fps['J11'])

cx, cy = 100.0, 100.0
R = 35.0

print("Testing J11 at rot=270 (socket facing East) inside circle R=35mm:")
for x in [119.5, 120.0, 120.5, 121.0, 121.5]:
    for y in [98.0, 99.0, 100.0, 101.0, 102.0]:
        box = s.get_world_bbox('J11', False, j11_shapes, x, y, 270)
        corners = [(box['x1'], box['y1']), (box['x2'], box['y1']), (box['x1'], box['y2']), (box['x2'], box['y2'])]
        max_d = max(math.hypot(px - cx, py - cy) for px, py in corners)
        inside = (max_d <= R)
        if inside:
            print(f"  J11 at ({x:.1f}, {y:.1f}): max_dist = {max_d:.2f} mm <= {R} mm (MARGIN = {R - max_d:.2f} mm)")
