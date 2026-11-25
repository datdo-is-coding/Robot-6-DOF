with open('scratch/foc_v2_orig.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\t\((?:gr_line|gr_arc|gr_circle)\b[\s\S]+?\(layer "Edge\.Cuts"\)[\s\S]+?\n\t\)', text)
for m in matches:
    print(m)
