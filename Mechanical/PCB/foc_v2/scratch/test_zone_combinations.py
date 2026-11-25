import math

cx, cy = 100.0, 100.0
r_board = 35.0
holes = [
    (115.556, 115.556, "H1"),
    (84.444, 115.556, "H2")
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

connectors = {
    'J7': {'w': 10.64, 'dl': 5.32, 'dr': 5.32, 'h': 9.03, 'y_pad_offset': -3.80},
    'J8': {'w': 10.51, 'dl': 5.06, 'dr': 5.45, 'h': 11.61, 'y_pad_offset': -9.20},
    'J9': {'w': 10.51, 'dl': 5.06, 'dr': 5.45, 'h': 11.61, 'y_pad_offset': -9.20},
    'J10': {'w': 15.51, 'dl': 7.56, 'dr': 7.95, 'h': 11.61, 'y_pad_offset': -9.20}
}

# Let's test if J8 is in Zone 1, (J7, J9) in Zone 2, J10 in Zone 3 or similar:
# Or what if (J8, J9) in Zone 2 (Center)?
# J8 width = 10.51, J9 width = 10.51 -> sum = 21.02 mm!
# Zone 2 width = 25.20 mm!
# 25.20 - 21.02 = 4.18 mm of free margin!
# J8 and J9 fit TOGETHER in Zone 2 with 4.18 mm of margin!
print("Testing J8 + J9 together in Zone 2 (Center):")
# CAN_IN and CAN_OUT side by side in the center! That is SO LOGICAL for daisy chaining!
# Then J7 (Type-C) in Zone 1? Width 10.64 mm in Zone 1 [68.5, 81.5] (width 13.0 mm):
# And J10 (SWD) in Zone 3? Wait, J10 width is 15.51 mm, does 15.51 mm fit in Zone 3?
# Let's check!
b10 = (118.8, 118.8 + 15.51, 120.0 - 11.61, 120.0)
print("J10 in Zone 3: inside_circle?", inside_circle(b10))
