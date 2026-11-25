with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(name "M2.5 screw head clearance")')
if idx != -1:
    print(text[max(0, idx-100):idx+400])
