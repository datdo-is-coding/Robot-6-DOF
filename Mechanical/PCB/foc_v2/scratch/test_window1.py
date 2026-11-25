import math

cx, cy = 100.0, 100.0
# Window 1: x < 81.49.
# If connector has width 10.51:
# x in [x_right - 10.51, x_right] where x_right <= 81.0.
# If x_right = 81.0 -> x in [70.49, 81.0].
# Let's check the distance of the 4 corners from center (100, 100) for various y_front:
for y_front in [118.0, 119.0, 120.0, 121.0, 122.0, 123.0, 123.5]:
    # JST-XH depth is 11.61 -> y in [y_front - 11.61, y_front]
    y_back = y_front - 11.61
    corners = [(70.49, y_back), (81.0, y_back), (70.49, y_front), (81.0, y_front)]
    dists = [math.sqrt((x-cx)**2 + (y-cy)**2) for x, y in corners]
    max_d = max(dists)
    print(f"y_front={y_front}: max distance to center = {max_d:.2f} mm (inside 35mm circle? {max_d <= 35.0})")
