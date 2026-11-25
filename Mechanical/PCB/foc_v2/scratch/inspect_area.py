import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

fp_blocks = re.findall(r'\(footprint\s+.*?\n\t\)', content, re.DOTALL)
for b in fp_blocks:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', b)
    at_m = re.search(r'\(at\s+([\d\.-]+)\s+([\d\.-]+)', b)
    if ref_m and at_m:
        ref = ref_m.group(1)
        x = float(at_m.group(1))
        y = float(at_m.group(2))
        if 80 <= x <= 125 and 75 <= y <= 90:
            print(f"Ref {ref:<8} at ({x:.2f}, {y:.2f})")
