with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'\(footprint "Fuse:Fuseholder_Blade_Mini_Keystone_3568".*?\n\t\)', text, flags=re.DOTALL)
if m:
    for line in m.group(0).splitlines():
        if 'CrtYd' in line or 'fp_' in line:
            print(line)
