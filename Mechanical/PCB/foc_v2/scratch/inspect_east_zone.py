import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

print("Components on top layer with x2 > 108:")
for ref, b in sorted(s.bboxes.items(), key=lambda item: item[1]['y1']):
    if b['x2'] > 108 and b['layer'] == 'top':
        print(f"{ref:6s}: x=[{b['x1']:6.2f}, {b['x2']:6.2f}], y=[{b['y1']:6.2f}, {b['y2']:6.2f}] (pos={s.P[ref]})")
