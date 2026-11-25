with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(380, 410):
    print(lines[j].rstrip())
