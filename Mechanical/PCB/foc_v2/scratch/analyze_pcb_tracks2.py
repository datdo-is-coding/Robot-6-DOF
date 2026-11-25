with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
track_nets = re.findall(r'\(segment[\s\S]*?\(net\s+"([^"]+)"\)', text)
via_nets = re.findall(r'\(via[\s\S]*?\(net\s+"([^"]+)"\)', text)

from collections import Counter
print("Top 15 track nets:")
for n, c in Counter(track_nets).most_common(15):
    print(f"  {n:30s}: {c}")

print("\nTop 15 via nets:")
for n, c in Counter(via_nets).most_common(15):
    print(f"  {n:30s}: {c}")
