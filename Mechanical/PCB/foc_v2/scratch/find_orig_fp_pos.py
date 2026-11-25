import re

content = open('foc_v2.kicad_pcb', 'r', encoding='utf-8').read()
for ref in ['C63', 'C_BULK1', 'J11', 'F1', 'D6', 'L1', 'D4']:
    m = re.search(r'\(footprint \"[^\"]+\"[^)]*?\n\s+\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)[^)]*?\n\s+\(property \"Reference\" \"' + ref + r'\"', content)
    if not m:
        m = re.search(r'\(property \"Reference\" \"' + ref + r'\"[^)]*?\n\s+\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)', content)
    # search full footprint block
    fp_m = re.search(r'\(footprint [^\n]+\n(?:[^\n]+\n)+?\s+\(property "Reference" "' + ref + r'"(?:[^\n]+\n)+?\)', content)
    if fp_m:
        at_m = re.search(r'\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)', fp_m.group(0))
        if at_m:
            print(f"{ref:8s}: at {at_m.group(1)} {at_m.group(2)} {at_m.group(3)}")
