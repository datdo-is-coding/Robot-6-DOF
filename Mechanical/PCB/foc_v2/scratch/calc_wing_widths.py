import math

# Let's check which connectors can fit along the South flat cut strictly inside the circle R = 35.0:
# Circle: (100, 100), R = 35.0 mm.
# H2 = (84.444, 115.556), H1 = (115.556, 115.556), keepout = 2.95 mm.

# Between H2 and H1: X in [87.4 .. 112.6] (width = 25.2 mm).
# Connectors:
# J7 (USB-C): width 8.94 (crtyd 10.64)
# J8 (3-pin): width 9.9 (crtyd 10.9)
# J9 (3-pin): width 9.9 (crtyd 10.9)
# J10 (5-pin): width 14.9 (crtyd 15.9)

# In the 25.2 mm center between H2 and H1:
# Can (J8 and J9) fit? 10.9 + 10.9 = 21.8 < 25.2. YES! (CAN IN and CAN OUT fit side by side!)
# Can (J7 and J8) fit? 10.64 + 10.9 = 21.54 < 25.2. YES!
# Can (J7 and J9) fit? 10.64 + 10.9 = 21.54 < 25.2. YES!
# Can (J10 and J8) fit? 15.9 + 10.9 = 26.8 > 25.2. NO.
# Can (J10 and J7) fit? 15.9 + 10.64 = 26.54 > 25.2. NO.
# So J10 alone fits in the center (15.9 < 25.2), OR two smaller connectors fit!

# Now, what about the West of H2 and East of H1?
# Outside H2 and H1, what is the maximum width of a rectangle that can fit inside the circle?
print("Let's calculate the maximum rectangle that fits West of H2 and East of H1 inside R = 35.0:")
for y_cut in [120.0, 122.0, 123.5, 125.0]:
    # West of H2: rx2 <= 81.5 mm.
    # What is the minimum rx1 such that the bottom-left corner (rx1, y_cut) is inside circle R = 35.0?
    # (rx1 - 100)^2 + (y_cut - 100)^2 <= 35^2
    dy = y_cut - 100.0
    rx1_min = 100.0 - math.sqrt(35.0**2 - dy**2)
    max_w_west = 81.5 - rx1_min
    # East of H1: rx1 >= 118.5 mm.
    rx2_max = 100.0 + math.sqrt(35.0**2 - dy**2)
    max_w_east = rx2_max - 118.5
    print(f"y_cut = {y_cut:.1f}: Max width West of H2 = {max_w_west:.2f} mm, East of H1 = {max_w_east:.2f} mm")
