import re
import os

sch_files = [f for f in os.listdir('.') if f.endswith('.kicad_sch')]
print("Schematic files:", sch_files)

for sf in sch_files:
    with open(sf, 'r', encoding='utf-8') as f:
        text = f.read()
    for ref in ['J7', 'J8', 'J9', 'J10', 'J11']:
        if f'"{ref}"' in text:
            # find symbol
            sym_m = re.findall(r'\(symbol\s+[\s\S]*?\(property\s+"Reference"\s+"' + ref + r'"[\s\S]*?\n\t\)', text)
            for sm in sym_m:
                val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', sm)
                fp = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', sm)
                print(f"{sf}: {ref} val={val.group(1) if val else ''} fp={fp.group(1) if fp else ''}")
