import math

# H4 is at (115.5563, 84.4437), radius with screw envelope = 2.40 + 0.50 = 2.90 mm
# F1 top is at Y = 91.79 for X in [116.68, 123.92] (if at 122.0, 105.0, 90)
# D4 courtyard: half_w = 3.5, half_h = 1.75
# Let's find valid (x, y) for D4:

h4_x, h4_y = 115.5563, 84.4437
h4_r = 2.90

candidates = []
for y in [89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0]:
    for x in [108.0, 109.0, 110.0, 111.0, 112.0, 113.0, 114.0]:
        # check distance to H4
        # D4 box: [x-3.5, x+3.5], [y-1.75, y+1.75]
        # closest point to (h4_x, h4_y)
        cx = max(x - 3.5, min(h4_x, x + 3.5))
        cy = max(y - 1.75, min(h4_y, y + 1.75))
        dist_h4 = math.hypot(cx - h4_x, cy - h4_y)
        
        # distance to F1 box (X in [116.68, 123.92], Y in [91.79, 108.29])
        f1_x1, f1_x2, f1_y1, f1_y2 = 116.68, 123.92, 91.79, 108.29
        f1_cx = max(f1_x1, min(cx, f1_x2))
        f1_cy = max(f1_y1, min(cy, f1_y2))
        # check overlap with F1
        overlap_f1 = not (x + 3.5 <= f1_x1 or x - 3.5 >= f1_x2 or y + 1.75 <= f1_y1 or y - 1.75 >= f1_y2)
        
        # check circle R <= 35 from (100, 100)
        # corners of D4
        corners = [(x-3.5, y-1.75), (x+3.5, y-1.75), (x-3.5, y+1.75), (x+3.5, y+1.75)]
        max_r = max(math.hypot(px-100, py-100) for px, py in corners)
        
        if dist_h4 >= 0.5 and not overlap_f1 and max_r <= 34.0:
            candidates.append((dist_h4, x, y, max_r))

candidates.sort(reverse=True)
for c in candidates[:10]:
    print(f"Dist_H4: {c[0]:.2f} mm | Pos: ({c[1]:.1f}, {c[2]:.1f}) | Max_R: {c[3]:.2f} mm")
