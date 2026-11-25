import json

with open('scratch/drc_final.json') as f:
    drc = json.load(f)

for v in drc.get('violations', []):
    if v['type'] == 'courtyards_overlap':
        descs = [it.get('description', '') for it in v.get('items', [])]
        if any('H3' in d for d in descs) and any('R1' in d for d in descs):
            print("Found H3 vs R1 in DRC!")
            break
else:
    print("H3 vs R1 was NOT in KiCad DRC! (Only in AABB approximation)")
