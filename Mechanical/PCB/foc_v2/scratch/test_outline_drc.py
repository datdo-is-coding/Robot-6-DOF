import math, subprocess, json, uuid

cx, cy = 100.0, 100.0
r = 35.0
y_cut = 120.0
x_half = math.sqrt(r**2 - (y_cut - cy)**2)
x_left = round(cx - x_half, 4)
x_right = round(cx + x_half, 4)

def arc_mid(x1, y1, x2, y2, cx=100.0, cy=100.0, r=35.0):
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    # clockwise means increasing angle in KiCad (Y down)
    if a2 <= a1:
        a2 += 2 * math.pi
    amid = (a1 + a2) / 2
    return round(cx + r * math.cos(amid), 6), round(cy + r * math.sin(amid), 6)

# Clockwise loop:
# Start at x_left, y_cut: angle is atan2(20, -28.72) ~ 145.16 deg
# Go to (65, 100): angle is 180 deg
m1x, m1y = arc_mid(x_left, y_cut, 65.0, 100.0)
# (65, 100) to (100, 65): angle 180 to 270 deg
m2x, m2y = arc_mid(65.0, 100.0, 100.0, 65.0)
# (100, 65) to (135, 100): angle 270 to 360 deg
m3x, m3y = arc_mid(100.0, 65.0, 135.0, 100.0)
# (135, 100) to (x_right, y_cut): angle 0 to 34.84 deg
m4x, m4y = arc_mid(135.0, 100.0, x_right, y_cut)

edge_cuts = f"""	(gr_arc
		(start {x_left} {y_cut})
		(mid {m1x} {m1y})
		(end 65 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_arc
		(start 65 100)
		(mid {m2x} {m2y})
		(end 100 65)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_arc
		(start 100 65)
		(mid {m3x} {m3y})
		(end 135 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_arc
		(start 135 100)
		(mid {m4x} {m4y})
		(end {x_right} {y_cut})
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_line
		(start {x_right} {y_cut})
		(end {x_left} {y_cut})
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
"""

print(f"Chord: ({x_right}, {y_cut}) -> ({x_left}, {y_cut})")
print("Arc mids:", (m1x, m1y), (m2x, m2y), (m3x, m3y), (m4x, m4y))

with open('scratch/test_outline.sexpr', 'w') as f:
    f.write(edge_cuts)
