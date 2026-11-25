with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "J10"' in l:
        print("Found line:", i+1)
        for j in range(max(0, i-5), min(len(lines), i+35)):
            print(lines[j].rstrip())
        break
