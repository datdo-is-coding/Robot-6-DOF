import math

# We want all 4 connectors to have their front mating faces at Y_edge = 120.00 mm
# (or Y_edge = 120.20 mm).
# Circle center = (100.0, 100.0), R = 35.0 mm.

# Let's test Y_edge values from 118.0 to 123.0
for y_edge in [119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0]:
    x_half = math.sqrt(35.0**2 - (y_edge - 100.0)**2)
    x_left = 100.0 - x_half
    x_right = 100.0 + x_half
    print(f"y_edge={y_edge:.1f}: X in [{x_left:.2f}, {x_right:.2f}], width={2*x_half:.2f} mm")
