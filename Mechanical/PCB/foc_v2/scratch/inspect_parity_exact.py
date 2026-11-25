import json

with open("scratch/drc_unrouted.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

print(json.dumps(drc['schematic_parity'], indent=2))
