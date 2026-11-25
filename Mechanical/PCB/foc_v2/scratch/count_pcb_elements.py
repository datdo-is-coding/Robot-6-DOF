with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
vias = re.findall(r'\(via\s+([^\)]+)\)', text)
print(f"Total vias in foc_v2.kicad_pcb: {len(vias)}")

tracks = re.findall(r'\(segment\s+([^\)]+)\)', text)
print(f"Total track segments in foc_v2.kicad_pcb: {len(tracks)}")
