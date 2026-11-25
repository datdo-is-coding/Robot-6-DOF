with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(8170, min(len(lines), 8230)):
    print(lines[j].rstrip())
