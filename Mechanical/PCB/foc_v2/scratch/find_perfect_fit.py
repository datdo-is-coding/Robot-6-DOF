import math

cx, cy = 100.0, 100.0
r_board = 35.0

# 4 holes at PCD 44mm (r = 22.0mm)
# H1: (115.556, 115.556), H2: (84.444, 115.556)
h1_x, h1_y = 115.556, 115.556
h2_x, h2_y = 84.444, 115.556
hole_r = 2.95

def collides_hole(box):
    for hx, hy in [(h1_x, h1_y), (h2_x, h2_y)]:
        cx_box = max(box[0], min(hx, box[1]))
        cy_box = max(box[2], min(hy, box[3]))
        if math.hypot(hx - cx_box, hy - cy_box) < hole_r:
            return True
    return False

def inside_board(box, y_cut):
    for px in [box[0], box[1]]:
        for py in [box[2], box[3]]:
            if py > y_cut + 0.05:
                return False
            if math.hypot(px - cx, py - cy) > (r_board - 0.2):
                return False
    return True

# Connector geometries when facing South (mating face flush at y_front = y_cut):
# J7 (Type-C):
#   origin: (x, y_cut - 4.18)
#   box: (x - 5.32, x + 5.32, y_cut - 9.03, y_cut)
# J8 / J9 (3-pin XH right angle):
#   origin: (x_pad1, y_cut - 9.20)
#   box: (x_pad1 - 2.56, x_pad1 + 7.95, y_cut - 11.61, y_cut)
#   Note: width = 10.51, pad1 is at x_box_left + 2.56
# J10 (5-pin XH right angle):
#   origin: (x_pad1, y_cut - 9.20)
#   box: (x_pad1 - 2.56, x_pad1 + 12.95, y_cut - 11.61, y_cut)
#   Note: width = 15.51, pad1 is at x_box_left + 2.56

# What if connectors are NOT all facing South?
# User prompt: "các cổng kết nối hãy đặt thẳng hàng nhau, tránh để lung tung không có hàng lối"
# If they are placed along the flat cut, they all face South!

# Let's search over y_cut and x positions:
# Order of 4 connectors from left to right:
# Let's test all 24 permutations of ['J8', 'J9', 'J7', 'J10']
import itertools

results = []
conns_spec = {
    'J7':  {'w': 10.64, 'h': 9.03,  'dl': 5.32, 'dr': 5.32},
    'J8':  {'w': 10.51, 'h': 11.61, 'dl': 2.56, 'dr': 7.95},
    'J9':  {'w': 10.51, 'h': 11.61, 'dl': 2.56, 'dr': 7.95},
    'J10': {'w': 15.51, 'h': 11.61, 'dl': 2.56, 'dr': 12.95}
}

for y_cut in [118.0, 118.5, 119.0, 119.5, 120.0, 120.2, 120.5, 121.0, 121.5, 122.0, 122.5, 123.0, 123.5]:
    for perm in itertools.permutations(['J8', 'J9', 'J7', 'J10']):
        # We need to find x positions for perm[0], perm[1], perm[2], perm[3]
        # Let x_left_edge of perm[0] be x0
        # Then perm[1] starts at x1 >= x0 + w0 + 0.5
        # perm[2] starts at x2 >= x1 + w1 + 0.5
        # perm[3] starts at x3 >= x2 + w2 + 0.5
        # But notice: between H2 and H1 is the center corridor [87.40, 112.60].
        # Left of H2 is [x_min, 81.49].
        # Right of H1 is [118.51, x_max].
        
        # Possible assignments of the 4 connectors to the 3 zones:
        # Configuration A: 1 in Left zone, 2 in Center zone, 1 in Right zone!
        # perm[0] in Left zone, perm[1] & perm[2] in Center zone, perm[3] in Right zone!
        w0 = conns_spec[perm[0]]['w']
        w1 = conns_spec[perm[1]]['w']
        w2 = conns_spec[perm[2]]['w']
        w3 = conns_spec[perm[3]]['w']
        
        # Center zone width needed: w1 + w2 + 0.5
        if w1 + w2 + 0.5 > (112.556 - 87.444):
            continue # cannot fit 2 in center!
            
        # Try placing perm[0] as close to H2 as possible without colliding
        # box0: x in [x0, x0 + w0]
        # We want x0 + w0 <= 81.40
        x0 = 81.40 - w0
        b0 = (x0, x0 + w0, y_cut - conns_spec[perm[0]]['h'], y_cut)
        if collides_hole(b0) or not inside_board(b0, y_cut):
            continue
            
        # Try placing perm[3] as close to H1 as possible
        # box3: x in [x3, x3 + w3]
        # x3 >= 118.60
        x3 = 118.60
        b3 = (x3, x3 + w3, y_cut - conns_spec[perm[3]]['h'], y_cut)
        if collides_hole(b3) or not inside_board(b3, y_cut):
            continue
            
        # Now place perm[1] and perm[2] in center [87.45, 112.55]
        # Available center width = 112.55 - 87.45 = 25.10
        spare = 25.10 - (w1 + w2)
        x1 = 87.45 + spare / 3.0
        b1 = (x1, x1 + w1, y_cut - conns_spec[perm[1]]['h'], y_cut)
        x2 = x1 + w1 + spare / 3.0
        b2 = (x2, x2 + w2, y_cut - conns_spec[perm[2]]['h'], y_cut)
        
        if collides_hole(b1) or not inside_board(b1, y_cut): continue
        if collides_hole(b2) or not inside_board(b2, y_cut): continue
        
        results.append((y_cut, perm, [b0, b1, b2, b3]))

print(f"Total successful 1-2-1 configurations found: {len(results)}")
for y_cut, perm, boxes in results[:10]:
    print(f"y_cut={y_cut}: {perm}")
    for name, b in zip(perm, boxes):
        print(f"   {name:5s}: X [{b[0]:.2f}, {b[1]:.2f}]")
