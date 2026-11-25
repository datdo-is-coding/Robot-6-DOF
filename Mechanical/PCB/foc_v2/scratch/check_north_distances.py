import math
import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

# Load fast search east positions
from fast_search_east import P, all_bboxes

print("Checking distance to center (100, 100) for North components:")
for ref in ['J1', 'J2', 'J3', 'C_BUS1', 'C_BUS2', 'C_BUS3', 'C_BULK1', 'C63']:
    b = all_bboxes[ref]
    corners = [(b['x1'], b['y1']), (b['x2'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y2'])]
    max_d = max(math.hypot(x - 100.0, y - 100.0) for x, y in corners)
    print(f"{ref:8s}: pos={P[ref][:2]}, max corner dist to (100,100) = {max_d:.2f} mm")
