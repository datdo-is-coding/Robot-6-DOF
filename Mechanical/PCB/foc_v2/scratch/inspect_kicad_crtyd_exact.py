import json

with open('scratch/drc_final_pure_circle.json') as f:
    d = json.load(f)

for v in d['violations']:
    if v['type'] == 'courtyards_overlap':
        print(v['description'])
        for item in v['items']:
            print("  ", item)
