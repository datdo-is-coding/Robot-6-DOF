import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

for ref in sorted(s.P.keys()):
    if ref.startswith('J') or ref.startswith('TP'):
        fp_name = s.fps[ref][0].strip()
        print(f"{ref:6s}: {fp_name} at {s.P[ref]}")
