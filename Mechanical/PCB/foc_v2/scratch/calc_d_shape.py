import math

# Pure D-Shape Board Outline:
# Circle: center (100.0, 100.0), Radius = 35.0 mm.
# Flat cut: Y = y_cut.
# Chord endpoints:
# dy = y_cut - 100.0
# dx = sqrt(35^2 - dy^2)
# P_start = (100.0 - dx, y_cut)  (left corner)
# P_end   = (100.0 + dx, y_cut)  (right corner)

# Elements:
# 1. gr_line from (100 - dx, y_cut) to (100 + dx, y_cut)
# 2. gr_arc from (100 + dx, y_cut) around (100, 65) to (100 - dx, y_cut)
# Center of arc is (100, 100), radius is 35.0 mm.
# Midpoint of arc is (100.0, 65.0) (the North pole of the circle!)

for y_cut in [123.0, 123.5, 124.0, 125.0, 126.0]:
    dy = y_cut - 100.0
    dx = math.sqrt(35.0**2 - dy**2)
    p_left = (100.0 - dx, y_cut)
    p_right = (100.0 + dx, y_cut)
    width = 2 * dx
    print(f"y_cut = {y_cut:.1f}:")
    print(f"  Chord: ({p_left[0]:.4f}, {p_left[1]:.4f}) -> ({p_right[0]:.4f}, {p_right[1]:.4f}), width = {width:.2f} mm")
    print(f"  Arc: start ({p_right[0]:.4f}, {p_right[1]:.4f}), mid (100.0, 65.0), end ({p_left[0]:.4f}, {p_left[1]:.4f})")
