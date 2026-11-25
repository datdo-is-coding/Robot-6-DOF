import json

with open("scratch/drc_verified_parity3.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

for item in drc.get("schematic_parity", []):
    print(item.get("type"), "-", item.get("description"))
