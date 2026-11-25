with open("MCU.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "J10"' in l:
        for j in range(max(0, i-10), min(len(lines), i+30)):
            print(lines[j].rstrip())
        break
