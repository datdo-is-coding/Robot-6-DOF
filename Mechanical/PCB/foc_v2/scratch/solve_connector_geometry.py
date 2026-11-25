import math

# Center of board
cx, cy = 100.0, 100.0
r_board = 35.0

# Holes
holes = [
    (115.556, 115.556, "H1"),
    (84.444, 115.556, "H2"),
    (84.444, 84.444, "H3"),
    (115.556, 84.444, "H4")
]
hole_r = 3.0 # keepout radius

def check_hole_collision(box, hole):
    # box is (xmin, xmax, ymin, ymax)
    hx, hy, name = hole
    # closest point in box to (hx, hy)
    closest_x = max(box[0], min(hx, box[1]))
    closest_y = max(box[2], min(hy, box[3]))
    dist = math.sqrt((hx - closest_x)**2 + (hy - closest_y)**2)
    return dist < hole_r

def check_board_boundary(box, y_cut):
    # all 4 corners must be inside circle (r <= r_board - 0.2) and y <= y_cut
    for x in [box[0], box[1]]:
        for y in [box[2], box[3]]:
            if y > y_cut:
                return False
            if math.sqrt((x - cx)**2 + (y - cy)**2) > (r_board - 0.2):
                return False
    return True

# Connector local boxes relative to (x_center, y_front):
# For JST XH 3-pin:
# width = 10.51, depth = 11.61
# x in [-5.06, +5.45], y in [-11.61, 0.0]
# For JST XH 5-pin:
# width = 15.51, depth = 11.61
# x in [-7.56, +7.95], y in [-11.61, 0.0]
# For Type-C (J7):
# width = 10.64, depth = 9.03
# x in [-5.32, +5.32], y in [-9.03, 0.0]

print("Scanning possible Y_cut and connector configurations...")
# Let's test different orientations or placement options
# What if J8 and J9 are 3-pin XH, J10 is 5-pin XH, J7 is Type-C:
