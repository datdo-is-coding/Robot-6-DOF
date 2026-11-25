import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

fps = re.split(r'\n\t\(footprint ', text)
for fp in fps[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    if ref in ['J7', 'J8', 'J9', 'J10', 'J11', 'H1', 'H2', 'H3', 'H4']:
        fp_name = fp.split('"')[0]
        at_m = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)(?:\s+([0-9.-]+))?\)', fp)
        at = at_m.groups() if at_m else ()
        print(f"{ref:<5}: {fp_name:<50} at {at}")
