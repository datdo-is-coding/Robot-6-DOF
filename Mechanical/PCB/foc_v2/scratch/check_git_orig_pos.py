import subprocess
import re

out = subprocess.check_output(['git', 'show', 'a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb'], text=True, encoding='utf-8')
blocks = out.split('(footprint ')
for b in blocks[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', b)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    if ref in ['J11', 'J7', 'J8', 'J9', 'J10', 'H1', 'H2', 'H3', 'H4', 'J1', 'J2', 'J3']:
        at_m = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', b)
        fp_m = b.split()[0].strip('"')
        print(f"{ref:5s} | at=({at_m.group(1):>7s}, {at_m.group(2):>7s}) rot={str(at_m.group(3)):>5s} | {fp_m}")
