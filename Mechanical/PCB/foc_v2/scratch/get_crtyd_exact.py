import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

fps = re.split(r'\n\t\(footprint ', text)
for fp in fps[1:]:
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp)
    if not ref_m:
        continue
    ref = ref_m.group(1)
    if ref in ['D4', 'F1', 'JP1', 'U9', 'R45', 'R46']:
        print(f"=== {ref} ===")
        # search for fp_line or fp_rect
        for item in re.finditer(r'\((fp_line|fp_rect|fp_poly)\s+(.*?)\n\t\t\)', fp, re.DOTALL):
            content = item.group(2)
            if 'CrtYd' in content:
                print(" ", " ".join(content.split()))
