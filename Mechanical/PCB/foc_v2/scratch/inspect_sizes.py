import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

refs = ['C63', 'J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58']
for ref in refs:
    _, shapes = s.parse_shapes(s.fps[ref])
    for rot in [0, 90, 270]:
        box = s.get_world_bbox(ref, False, shapes, 0, 0, rot)
        print(f"{ref:6s} rot={rot:3d}: w={box['w']:5.2f}, h={box['h']:5.2f}, lx=[{box['x1']:6.2f}, {box['x2']:6.2f}], ly=[{box['y1']:6.2f}, {box['y2']:6.2f}]")
