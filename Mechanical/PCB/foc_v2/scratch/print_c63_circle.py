import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"C63"', block)
    if ref_m:
        circles = re.findall(r'\(fp_circle[\s\S]*?\(layer\s+"F\.CrtYd"\)[\s\S]*?\)', block)
        for c in circles:
            print("CrtYd circle:", c)
        pads = re.findall(r'\(pad\s+"[^"]*"[\s\S]*?\(at\s+([^\)]+)\)', block)
        print("Pads at:", pads)
        break
