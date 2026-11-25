with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

target_nets = [
    "GND", "+3V3", "+5V", "+24V",
    "/MCU/SWDIO", "/MCU/SWCLK", "/MCU/NRST",
    "/COMMUNICATION/CAN_H", "/COMMUNICATION/CAN_L"
]

for t in target_nets:
    m = re.search(r'\(net\s+(\d+)\s+"' + re.escape(t) + r'"\)', text)
    if m:
        print(f'{t}: net index = {m.group(1)}')
    else:
        print(f'{t}: NOT FOUND')
