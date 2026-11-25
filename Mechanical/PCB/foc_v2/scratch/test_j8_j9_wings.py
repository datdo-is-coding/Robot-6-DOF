import math

cx, cy = 100.0, 100.0
r_board = 35.0
h1_x, h1_y = 115.556, 115.556
h2_x, h2_y = 84.444, 115.556
hole_r = 2.95

def collides_hole(box):
    for hx, hy in [(h1_x, h1_y), (h2_x, h2_y)]:
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

# Let's test J8 (w=10.51, h=11.61) in Zone 1:
# x in [x_right - 10.51, x_right]
print("Testing J8 in Zone 1 (West of H2):")
for y_front in [117.0, 118.0, 119.0, 120.0, 120.2, 121.0, 122.0, 123.5]:
    for x_right in [80.0, 80.5, 81.0, 81.4]:
        b = (x_right - 10.51, x_right, y_front - 11.61, y_front)
        if not collides_hole(b) and inside_circle(b):
            print(f"  SUCCESS J8 in Zone 1: y_front={y_front}, x_right={x_right}, b={b}")
            break

print("\nTesting J9 in Zone 3 (East of H1):")
for y_front in [117.0, 118.0, 119.0, 120.0, 120.2, 121.0, 122.0, 123.5]:
    for x_left in [118.6, 119.0, 119.5, 120.0]:
        b = (x_left, x_left + 10.51, y_front - 11.61, y_front)
        if not collides_hole(b) and inside_circle(b):
            print(f"  SUCCESS J9 in Zone 3: y_front={y_front}, x_left={x_left}, b={b}")
            break
