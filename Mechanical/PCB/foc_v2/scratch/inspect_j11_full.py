import sys
sys.path.insert(0, 'scratch')
import solve_final_zero_conflicts as s

print("J11 footprint lines:")
for l in s.fps['J11']:
    print(" ", l.strip())
