with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find all footprint starts
pos = 0
footprints = []
while True:
    idx = text.find('(footprint ', pos)
    if idx == -1:
        break
    # parse until matching closing parenthesis
    depth = 0
    end = idx
    for i in range(idx, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    fp_text = text[idx:end]
    # parse ref, at, layer
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
    ref = m_ref.group(1) if m_ref else "Unknown"
    m_at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', fp_text)
    if m_at:
        x = float(m_at.group(1))
        y = float(m_at.group(2))
        rot = float(m_at.group(3)) if m_at.group(3) else 0.0
    else:
        x, y, rot = 0, 0, 0
    m_layer = re.search(r'\(layer\s+"([^"]+)"\)', fp_text)
    layer = m_layer.group(1) if m_layer else ""
    footprints.append({'ref': ref, 'x': x, 'y': y, 'rot': rot, 'layer': layer, 'text': fp_text})
    pos = end

print(f"Total footprints found: {len(footprints)}")
print("References:", sorted([f['ref'] for f in footprints]))
