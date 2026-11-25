import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

footprints = re.findall(r'(\(footprint\s+"([^"]+)"\s+\(layer\s+"([^"]+)"\).*?\(uuid\s+"([^"]+)"\)\s*\n\t\))', text, flags=re.DOTALL)

for fp, name, layer, uid in footprints:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp)
    ref = ref_m.group(1) if ref_m else ""
    if ref in ['D4', 'F1', 'JP1', 'U9', 'R45', 'R46']:
        at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', fp)
        at = at_m.groups() if at_m else ()
        print(f"Ref: {ref}, Layer: {layer}, At: {at}, Name: {name}")
        # find crt lines
        crt_lines = re.findall(r'\((?:fp_line|fp_rect|fp_poly).*?\(layer\s+"[^"]*CrtYd"\).*?\)', fp, flags=re.DOTALL)
        for cl in crt_lines[:5]:
            print("   ", " ".join(cl.split()))
