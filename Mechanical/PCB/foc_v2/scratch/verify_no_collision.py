import math

H_SW = (84.444, 115.556)
H_SE = (115.556, 115.556)
R_ko = 3.0 # keepout radius (screw head)
pad_r = 0.85 # pad copper radius for 1.7mm pad

# Test any pad with y_pad >= 119.5 mm:
for x in [75.0, 78.0, 81.0, 84.444, 87.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.556, 120.0]:
    for y in [119.5, 120.0, 120.5]:
        d_sw = math.hypot(x - H_SW[0], y - H_SW[1])
        d_se = math.hypot(x - H_SE[0], y - H_SE[1])
        min_d = min(d_sw, d_se)
        margin = min_d - (R_ko + pad_r)
        assert margin > 0, f"Collision at ({x}, {y}): margin={margin}"

print("All assertions passed! Any pad with y >= 119.5 mm has ZERO collision with screw keepouts!")
