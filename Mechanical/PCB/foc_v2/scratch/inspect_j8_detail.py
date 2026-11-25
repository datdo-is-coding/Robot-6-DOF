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

fp_j8 = get_fp('J8')
print("=== J8 ===")
for line in fp_j8.splitlines():
    if 'CrtYd' in line or 'pad' in line or 'fp_rect' in line or 'fp_line' in line:
        print(line)

fp_j10 = get_fp('J10')
print("=== J10 ===")
for line in fp_j10.splitlines():
    if 'CrtYd' in line or 'pad' in line or 'fp_rect' in line or 'fp_line' in line:
        print(line)
