import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

print("Components on B.Cu:")
for ref, (x, y, rot, layer) in s.P.items():
    if layer == 'B.Cu':
        print(f"  {ref:6s}: at ({x}, {y})")
