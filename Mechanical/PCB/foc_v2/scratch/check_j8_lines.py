with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "J8"' in l:
        for j in range(max(0, i-5), min(len(lines), i+35)):
            print(lines[j].rstrip())
        break
