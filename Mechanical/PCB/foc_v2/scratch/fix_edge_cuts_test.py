import math, uuid, subprocess, json, re

# Arc 1: from SE (125.9374, 123.5) to East to Top (100, 65)
# mid point between 42.1774 deg and -90 deg:
# ang_mid1 = (42.1774457 - 90.0) / 2 = -23.911277 deg
rad1 = math.radians(-23.911277)
x_mid1 = round(100.0 + 35.0 * math.cos(rad1), 4)
y_mid1 = round(100.0 + 35.0 * math.sin(rad1), 4)

# Arc 2: from Top (100, 65) to West to SW (74.0626, 123.5)
# ang_mid2: from -90 deg (-1.5708 rad) through 180 deg to 137.82255 deg
# span from -90 to -222.1774 deg -> mid is -156.0887 deg
rad2 = math.radians(-156.088727)
x_mid2 = round(100.0 + 35.0 * math.cos(rad2), 4)
y_mid2 = round(100.0 + 35.0 * math.sin(rad2), 4)

u1 = str(uuid.uuid4())
u2 = str(uuid.uuid4())
u3 = str(uuid.uuid4())

edge_sexpr = f"""	(gr_line
		(start 74.0626 123.5)
		(end 125.9374 123.5)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{u1}")
	)
	(gr_arc
		(start 125.9374 123.5)
		(mid {x_mid1} {y_mid1})
		(end 100 65)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{u2}")
	)
	(gr_arc
		(start 100 65)
		(mid {x_mid2} {y_mid2})
		(end 74.0626 123.5)
		(stroke
			(width 0.05)
			(type default)
		)
		(layer "Edge.Cuts")
		(uuid "{u3}")
	)
"""

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the previous Edge.Cuts block
pattern = r'\(gr_line\s*\(start 74\.0626 123\.5\).*?\(uuid "edge-circular-arc-r35"\)\s*\)'
new_text = re.sub(pattern, edge_sexpr.strip(), text, flags=re.DOTALL)

with open('scratch/test_edge.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(new_text)

print(f"Arc 1 mid: ({x_mid1}, {y_mid1}), Arc 2 mid: ({x_mid2}, {y_mid2})")
print("Saved scratch/test_edge.kicad_pcb. Testing with kicad-cli...")

cmd = ['C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe', 'pcb', 'drc', '--format', 'json', '-o', 'scratch/test_edge_drc.json', 'scratch/test_edge.kicad_pcb']
res = subprocess.run(cmd, capture_output=True, text=True)
with open('scratch/test_edge_drc.json') as f:
    d = json.load(f)
v = d.get('violations', [])
invalid = [item for item in v if item['type'] == 'invalid_outline']
print(f"Total violations: {len(v)}, invalid_outline: {len(invalid)}")
if invalid:
    print(invalid[0])
