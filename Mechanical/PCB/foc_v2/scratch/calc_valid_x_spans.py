import math

# Circle is center (100, 100), R = 35.0
# A connector has a rectangular box: x in [x1, x2], y in [y1, y2].
# All 4 corners must satisfy (x - 100)^2 + (y - 100)^2 <= 35.0^2.
# Let's find for each connector, if y2 = y_front, what is the valid range of x!

conns = {
    'J7':  {'w': 10.64, 'h': 9.03},
    'J8':  {'w': 10.51, 'h': 11.61},
    'J9':  {'w': 10.51, 'h': 11.61},
    'J10': {'w': 15.51, 'h': 11.61}
}

for y_front in [118.0, 118.5, 119.0, 119.5, 120.0, 120.5, 121.0, 121.5, 122.0]:
    print(f"=== y_front = {y_front} ===")
    for name, c in conns.items():
        w, h = c['w'], c['h']
        y1 = y_front - h
        y2 = y_front
        # we need for any x in [x_min, x_max]:
        # corners (x, y1), (x+w, y1), (x, y2), (x+w, y2) inside R=35.0
        valid_x = []
        for x in [round(65.0 + i * 0.1, 2) for i in range(700)]:
            corners = [(x, y1), (x+w, y1), (x, y2), (x+w, y2)]
            if all(math.hypot(px - 100, py - 100) <= 34.95 for px, py in corners):
                valid_x.append(x)
        if valid_x:
            print(f"  {name:5s}: X in [{min(valid_x):.2f}, {max(valid_x):.2f}] (span={max(valid_x)-min(valid_x):.2f})")
        else:
            print(f"  {name:5s}: NO VALID X")
