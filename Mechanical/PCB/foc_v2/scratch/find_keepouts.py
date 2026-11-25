with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

import re
zones = re.findall(r'\(zone[\s\S]*?\n  \)', pcb)
print(f"Total zones: {len(zones)}")
for i, z in enumerate(zones):
    if "keepout" in z:
        lines = z.strip().split("\n")
        print(f"\nKeepout zone {i}:")
        for l in lines[:10]:
            print(f"  {l}")
        # print pts
        pts = re.findall(r'\(xy ([-0-9.]+) ([-0-9.]+)\)', z)
        print(f"  Points ({len(pts)}): {pts[:4]} ... {pts[-2:] if len(pts)>2 else ''}")
