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

def overlaps(b1, b2, margin=0.5):
    if b1[1] + margin < b2[0] or b2[1] + margin < b1[0]:
        return False
    if b1[3] + margin < b2[2] or b2[3] + margin < b1[2]:
        return False
    return True

# Let's search all permutations of order of connectors [c1, c2, c3, c4]
# where connectors are:
# 'J7': w=10.64, d=9.03, front=y_cut, box=(x-5.32, x+5.32, y_cut-9.03, y_cut)
# 'J8': w=10.51, d=11.61, front=y_cut, box=(x-5.06, x+5.45, y_cut-11.61, y_cut)
# 'J9': w=10.51, d=11.61, front=y_cut, box=(x-5.06, x+5.45, y_cut-11.61, y_cut)
# 'J10': w=15.51, d=11.61, front=y_cut, box=(x-7.56, x+7.95, y_cut-11.61, y_cut)

import itertools

connectors = {
    'J7': {'w': 10.64, 'dl': 5.32, 'dr': 5.32, 'h': 9.03},
    'J8': {'w': 10.51, 'dl': 5.06, 'dr': 5.45, 'h': 11.61},
    'J9': {'w': 10.51, 'dl': 5.06, 'dr': 5.45, 'h': 11.61},
    'J10': {'w': 15.51, 'dl': 7.56, 'dr': 7.95, 'h': 11.61}
}

valid_solutions = []

for y_cut in [118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5, 124.0]:
    for order in itertools.permutations(['J8', 'J9', 'J7', 'J10']):
        # We want to place them left to right along x
        # Try different spacings and centerings
        # Let x1 be in range [70, 85] with step 0.5
        for x1 in [round(v * 0.5, 1) for v in range(140, 175)]:
            boxes = {}
            cur_x = x1
            possible = True
            for name in order:
                c = connectors[name]
                # center of this connector
                cx_c = cur_x + c['dl']
                box = (cx_c - c['dl'], cx_c + c['dr'], y_cut - c['h'], y_cut)
                if collides_hole(box) or not inside_circle(box):
                    possible = False
                    break
                boxes[name] = (cx_c, box)
                cur_x = cx_c + c['dr'] + 0.8 # 0.8 mm gap between connectors
            
            if possible:
                valid_solutions.append((y_cut, order, boxes))

print(f"Total valid solutions found: {len(valid_solutions)}")
if valid_solutions:
    # sort by symmetry around x=100
    def symmetry_cost(sol):
        y_cut, order, boxes = sol
        xs = [b[0] for b in boxes.values()]
        mid = (min(xs) + max(xs)) / 2.0
        return abs(mid - 100.0)
    
    valid_solutions.sort(key=symmetry_cost)
    for y_cut, order, boxes in valid_solutions[:10]:
        print(f"y_cut={y_cut}, order={order}:")
        for name in order:
            cx_c, b = boxes[name]
            print(f"  {name:5s}: center_x={cx_c:6.2f}, box X [{b[0]:6.2f}, {b[1]:6.2f}]")
