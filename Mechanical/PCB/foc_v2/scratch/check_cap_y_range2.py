import sys
sys.path.insert(0, 'scratch')
import find_cap_positions as f
import itertools

valid_left_y = [p for p in f.valid_left if 76 <= p[1] <= 88]
for y, group in itertools.groupby(sorted(valid_left_y, key=lambda p: p[1]), key=lambda p: p[1]):
    pts = list(group)
    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    print(f"y = {y:4.1f}: valid x in [{min_x:4.1f}, {max_x:4.1f}]")
