import math

# Circle: center (100, 100), R = 35.0 mm
# Flat cut: Y = y_cut
# Inside board means:
# For all points (x, y) of the component:
# 1. (x - 100)^2 + (y - 100)^2 <= 35.0^2  (inside the circle!)
# 2. y <= y_cut                           (above the flat cut!)

def point_inside_board(x, y, y_cut):
    if y > y_cut:
        return False
    return (x - 100.0)**2 + (y - 100.0)**2 <= 35.0**2

def box_inside_board(x1, y1, x2, y2, y_cut):
    # check all 4 corners:
    # also if corners are inside, since circle is convex, all points between corners are inside!
    # Wait, the flat cut is a straight line, so if all 4 corners are inside the circle and <= y_cut,
    # the entire rectangle is inside the board!
    for x in [x1, x2]:
        for y in [y1, y2]:
            if not point_inside_board(x, y, y_cut):
                return False
    return True

def rect_circle_overlap(rx1, ry1, rx2, ry2, cx, cy, r):
    qx = max(rx1, min(cx, rx2))
    qy = max(ry1, min(cy, ry2))
    return math.hypot(cx - qx, cy - qy) < r

H2 = (84.444, 115.556, 2.95)
H1 = (115.556, 115.556, 2.95)

# Test J8 (3-pin XH) placed at x_orig, with front face at y_cut:
# J8 crtyd: [x_orig - 2.95, x_orig + 7.95] x [y_orig - 2.81, y_orig + 9.70]
# where y_orig = y_cut - 9.20
# So y1 = y_cut - 12.01, y2 = y_cut + 0.50. Wait! y2 = y_cut + 0.50 is 0.5mm past y_cut!
# In KiCad, courtyard of a connector can be flush with edge (or 0.2mm inside edge).
# If we set front of courtyard at y_cut:
# y2 = y_cut => y_orig = y_cut - 9.70!
# Then y1 = y_orig - 2.81 = y_cut - 12.51.
# And front face of connector is at y_orig + 9.20 = y_cut - 0.50 (0.5 mm inside board, perfect!)

print("Testing J8 to the left of H2:")
for y_cut in [123.0, 123.5, 124.0, 124.5, 125.0]:
    y_orig = y_cut - 9.70
    y1 = y_orig - 2.81
    y2 = y_cut
    for x_orig in [73.0, 73.5, 74.0, 74.5, 75.0, 75.5, 76.0]:
        x1 = x_orig - 2.95
        x2 = x_orig + 7.95
        in_board = box_inside_board(x1, y1, x2, y2, y_cut)
        col_h2 = rect_circle_overlap(x1, y1, x2, y2, H2[0], H2[1], H2[2])
        d_h2 = math.hypot(H2[0] - max(x1, min(H2[0], x2)), H2[1] - max(y1, min(H2[1], y2)))
        # check pad 1, 2, 3:
        # pad 1 is at x_orig, pad 2 at x_orig+2.5, pad 3 at x_orig+5.0, y=y_orig
        pad_in_board = all(point_inside_board(x_orig + p*2.5, y_orig, y_cut) for p in [0, 1, 2])
        if in_board and not col_h2:
            print(f"  MATCH: y_cut={y_cut:.1f}, x_orig={x_orig:.1f}: X=[{x1:.2f}, {x2:.2f}], Y=[{y1:.2f}, {y2:.2f}], dist_H2={d_h2:.2f}mm")
