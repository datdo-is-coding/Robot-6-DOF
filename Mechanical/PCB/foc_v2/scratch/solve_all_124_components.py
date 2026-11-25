import math, re

# Let's write the complete solver and placement generator
# First, let's load all footprints and parse their text blocks from foc_v2.kicad_pcb
with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import test_courtyards
local_boxes = test_courtyards.parse_footprints()

def get_fp_dict():
    pos = 0
    fps = {}
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
        m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
        if m_ref:
            fps[m_ref.group(1)] = fp_text
        pos = end
    return fps

fp_dict = get_fp_dict()
print(f"Loaded {len(fp_dict)} footprint raw blocks.")
