import math, uuid, subprocess, json

def get_arc_mid(x1, y1, x2, y2, cx=100.0, cy=100.0, r=35.0, ccw=False):
    # Calculate mid point on circle between (x1,y1) and (x2,y2)
    # in KiCad, positive rotation is clockwise (Y down)
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    if not ccw: # clockwise: angle increases
        if a2 <= a1:
            a2 += 2 * math.pi
        amid = (a1 + a2) / 2
    else:
        if a2 >= a1:
            a2 -= 2 * math.pi
        amid = (a1 + a2) / 2
    return round(cx + r * math.cos(amid), 6), round(cy + r * math.sin(amid), 6)

# Test clockwise loop:
# 1. Top-Left to Top: from (65, 100) through (75.251262, 75.251262) to (100, 65)
# 2. Top to Right: from (100, 65) through (124.748737, 75.251262) to (135, 100)
# 3. Right to SE: from (135, 100) to (125.9374, 123.5)
#    a1 = 0, a2 = atan2(23.5, 25.9374) = 42.177 deg -> mid = 21.088 deg
mx3, my3 = get_arc_mid(135.0, 100.0, 125.9374, 123.5)
# 4. Straight line: from (125.9374, 123.5) to (74.0626, 123.5)
# 5. SW to Left: from (74.0626, 123.5) to (65, 100)
#    a1 = atan2(23.5, -25.9374) = 137.822 deg, a2 = 180 deg -> mid = 158.911 deg
mx5, my5 = get_arc_mid(74.0626, 123.5, 65.0, 100.0)

print(f"Arc 3 mid: ({mx3}, {my3})")
print(f"Arc 5 mid: ({mx5}, {my5})")

u1 = str(uuid.uuid4())
u2 = str(uuid.uuid4())
u3 = str(uuid.uuid4())
u4 = str(uuid.uuid4())
u5 = str(uuid.uuid4())

new_edges = f"""	(gr_arc
		(start 65 100)
		(mid 75.251262 75.251262)
		(end 100 65)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{u1}")
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
		(uuid "{u2}")
	)
	(gr_arc
		(start 135 100)
		(mid {mx3} {my3})
		(end 125.9374 123.5)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{u3}")
	)
	(gr_line
		(start 125.9374 123.5)
		(end 74.0626 123.5)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{u4}")
	)
	(gr_arc
		(start 74.0626 123.5)
		(mid {mx5} {my5})
		(end 65 100)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{u5}")
	)
"""

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the 4 arcs in git_raw
import re
# remove the existing gr_arc on Edge.Cuts
# git_raw had the 4 arcs together
pattern = r'(\t\(gr_arc\s+\(start 65 100\).*?\(uuid "037693de-df8a-455f-bed1-fc100082e71e"\)\s*\n\t\))'
match = re.search(pattern, text, flags=re.DOTALL)
if match:
    print("Found match in git_raw!")
    text = text[:match.start()] + new_edges.strip() + text[match.end():]
else:
    print("Pattern not matched directly, using custom replacement")

with open('scratch/test_d_shape.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(text)

cmd = ['C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe', 'pcb', 'drc', '--format', 'json', '-o', 'scratch/d_shape_drc.json', 'scratch/test_d_shape.kicad_pcb']
res = subprocess.run(cmd, capture_output=True, text=True)
with open('scratch/d_shape_drc.json') as f:
    d = json.load(f)
v = d.get('violations', [])
invalid = [item for item in v if item['type'] == 'invalid_outline']
print(f"Test D-shape DRC: total violations={len(v)}, invalid_outline={len(invalid)}")
if invalid:
    print(invalid[0])
