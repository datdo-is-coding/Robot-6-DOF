with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(17730, 17780):
    print(lines[j].rstrip())
