import math, uuid, subprocess, json, re

def get_arc_mid(x1, y1, x2, y2, cx=100.0, cy=100.0, r=35.0, ccw=False):
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    if not ccw:
        if a2 <= a1: a2 += 2 * math.pi
        amid = (a1 + a2) / 2
    else:
        if a2 >= a1: a2 -= 2 * math.pi
        amid = (a1 + a2) / 2
    return round(cx + r * math.cos(amid), 6), round(cy + r * math.sin(amid), 6)

cx, cy, r = 100.0, 100.0, 35.0
y_cut = 120.0
x_half = math.sqrt(r**2 - (y_cut - cy)**2)
x_left = round(cx - x_half, 6)
x_right = round(cx + x_half, 6)

mx3, my3 = get_arc_mid(135.0, 100.0, x_right, y_cut)
mx5, my5 = get_arc_mid(x_left, y_cut, 65.0, 100.0)

print(f"Cut: Y={y_cut}, X=[{x_left}, {x_right}]")
print(f"Arc 3 mid: ({mx3}, {my3})")
print(f"Arc 5 mid: ({mx5}, {my5})")

u1, u2, u3, u4, u5 = [str(uuid.uuid4()) for _ in range(5)]

new_edges = f"""	(gr_arc
		(start 65 100)
		(mid 75.251262 75.251262)
		(end 100 65)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u1}")
	)
	(gr_arc
		(start 100 65)
		(mid 124.748737 75.251262)
		(end 135 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u2}")
	)
	(gr_arc
		(start 135 100)
		(mid {mx3} {my3})
		(end {x_right} {y_cut})
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u3}")
	)
	(gr_line
		(start {x_right} {y_cut})
		(end {x_left} {y_cut})
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u4}")
	)
	(gr_arc
		(start {x_left} {y_cut})
		(mid {mx5} {my5})
		(end 65 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u5}")
	)"""

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'(\t\(gr_arc\s+\(start 65 100\).*?\(uuid "037693de-df8a-455f-bed1-fc100082e71e"\)\s*\n\t\))'
match = re.search(pattern, text, flags=re.DOTALL)
text = text[:match.start()] + new_edges + text[match.end():]

with open('scratch/test_d_shape_120.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(text)

cmd = ['C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe', 'pcb', 'drc', '--format', 'json', '-o', 'scratch/d_shape_120_drc.json', 'scratch/test_d_shape_120.kicad_pcb']
res = subprocess.run(cmd, capture_output=True, text=True)
with open('scratch/d_shape_120_drc.json') as f:
    d = json.load(f)
v = d.get('violations', [])
invalid = [item for item in v if item['type'] == 'invalid_outline']
print(f"Test D-shape Y=120 DRC: total violations={len(v)}, invalid_outline={len(invalid)}")
if invalid:
    print(invalid[0])
