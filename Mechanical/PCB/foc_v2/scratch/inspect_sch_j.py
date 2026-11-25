import re

for sf in ['communication.kicad_sch', 'MCU.kicad_sch', 'foc_v2.kicad_sch']:
    with open(sf, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"=== {sf} ===")
    symbols = text.split('(symbol ')
    for s in symbols[1:]:
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', s)
        if ref_m and ref_m.group(1).startswith('J'):
            val_m = re.search(r'\(property "Value" "([^"]+)"', s)
            fp_m = re.search(r'\(property "Footprint" "([^"]+)"', s)
            print(f"  {ref_m.group(1):5s} | {val_m.group(1) if val_m else '':20s} | {fp_m.group(1) if fp_m else ''}")
