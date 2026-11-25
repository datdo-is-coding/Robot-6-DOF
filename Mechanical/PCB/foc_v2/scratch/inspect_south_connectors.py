import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

for ref in ['J8', 'J9', 'J7', 'J10']:
    b = s.bboxes[ref]
    print(f"{ref:6s}: x=[{b['x1']:6.2f}, {b['x2']:6.2f}], y=[{b['y1']:6.2f}, {b['y2']:6.2f}]")
