import re, uuid, subprocess, json

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Define the 5-segment clean D-shape Edge.Cuts
u1, u2, u3, u4, u5 = [str(uuid.uuid4()) for _ in range(5)]

clean_d_shape = f"""	(gr_arc
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
		(mid 133.39385 110.480972)
		(end 128.722813 120)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u3}")
	)
	(gr_line
		(start 128.722813 120)
		(end 71.277187 120)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u4}")
	)
	(gr_arc
		(start 71.277187 120)
		(mid 66.60615 110.480972)
		(end 65 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u5}")
	)\n)"""

# Delete ALL gr_line / gr_arc on Edge.Cuts
text = re.sub(r'(\t\(gr_(?:line|arc|poly|rect|circle)[\s\S]*?\(layer "Edge\.Cuts"\)[\s\S]*?\n\t\)\s*)+', '', text)
text = text.rstrip()
if text.endswith(')'):
    text = text[:-1] + clean_d_shape + '\n'

with open('scratch/foc_v2_clean_d_shape.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(text)

# Run DRC on clean D-shape
cmd = ['C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe', 'pcb', 'drc', '--format', 'json', '-o', 'scratch/drc_clean_d_shape.json', 'scratch/foc_v2_clean_d_shape.kicad_pcb']
res = subprocess.run(cmd, capture_output=True, text=True)
with open('scratch/drc_clean_d_shape.json') as f:
    d = json.load(f)
v = d.get('violations', [])
invalid = [item for item in v if item['type'] == 'invalid_outline']
print(f"Clean D-shape DRC: total violations={len(v)}, invalid_outline={len(invalid)}")
