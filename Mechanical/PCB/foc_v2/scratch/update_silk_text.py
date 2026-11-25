with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('D70  4x2.7 PCD26', 'D70  4x2.7 PCD44')

with open('foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated silkscreen text to PCD44.")
