import math, re, uuid, subprocess, json
import test_courtyards

local_boxes = test_courtyards.parse_footprints()

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    orig_text = f.read()

# Board constants
cx, cy = 100.0, 100.0
r_board = 35.0
y_cut = 120.2
x_left = round(100.0 - math.sqrt(35**2 - (y_cut - 100)**2), 4)
x_right = round(100.0 + math.sqrt(35**2 - (y_cut - 100)**2), 4)

# 1. Edge.Cuts definitions (5-segment watertight outline)
def get_arc_mid(x1, y1, x2, y2, cx=100.0, cy=100.0, r=35.0, ccw=False):
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    if not ccw:
        if a2 <= a1: a2 += 2 * math.pi
        amid = (a1 + a2) / 2
    else:
        if a2 >= a1: a2 -= 2 * math.pi
        amid = (a1 + a2) / 2
    return round(cx + r * math.cos(amid), 4), round(cy + r * math.sin(amid), 4)

mx3, my3 = get_arc_mid(135.0, 100.0, x_right, y_cut)
mx5, my5 = get_arc_mid(x_left, y_cut, 65.0, 100.0)

edge_cuts_sexpr = f"""	(gr_arc
		(start 65 100)
		(mid 75.251262 75.251262)
		(end 100 65)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_arc
		(start 100 65)
		(mid 124.748737 75.251262)
		(end 135 100)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_arc
		(start 135 100)
		(mid {mx3} {my3})
		(end {x_right} {y_cut})
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_line
		(start {x_right} {y_cut})
		(end {x_left} {y_cut})
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
	(gr_arc
		(start {x_left} {y_cut})
		(mid {my5} {my5})
		(end 65 100)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{uuid.uuid4()}")
	)
"""

print(f"Outline: circle R=35 with flat cut at Y={y_cut} from X={x_left} to X={x_right}")
