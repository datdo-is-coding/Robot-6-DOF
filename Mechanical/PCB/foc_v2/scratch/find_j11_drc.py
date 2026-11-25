import json

with open('scratch/drc_final.json') as f:
    drc = json.load(f)

for v in drc.get('violations', []):
    for it in v.get('items', []):
        d = it.get('description', '')
        if 'J11' in d:
            print(d, it.get('pos'))
