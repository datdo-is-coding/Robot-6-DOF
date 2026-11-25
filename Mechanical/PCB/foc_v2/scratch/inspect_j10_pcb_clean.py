with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(property "Reference" "J10"')
if idx != -1:
    print(text[max(0, idx-200):idx+500])
