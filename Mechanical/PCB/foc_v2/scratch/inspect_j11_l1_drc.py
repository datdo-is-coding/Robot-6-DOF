import json

with open('scratch/drc_final.json') as f:
    drc = json.load(f)

for v in drc.get('violations', []):
    if v['type'] == 'courtyards_overlap':
        items = v.get('items', [])
        descs = [it.get('description', '') for it in items]
        if any('J11' in d for d in descs) and any('L1' in d for d in descs):
            print(json.dumps(v, indent=2))
            break
