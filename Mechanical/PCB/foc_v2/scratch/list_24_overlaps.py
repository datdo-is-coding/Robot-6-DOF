import sys
sys.path.insert(0, 'scratch')
import test_refined_zero as trz

print(f"Total overlaps in test_refined_zero: {len(trz.overlaps)}")
for r1, r2, dx, dy, b1, b2 in trz.overlaps:
    p1 = trz.P[r1]
    p2 = trz.P[r2]
    print(f"  {r1:6s} at ({p1[0]:6.2f}, {p1[1]:6.2f}) <--> {r2:6s} at ({p2[0]:6.2f}, {p2[1]:6.2f}) : dx={dx:.2f}, dy={dy:.2f}")
