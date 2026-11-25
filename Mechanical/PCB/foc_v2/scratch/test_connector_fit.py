import math

CX, CY = 100.0, 100.0
R_BOARD = 35.0

# Check if a rectangle [x_min, x_max] x [y_min, y_max] is inside circle (CX, CY, R)
def rect_inside_circle(xmin, xmax, ymin, ymax, cx=100.0, cy=100.0, r=35.0):
    corners = [(xmin, ymin), (xmin, ymax), (xmax, ymin), (xmax, ymax)]
    max_d = max(math.hypot(x - cx, y - cy) for x, y in corners)
    return max_d <= r, max_d

# Let's check where JST-XH 3p and 5p can fit at the bottom:
# JST-XH 3p: width 10.9 mm, depth 12.51 mm
# JST-XH 5p: width 15.9 mm, depth 12.51 mm
# USB-C: width 9.0 mm, depth 8.5 mm

print("Checking connector fits:")
# If we have 3 connectors: CAN_IN (J8), CAN_OUT (J9), SWD (J10), Type-C (J7)
# What if Type-C is in the middle (x=100)?
# If Type-C is at x=100: mouth at y=131.0, body y in [122.5, 131.0], x in [95.5, 104.5]
ok, d = rect_inside_circle(95.5, 104.5, 122.5, 131.0)
print(f"Type-C at x=100, y_mouth=131.0: inside={ok}, max_dist={d:.2f}")

# What if J8 and J9 are to the left and right of Type-C?
# Or what if SWD (J10) is somewhere else, or they are all placed together?
# Let's test placing them:
# Can all 4 be in a single row?
# If all 4 are in a row:
# Total width = J8 (10.9) + gap (2) + J9 (10.9) + gap (2) + J7 (9.0) + gap (2) + J10 (15.9) = 52.7 mm!
# If centered at x=100: x from 100 - 26.35 = 73.65 to 100 + 26.35 = 126.35!
# At x = 73.65, dx = 26.35. Max y on circle is 100 + sqrt(35^2 - 26.35^2) = 100 + 23.03 = 123.03!
# But JST-XH depth is 12.5 mm!
# If its bottom is at 123.03, its top (pins) MUST be at 123.03 - 9.7 = 113.33!
# Let's check: at x in [73.65, 84.55], y in [110.5, 123.0]:
ok, d = rect_inside_circle(73.65, 84.55, 110.5, 123.0)
print(f"XH at x in [73.65, 84.55], y in [110.5, 123.0]: inside={ok}, max_dist={d:.2f}")
