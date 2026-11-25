with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'\(footprint "Fuse:Fuseholder_Blade_Mini_Keystone_3568".*?\n\t\)', text, flags=re.DOTALL)
if m:
    for block in re.findall(r'\(fp_line.*?\n\t\t\)', m.group(0), flags=re.DOTALL):
        if 'B.CrtYd' in block:
            print(" ".join(block.split()))
