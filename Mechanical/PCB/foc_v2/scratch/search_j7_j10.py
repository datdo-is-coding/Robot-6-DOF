import math

h2 = (84.444, 115.556)
h1 = (115.556, 115.556)
hole_r = 2.95

# J7 box when origin is (x7, y7_orig):
# x in [x7 - 5.32, x7 + 5.32]
# y in [y7_orig - 4.85, y7_orig + 4.18]
# J10 box when pad1 is at (x10, y10_pad):
# x in [x10 - 2.56, x10 + 12.95]
# y in [y10_pad - 2.41, y10_pad + 9.20]

def dist_box_circle(box, circle_center):
    cx, cy = circle_center
    closest_x = max(box[0], min(cx, box[1]))
    closest_y = max(box[2], min(cy, box[3]))
    return math.hypot(cx - closest_x, cy - closest_y)

print("Testing exact distance between H2, H1 and (J7, J10)...")
# Let y_front = 120.0 mm
y7_orig = 120.0 - 4.18 # = 115.82
y10_pad = 120.0 - 9.20 # = 110.80

# Can we find x7 and x10 such that:
# dist_box_circle(box7, h2) >= hole_r
# dist_box_circle(box10, h1) >= hole_r
# box7[1] <= box10[0] (no overlap between J7 and J10)
# Let's search!

found = []
for x7 in [round(85.0 + i * 0.1, 2) for i in range(150)]:
    b7 = (x7 - 5.32, x7 + 5.32, y7_orig - 4.85, y7_orig + 4.18)
    d7_h2 = dist_box_circle(b7, h2)
    if d7_h2 < hole_r: continue
    
    # x10 must be >= b7[1] + 2.56
    min_x10 = b7[1] + 2.56
    for x10 in [round(min_x10 + j * 0.1, 2) for j in range(50)]:
        b10 = (x10 - 2.56, x10 + 12.95, y10_pad - 2.41, y10_pad + 9.20)
        d10_h1 = dist_box_circle(b10, h1)
        if d10_h1 >= hole_r:
            found.append((x7, x10, d7_h2, d10_h1, b10[0] - b7[1]))

print(f"Solutions where J7 and J10 both fit in center: {len(found)}")
if found:
    for x7, x10, d7, d10, gap in found[:10]:
        print(f"  x7={x7:.2f}, x10={x10:.2f}, dist_H2={d7:.3f}, dist_H1={d10:.3f}, gap={gap:.3f}")
