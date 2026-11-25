with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(property "Reference" "R1"')
if idx != -1:
    idx2 = text.find('(pad ', idx)
    print(text[idx2:idx2+600])
