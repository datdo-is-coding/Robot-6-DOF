import subprocess, json

# Let's run kicad-cli drc on git version
res = subprocess.run(['git', 'show', '51d2e07:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], capture_output=True)
with open('scratch/git_raw.kicad_pcb', 'wb') as f:
    f.write(res.stdout)

cmd = ['C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe', 'pcb', 'drc', '--format', 'json', '-o', 'scratch/git_drc.json', 'scratch/git_raw.kicad_pcb']
subprocess.run(cmd, capture_output=True)

with open('scratch/git_drc.json') as f:
    d = json.load(f)
v = d.get('violations', [])
invalid = [item for item in v if item['type'] == 'invalid_outline']
print("Git version invalid_outline count:", len(invalid))
if invalid:
    print(invalid[0])
