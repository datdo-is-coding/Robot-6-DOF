import math

cx, cy = 100.0, 100.0
R = 35.0

print("D-Shape Board: Circle R=35mm with single flat chord cut at y = y_cut:")
for y_cut in [120.0, 122.0, 124.0, 125.0, 126.0, 128.0, 130.0, 132.0]:
    dy = y_cut - cy
    if dy < R:
        dx = math.sqrt(R**2 - dy**2)
        x1 = cx - dx
        x2 = cx + dx
        chord_len = 2 * dx
        print(f"  y_cut = {y_cut:5.1f} mm : chord from x=[{x1:6.2f}, {x2:6.2f}] (length = {chord_len:5.2f} mm)")
