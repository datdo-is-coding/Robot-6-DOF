import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if ref_m and ref_m.group(1) in ['J7', 'J8', 'J9', 'J10']:
        ref = ref_m.group(1)
        print(f"=== {ref} ===")
        at_m = re.search(r'\(at\s+([^\)]+)\)', block)
        print("  at:", at_m.group(1))
        # print all pads
        pads = re.findall(r'\(pad\s+"[^"]*"\s+\w+\s+\w+\s+\(at\s+([^\)]+)\)', block)
        print(f"  Pads ({len(pads)}):", pads[:3], "...")
        # find crtyd
        crtyd = re.findall(r'\(fp_line\s+\(start\s+([^\)]+)\)\s+\(end\s+([^\)]+)\)[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)', block)
        print("  CrtYd lines:", len(crtyd))
        for s, e in crtyd:
            print(f"    line: {s} -> {e}")
        # check fp_rect
        rects = re.findall(r'\(fp_rect\s+\(start\s+([^\)]+)\)\s+\(end\s+([^\)]+)\)[\s\S]*?\(layer\s+"[FB]\.CrtYd"\)', block)
        for s, e in rects:
            print(f"    rect: {s} -> {e}")
