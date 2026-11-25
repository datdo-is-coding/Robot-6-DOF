import subprocess
import re

out = subprocess.check_output(['git', 'show', 'a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], text=True, encoding='utf-8')

blocks = out.split('(footprint ')
orig_P = {}
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
    layer_m = re.search(r'\(layer "([^"]+)"\)', b)
    x = float(at_m.group(1))
    y = float(at_m.group(2))
    rot = float(at_m.group(3)) if at_m.group(3) else 0.0
    layer = layer_m.group(1)
    orig_P[ref] = (x, y, rot, layer)

print(f"Total components in commit a0922b7: {len(orig_P)}")
for ref in ['U1', 'IC1', 'U2', 'J1', 'J2', 'J3', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'C_BULK1', 'C63', 'J7', 'J8', 'J9', 'J10', 'J11']:
    if ref in orig_P:
        print(f"  {ref:8s}: {orig_P[ref]}")
