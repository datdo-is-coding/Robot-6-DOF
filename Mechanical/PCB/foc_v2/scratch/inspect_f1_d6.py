import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(F1|D6)"', block)
    if ref_m:
        print(f"=== {ref_m.group(1)} ===")
        print("Name:", block.split('\n')[0].strip())
        lines = re.findall(r'\(fp_line\s+\(start\s+([^\)]+)\)\s+\(end\s+([^\)]+)\)[\s\S]*?\(layer\s+"F\.CrtYd"\)', block)
        for s, e in lines:
            print(f"  CrtYd: {s} -> {e}")
        rects = re.findall(r'\(fp_rect\s+\(start\s+([^\)]+)\)\s+\(end\s+([^\)]+)\)[\s\S]*?\(layer\s+"F\.CrtYd"\)', block)
        for s, e in rects:
            print(f"  CrtYd rect: {s} -> {e}")
