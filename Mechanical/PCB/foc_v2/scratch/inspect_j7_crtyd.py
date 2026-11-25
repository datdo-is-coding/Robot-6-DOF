import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split('(footprint ')
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"J7"', p)
    if ref_m:
        lines = p.split('\n')
        for i, l in enumerate(lines):
            if 'F.CrtYd' in l:
                # look up backwards to find (fp_line
                k = i
                while k > 0 and '(fp_line' not in lines[k]:
                    k -= 1
                print("\n".join(lines[k:i+1]))
