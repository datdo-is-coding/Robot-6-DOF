import math

# Holes
H_SW = (84.444, 115.556)
H_SE = (115.556, 115.556)
R_ko = 3.0 # keepout radius

def check_clearance(px, py, pad_r=0.85):
    d_sw = math.hypot(px - H_SW[0], py - H_SW[1])
    d_se = math.hypot(px - H_SE[0], py - H_SE[1])
    min_d = min(d_sw, d_se)
    margin = min_d - (R_ko + pad_r)
    return margin

# Let's test various y_pin from 116.0 to 122.0
# and various x positions for J8, J9, J7, J10:
print("Testing clearances:")
for y_pin in [116.0, 117.0, 118.0, 119.0, 120.0, 121.0]:
    # If J8 is at x=78.0:
    # J8 pads at x, x+2.5, x+5.0
    pads_j8 = [(78.0, y_pin), (80.5, y_pin), (83.0, y_pin)]
    margins = [check_clearance(p[0], p[1]) for p in pads_j8]
    print(f"y_pin={y_pin}: min margin J8={min(margins):.2f} mm")

