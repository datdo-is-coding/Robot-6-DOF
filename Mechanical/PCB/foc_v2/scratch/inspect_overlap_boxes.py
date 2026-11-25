import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s
for ref in ['J11', 'F1', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'D6']:
    b = s.bboxes[ref]
    print(f"{ref:6s}: x=[{b['x1']:6.2f}, {b['x2']:6.2f}], y=[{b['y1']:6.2f}, {b['y2']:6.2f}]")
