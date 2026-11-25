with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for j in range(825, 875):
    print(lines[j].rstrip())
