import json

with open('scratch/drc_final.json') as f:
    drc = json.load(f)

overlaps = []
for v in drc.get('violations', []):
    if v['type'] == 'courtyards_overlap':
        items = v.get('items', [])
        refs = []
        for it in items:
            desc = it.get('description', '')
            if 'Footprint ' in desc:
                refs.append(desc.split('Footprint ')[1])
            else:
                refs.append(desc)
        overlaps.append(tuple(sorted(refs)))

print(f"Total REAL KiCad courtyard overlaps: {len(overlaps)}")
from collections import Counter
c = Counter(overlaps)
for pair, count in sorted(c.items()):
    print(f"  {pair[0]:8s} <--> {pair[1]:8s}")
