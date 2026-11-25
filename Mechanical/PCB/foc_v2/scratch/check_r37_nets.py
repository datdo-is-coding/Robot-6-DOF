with open('MCU.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# find wires or labels near (40.64, 175.26)
for line in text.splitlines():
    if any(k in line for k in ['40.64', '92.71', '144.78', 'SWDIO', 'SWCLK', 'NRST', 'BOOT', 'OSC']):
        print(line[:120])
