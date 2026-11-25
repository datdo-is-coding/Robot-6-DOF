import json

with open("scratch/drc_verified_parity.json", "r", encoding="utf-8") as f:
    drc = json.load(f)

for k in drc:
    if "parity" in k:
        print(f"Key {k}: {len(drc[k])} items")
        for item in drc[k]:
            print(" ", item)
