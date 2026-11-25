with open("MCU.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "220.98" in l and ("wire" in l or "label" in l or "pin" in l):
        for j in range(max(0, i-2), min(len(lines), i+6)):
            print(lines[j].rstrip())
