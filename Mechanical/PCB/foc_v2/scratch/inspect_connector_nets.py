import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

fp_blocks = re.findall(r'\(footprint\s+.*?\n\t\)', text, re.DOTALL)
for b in fp_blocks:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(J\d+)"', b)
    if ref_m:
        ref = ref_m.group(1)
        pads = re.findall(r'\(pad\s+"?([^"\s]+)"?\s+([^\s]+).*?\(net\s+"([^"]*)"\)', b, re.DOTALL)
        print(f"\nConnector {ref}:")
        for p in pads:
            print(f"   Pad {p[0]:<4} ({p[1]}): net '{p[2]}'")
