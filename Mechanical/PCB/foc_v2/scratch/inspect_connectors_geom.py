import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

def get_fp_text(ref):
    m = re.search(r'(\(footprint\s+"[^"]+"[\s\S]*?\(property\s+"Reference"\s+"' + ref + r'"[\s\S]*?\n\t\))', text)
    return m.group(1) if m else None

for ref in ['J7', 'J8', 'J9', 'J10', 'H1', 'H2', 'H3', 'H4']:
    print(f"=== {ref} ===")
    t = get_fp_text(ref)
    if not t:
        print("Not found")
        continue
    # print layer, at, lines
    at_m = re.search(r'\(at\s+([^\)]+)\)', t)
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', t)
    print("  at:", at_m.group(1) if at_m else "none")
    print("  layer:", layer_m.group(1) if layer_m else "none")
    # print lines on crtyd or fab
    for line in t.split('\n'):
        if 'fp_line' in line or 'fp_rect' in line or 'fp_poly' in line or 'fp_circle' in line or 'pad' in line:
            if 'CrtYd' in line or 'Fab' in line or 'Edge' in line:
                print("    ", line.strip())
