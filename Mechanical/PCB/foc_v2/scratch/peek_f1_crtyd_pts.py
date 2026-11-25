with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'\(footprint "Fuse:Fuseholder_Blade_Mini_Keystone_3568".*?\n\t\)', text, flags=re.DOTALL)
if m:
    lines = m.group(0).splitlines()
    for i, l in enumerate(lines):
        if 'B.CrtYd' in l:
            print("\n".join(lines[i-4:i+2]))
