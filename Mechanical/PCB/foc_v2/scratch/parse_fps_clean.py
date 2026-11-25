import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# split by top-level footprints
fps = re.split(r'\n\t\(footprint ', text)
for fp in fps[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    if ref in ['D4', 'F1', 'JP1', 'U9', 'R45', 'R46']:
        at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', fp)
        layer_m = re.search(r'\(layer\s+"([^"]+)"\)', fp)
        fp_name = fp.split('"')[0]
        at = at_m.groups() if at_m else ()
        layer = layer_m.group(1) if layer_m else ""
        print(f"Ref: {ref:<5} Pos: {at} Layer: {layer}")
        # print CrtYd
        for line in fp.splitlines():
            if 'CrtYd' in line and ('start' in line or 'end' in line or 'fp_rect' in line):
                print("   ", " ".join(line.split()))
            elif 'fp_line' in line and 'uuid' not in line:
                pass
