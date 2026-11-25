import subprocess
import uuid

# read foc_v2.kicad_pcb
with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

# let's add a test via for C21 pad 1 GND at 105.0, 96.3675 (from VIPPO_REQUIRED.csv)
test_via = f"""
	(via
		(at 105.0 96.3675)
		(size 0.4)
		(drill 0.2)
		(layers "F.Cu" "B.Cu")
		(net "GND")
		(uuid "{str(uuid.uuid4())}")
	)
"""

# insert test_via right before the last closing parenthesis
idx = content.rfind(')')
test_content = content[:idx] + test_via + content[idx:]

with open('scratch/test_via.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(test_content)

res = subprocess.run([
    'C:/Program Files/KiCad/10.0/bin/kicad-cli.exe',
    'pcb', 'drc',
    '--format', 'json',
    '-o', 'scratch/test_via_drc.json',
    'scratch/test_via.kicad_pcb'
], capture_output=True, text=True)

print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
