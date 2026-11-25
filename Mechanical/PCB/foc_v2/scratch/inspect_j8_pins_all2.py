with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for j in range(5870, 5920):
    print(lines[j])
