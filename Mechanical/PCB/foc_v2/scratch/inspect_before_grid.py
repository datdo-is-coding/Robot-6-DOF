with open('work/2026-11-13-pcb-layout/before-grid.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
idx = text.find('(via ')
print(text[idx:idx+400])
