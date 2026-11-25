with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '(property "Reference" "J7"' in l:
        print(f"J7 is around line {i+1}")
        for j in range(max(0, i-15), min(len(lines), i+60)):
            print(lines[j].rstrip())
        break
