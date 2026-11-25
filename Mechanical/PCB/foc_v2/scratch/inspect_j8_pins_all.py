with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for j in range(5830, 5870):
    print(lines[j])
