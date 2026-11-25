import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

connectors = ['J7', 'J8', 'J9', 'J10', 'J11']

for conn in connectors:
    pattern = r'\(footprint\s+"([^"]+)"[\s\S]*?\(property\s+"Reference"\s+"' + conn + r'"[\s\S]*?\n\t\)'
    m = re.search(pattern, text)
    if m:
        block = m.group(0)
        fp_name = re.search(r'\(footprint\s+"([^"]+)"', block).group(1)
        val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block).group(1)
        at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', block)
        layer = re.search(r'\(layer\s+"([^"]+)"\)', block).group(1)
        print(f"{conn}: val={val}, fp={fp_name}, at=({at_m.group(1)}, {at_m.group(2)}), rot={at_m.group(3)}, layer={layer}")
