import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if ref_m and ref_m.group(1) == 'J7':
        # print all fp_line with start and end and layer
        lines = re.findall(r'\(fp_line\s+\(start\s+([^\)]+)\)\s+\(end\s+([^\)]+)\)[\s\S]*?\(layer\s+"([^"]+)"\)', block)
        for s, e, l in lines:
            print(f"  {l:10s} : {s} -> {e}")
