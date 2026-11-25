import math

H2 = (84.444, 115.556)
H1 = (115.556, 115.556)
R_KEEPOUT = 3.0

# J8: 3-pin XH. CrtYd: x in [x_pin - 2.95, x_pin + 7.95], y in [y_pin - 2.81, y_pin + 9.70] (width 10.9)
# J9: 3-pin XH. CrtYd: x in [x_pin - 2.95, x_pin + 7.95], y in [y_pin - 2.81, y_pin + 9.70] (width 10.9)
# J7: Type-C. CrtYd: x in [x_pin - 5.32, x_pin + 5.32], y in [y_pin - 5.27, y_pin + 4.15] (width 10.64)

# We want J8, J9, J7 to be aligned facing South!
# Either:
# Option 1: y_pin > 115.556 + 3.0 + 2.81 = 121.37 mm!
# If y_pin = 122.0 mm:
# Then y_crtyd_min = 122.0 - 2.81 = 119.19 mm > 118.556 mm (bottom of H2/H1 keepouts)!
# That means J8 and J7 can be as wide as needed because they are entirely SOUTH of H2 and H1!
# Let's check where their front face lands if y_pin = 121.0 or 122.0:
# For J8/J9: front face = y_pin + 9.70 = 130.7 or 131.7 mm.
# For J7: front face = y_pin + 4.15 = 125.15 or 126.15 mm. (To align front faces, J7 y_pin can be 126.5 mm).

print("Testing Option 1: Connectors placed below (South of) H2 and H1:")
for y_pin_xh in [120.0, 121.0, 122.0]:
    y_min = y_pin_xh - 2.81
    y_max = y_pin_xh + 9.70
    print(f"y_pin={y_pin_xh}: Y span = [{y_min:.2f}, {y_max:.2f}]")
    # Check H2 distance for x_pin from 86.0 to 90.0
    for x_pin in [86.0, 87.0, 88.0, 89.0]:
        x_min, x_max = x_pin - 2.95, x_pin + 7.95
        # closest point to H2 (84.444, 115.556)
        cx = max(x_min, min(H2[0], x_max))
        cy = max(y_min, min(H2[1], y_max))
        d = math.hypot(cx - H2[0], cy - H2[1])
        print(f"  x_pin={x_pin}, dist to H2 = {d:.2f} mm (keepout={R_KEEPOUT})")
