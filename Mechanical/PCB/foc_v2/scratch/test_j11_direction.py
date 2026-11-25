import math

# In KiCad 6+:
# angle theta is in degrees clockwise because Y axis points DOWN (+Y is south).
# x_world = x0 + px * cos(a) - py * sin(a)
# y_world = y0 + px * sin(a) + py * cos(a)

def get_world(x0, y0, rot_deg, px, py):
    rad = math.radians(rot_deg)
    c = math.cos(rad)
    s = math.sin(rad)
    return x0 + px * c - py * s, y0 + px * s + py * c

# For J11:
# local lines: X in [-9.65, 4.65], Y in [-13.60, 2.25]
# local pads:
# pad 1: (0, 0)
# pad 2: (-5, 0)
# mounting hole 1: (-8, -10)
# mounting hole 2: (3, -10)

rot = -90 # or 270
# With rot = -90:
# cos(-90) = 0, sin(-90) = -1
# x_world = x0 - py * (-1) = x0 + py
# y_world = y0 + px * (-1) = y0 - px
# Look at that:
# local py in [-13.60, 2.25]
# x_world = x0 + py => x_world in [x0 - 13.60, x0 + 2.25]
# WAIT!
# If x_world in [x0 - 13.60, x0 + 2.25], then the front (py = -13.60) is at x0 - 13.60 (WEST)!
# That means it points WEST into the board, NOT East!
# Let's check!
print("rot = -90:")
for py in [-13.60, 2.25]:
    for px in [-9.65, 4.65]:
        xw, yw = get_world(122, 100, -90, px, py)
        print(f"  local ({px}, {py}) -> world ({xw:.2f}, {yw:.2f})")

print("\nrot = 90:")
for py in [-13.60, 2.25]:
    for px in [-9.65, 4.65]:
        xw, yw = get_world(122, 100, 90, px, py)
        print(f"  local ({px}, {py}) -> world ({xw:.2f}, {yw:.2f})")
