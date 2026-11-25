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

def inside_circle(box):
    for x in [box[0], box[1]]:
        for y in [box[2], box[3]]:
            if math.sqrt((x - cx)**2 + (y - cy)**2) > 34.5:
                return False
    return True

# Can J10 (SWD 5-pin, w=15.51, h=11.61) fit anywhere?
# What are the dimensions of J10?
# In horizontal orientation (pins at y, body y..y+9.31):
# w=15.51, h=11.61
# In vertical orientation (pins at x, body x..x+9.31 or x-9.31..x):
# w=11.61, h=15.51

# Let's test if J10 can fit in the central corridor [87.40, 112.60] (width 25.20):
# J10 width is 15.51.
# 25.20 - 15.51 = 9.69 mm of free space left in the center!
# Can J7 (width 10.64) fit next to J10? 10.64 > 9.69, so NO, not side-by-side!

print("Testing J10 in center corridor:")
for x10 in [88.0 + 7.56, 112.0 - 7.95, 100.0]:
    # x10 is center of J10
    box10 = (x10 - 7.56, x10 + 7.95, 114.30 - 2.41, 114.30 + 9.20)
    print(f"x10={x10:.1f}: box={box10}, collides_hole={collides_hole(box10)}, inside_circle={inside_circle(box10)}")
