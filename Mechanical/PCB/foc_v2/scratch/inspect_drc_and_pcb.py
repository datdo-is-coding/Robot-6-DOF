import json

with open('scratch/drc_final.json') as f:
    drc = json.load(f)

overlaps = [v for v in drc.get('violations', []) if v['type'] == 'courtyards_overlap']
print(f"Total courtyard overlaps in DRC: {len(overlaps)}")

for i, v in enumerate(overlaps):
    items = v.get('items', [])
    names = []
    for it in items:
        names.append(f"{it.get('description', '')} at {it.get('pos')}")
    print(f"[{i+1}] {' <--> '.join(names)}")
