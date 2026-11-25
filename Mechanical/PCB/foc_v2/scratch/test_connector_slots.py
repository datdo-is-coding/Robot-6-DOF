import math

# We have 4 connectors:
# J8: 3-pin XH. Width = 10.12 mm. Pin 1 to Pin 3 = 5.0 mm. Local X in [-2.56, 7.56].
# J9: 3-pin XH. Width = 10.12 mm.
# J10: 5-pin XH. Width = 15.12 mm. Pin 1 to Pin 5 = 10.0 mm. Local X in [-2.56, 12.56].
# J7: Type-C. Width = 10.64 mm. Local X in [-5.32, 5.32].

# Let's write functions to get the world bounding box:
# When placed at (px, py, rot=0):
def bbox_xh3(px, py):
    # px is pin 1. py is pin row.
    # X in [px - 2.56, px + 7.56]
    # Y in [py - 2.41, py + 9.31]
    return (px - 2.56, px + 7.56, py - 2.41, py + 9.31)

def bbox_xh5(px, py):
    # px is pin 1. py is pin row.
    # X in [px - 2.56, px + 12.56]
    # Y in [py - 2.41, py + 9.31]
    return (px - 2.56, px + 12.56, py - 2.41, py + 9.31)

def bbox_typec(px, py):
    # px is center. py is at (where front edge is py + 3.79, crtyd py + 4.18)
    return (px - 5.32, px + 5.32, py - 4.85, py + 4.18)

# Check distance from box to point (hx, hy)
def dist_box_point(x1, x2, y1, y2, hx, hy):
    cx = max(x1, min(hx, x2))
    cy = max(y1, min(hy, y2))
    return math.hypot(cx - hx, cy - hy)

# Check all 4 corners of box inside circle (100, 100), R=35 and Y <= y_edge
def box_in_board(x1, x2, y1, y2, y_edge, r_board=35.0):
    if y2 > y_edge + 0.05:
        return False, f"y2={y2:.2f} > y_edge={y_edge:.2f}"
    for x in [x1, x2]:
        for y in [y1, y2]:
            d = math.hypot(x - 100.0, y - 100.0)
            if d > r_board:
                return False, f"corner ({x:.2f}, {y:.2f}) dist={d:.2f} > {r_board}"
    return True, "OK"

# Test a configuration:
# For front flush at Y_edge:
# XH pin row py = Y_edge - 9.31
# Type-C py = Y_edge - 4.00 (so front is flush at Y_edge)
y_edge = 120.0
py_xh = y_edge - 9.31
py_typec = y_edge - 4.00

# Let's inspect the available X ranges:
# At y_edge = 120.0: X in [71.28, 128.72].
# H2 is at (84.444, 115.556), H1 is at (115.556, 115.556).
# If screw head R = 2.40 mm:
# H2 forbidden X near Y=115.556 is [84.444 - 2.40, 84.444 + 2.40] = [82.04, 86.84].
# H1 forbidden X near Y=115.556 is [115.556 - 2.40, 115.556 + 2.40] = [113.16, 117.96].

# Available X slots:
# West slot (left of H2): X in [71.5, 82.0] -> width = 10.5 mm!
# Middle slot (between H2 and H1): X in [86.9, 113.1] -> width = 26.2 mm!
# East slot (right of H1): X in [118.0, 128.5] -> width = 10.5 mm!

print(f"Slot 1 (West): [71.5, 82.0] width = 10.5 mm")
print(f"Slot 2 (Mid):  [86.9, 113.1] width = 26.2 mm")
print(f"Slot 3 (East): [118.0, 128.5] width = 10.5 mm")
