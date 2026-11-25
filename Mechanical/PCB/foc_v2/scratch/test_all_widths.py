import math

cx, cy = 100.0, 100.0
r_board = 35.0
holes = [
    (115.556, 115.556, "H1"),
    (84.444, 115.556, "H2"),
    (84.444, 84.444, "H3"),
    (115.556, 84.444, "H4")
]
hole_r = 2.95

def collides_hole(box):
    for hx, hy, name in holes:
        cx_box = max(box[0], min(hx, box[1]))
        cy_box = max(box[2], min(hy, box[3]))
        if math.sqrt((hx - cx_box)**2 + (hy - cy_box)**2) < hole_r:
            return True
    return False

def inside_circle(box, max_r=34.6):
    for x in [box[0], box[1]]:
        for y in [box[2], box[3]]:
            if math.sqrt((x - cx)**2 + (y - cy)**2) > max_r:
                return False
    return True

def overlaps(b1, b2, margin=0.5):
    if b1[1] + margin < b2[0] or b2[1] + margin < b1[0]:
        return False
    if b1[3] + margin < b2[2] or b2[3] + margin < b1[2]:
        return False
    return True

# J8/J9 (3-pin XH right angle): w=10.51, h=11.61 (if facing S: x in [-5.06, 5.45], y in [-11.61, 0])
# J10 (5-pin XH right angle): w=15.51, h=11.61 (if facing S: x in [-7.56, 7.95], y in [-11.61, 0])
# J7 (Type-C): w=10.64, h=9.03 (if facing S: x in [-5.32, 5.32], y in [-9.03, 0])

# What if all 4 face South?
# Total width = 10.51 + 10.51 + 15.51 + 10.64 = 47.17 mm!
# If there is a flat cut at y_cut:
# What y_cut allows a width of at least 47.17 + margins?
# At y_cut, the width is 2 * sqrt(35^2 - (y_cut - 100)^2)
for y_cut in [115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]:
    dy = y_cut - 100.0
    w = 2 * math.sqrt(35**2 - dy**2)
    print(f"y_cut={y_cut}: available chord width = {w:.2f} mm")
