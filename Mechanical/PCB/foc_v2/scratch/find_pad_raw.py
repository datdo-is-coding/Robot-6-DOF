with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(pad ')
print("idx:", idx)
if idx != -1:
    print(text[idx:idx+500])
