with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(property "Reference" "J10"')
end_idx = text.find('(footprint ', idx)
print(text[idx:idx+1500])
