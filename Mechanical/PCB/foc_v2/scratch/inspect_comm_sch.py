import re
with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

symbols = text.split('(symbol ')
for s in symbols[1:]:
    if 'Conn_01x03' in s:
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', s)
        val_m = re.search(r'\(property "Value" "([^"]+)"', s)
        fp_m = re.search(r'\(property "Footprint" "([^"]+)"', s)
        print("Ref:", ref_m.group(1) if ref_m else "None")
        print("Val:", val_m.group(1) if val_m else "None")
        print("FP:", fp_m.group(1) if fp_m else "None")
        print("-" * 20)
