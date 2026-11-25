import uuid, subprocess, json, re

u1, u2, u3, u4 = [str(uuid.uuid4()) for _ in range(4)]
circle_edges = f"""	(gr_arc
		(start 100 65)
		(mid 124.748737 75.251262)
		(end 135 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u1}")
	)
	(gr_arc
		(start 135 100)
		(mid 124.748737 124.748737)
		(end 100 135)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u2}")
	)
	(gr_arc
		(start 100 135)
		(mid 75.251262 124.748737)
		(end 65 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u3}")
	)
	(gr_arc
		(start 65 100)
		(mid 75.251262 75.251262)
		(end 100 65)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u4}")
	)"""

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'(\t\(gr_arc\s+\(start 65 100\).*?\(uuid "037693de-df8a-455f-bed1-fc100082e71e"\)\s*\n\t\))'
match = re.search(pattern, text, flags=re.DOTALL)
if match:
    text = text[:match.start()] + circle_edges + text[match.end():]
    print('Pattern matched!')
else:
    print('Pattern not matched in git_raw!')

with open('scratch/test_pure_circle.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(text)

cmd = ['C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe', 'pcb', 'drc', '--format', 'json', '-o', 'scratch/pure_circle_drc.json', 'scratch/test_pure_circle.kicad_pcb']
res = subprocess.run(cmd, capture_output=True, text=True)
with open('scratch/pure_circle_drc.json') as f:
    d = json.load(f)
v = d.get('violations', [])
invalid = [item for item in v if item['type'] == 'invalid_outline']
print(f'Pure Circle DRC: total violations={len(v)}, invalid_outline={len(invalid)}')
