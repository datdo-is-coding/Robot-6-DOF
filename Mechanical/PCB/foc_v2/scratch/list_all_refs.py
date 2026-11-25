with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
parts = text.split('(footprint ')
refs = []
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m:
        refs.append(ref_m.group(1))

print(f"Total footprints in foc_v2.kicad_pcb: {len(refs)}")
print("Unique footprints:", len(set(refs)))
# Group by prefix:
from collections import defaultdict
grouped = defaultdict(list)
for r in sorted(refs):
    prefix = re.match(r'[A-Za-z_]+', r).group(0)
    grouped[prefix].append(r)

for k, v in sorted(grouped.items()):
    print(f"  {k} ({len(v)}): {', '.join(v)}")
