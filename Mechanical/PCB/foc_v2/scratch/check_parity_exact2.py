import json

with open("scratch/drc_final_test.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

print(json.dumps(drc.get('schematic_parity', []), indent=2))
