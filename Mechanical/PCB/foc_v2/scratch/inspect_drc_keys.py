import json

with open("scratch/drc_unrouted.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

print("Keys:", list(drc.keys()))
for k in drc.keys():
    if k not in ["coordinate_units", "date", "kicad_version", "source"]:
        print(f"{k}: count = {len(drc[k]) if isinstance(drc[k], list) else drc[k]}")
