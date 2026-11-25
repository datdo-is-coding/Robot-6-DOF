with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re

def get_fp(ref_name):
    pos = 0
    while True:
        idx = text.find('(footprint ', pos)
        if idx == -1: break
        depth = 0
        end = idx
        for i in range(idx, len(text)):
            if text[i] == '(': depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        fp_text = text[idx:end]
        if f'(property "Reference" "{ref_name}"' in fp_text:
            return fp_text
        pos = end
    return None

connectors = ['J7', 'J8', 'J9', 'J10', 'H1', 'U1', 'IC1', 'Q1']
for c in connectors:
    fp = get_fp(c)
    if fp:
        lines = fp.splitlines()
        crtyd_lines = []
        for i, l in enumerate(lines):
            if 'CrtYd' in l:
                # get context
                for k in range(max(0, i-4), min(len(lines), i+4)):
                    crtyd_lines.append(lines[k].strip())
        print(f"=== {c} ===")
        print('\n'.join(crtyd_lines[:15]))
