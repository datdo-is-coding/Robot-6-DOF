import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    if ref_m and ref_m.group(1) in ['J8', 'J7', 'J10']:
        ref = ref_m.group(1)
        print(f"=== {ref} ===")
        for line in p.split('\n'):
            if any(k in line for k in ['(fp_rect', '(fp_line', '(fp_circle', '(start', '(end', '(center', 'F.CrtYd', 'F.Fab']):
                print("  ", line.strip())
