with open('scratch/test_edge.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('74.0626 123.5')
print("Position:", pos, "out of", len(text))
print(text[max(0, pos-300):min(len(text), pos+300)])
