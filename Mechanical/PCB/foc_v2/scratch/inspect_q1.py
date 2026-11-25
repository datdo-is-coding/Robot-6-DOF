import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"Q1"', block)
    if ref_m:
        print("=== Q1 FOOTPRINT ===")
        print("Name:", block.split('\n')[0])
        # print crtyd
        lines = re.findall(r'\(fp_line\s+\(start\s+([^\)]+)\)\s+\(end\s+([^\)]+)\)[\s\S]*?\(layer\s+"F\.CrtYd"\)', block)
        for s, e in lines:
            print(f"  CrtYd: {s} -> {e}")
        pads = re.findall(r'\(pad\s+"([^"]*)"[\s\S]*?\(at\s+([^\)]+)\)', block)
        for p, at in pads[:6]:
            print(f"  Pad {p} at {at}")
        break
