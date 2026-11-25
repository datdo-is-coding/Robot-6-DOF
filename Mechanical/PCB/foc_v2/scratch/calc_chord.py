import math

# Circle: center (100, 100), R = 35 mm
# Flat cut: Y = y_cut
# Chord: from (100 - dx, y_cut) to (100 + dx, y_cut)
# dx = sqrt(35^2 - (y_cut - 100)^2)

print(f"{'y_cut':>6s} | {'dy':>5s} | {'dx':>6s} | {'chord width':>11s} | {'X_min':>6s} .. {'X_max':>6s}")
print("-" * 55)
for y_cut in [122.0, 123.0, 123.5, 124.0, 125.0, 126.0, 127.0, 128.0]:
    dy = y_cut - 100.0
    dx = math.sqrt(35.0**2 - dy**2)
    width = 2 * dx
    print(f"{y_cut:6.1f} | {dy:5.1f} | {dx:6.2f} | {width:11.2f} | {100-dx:6.2f} .. {100+dx:6.2f}")
