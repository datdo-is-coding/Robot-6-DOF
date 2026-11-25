with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
pads = re.findall(r'\(pad\s+"[^"]+"\s+[^)]+\(net\s+[^)]+\)', text)
print(f"Found {len(pads)} pads with net")
for p in pads[:10]:
    print(p)
