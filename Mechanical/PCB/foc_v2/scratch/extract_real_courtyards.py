import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_fp = False
curr_ref = None
fp_lines = []
footprints = {}

for l in lines:
    if l.startswith('\t(footprint ') or l.startswith('(footprint '):
        in_fp = True
        fp_lines = [l]
        curr_ref = None
    elif in_fp:
        fp_lines.append(l)
        if '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif l.startswith('\t)') or l.startswith(')'):
            if curr_ref:
                footprints[curr_ref] = fp_lines
            in_fp = False

print(f"Total footprints parsed: {len(footprints)}")

def inspect_crtyd(ref):
    if ref not in footprints:
        print(f"{ref} not found")
        return
    print(f"=== Footprint {ref} ===")
    lines = footprints[ref]
    for idx, l in enumerate(lines):
        if 'CrtYd' in l:
            # show surrounding lines
            for k in range(max(0, idx-5), min(len(lines), idx+5)):
                print(lines[k].rstrip())
            print("---")

inspect_crtyd('J11')
inspect_crtyd('Q1')
inspect_crtyd('H3')
inspect_crtyd('U1')
