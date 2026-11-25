import re

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = text.split('(footprint ')
for b in blocks[1:]:
    m_ref = re.search(r'\(property "Reference" "([^"]+)"', b)
    if m_ref:
        ref = m_ref.group(1)
        m_at = re.search(r'\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)', b)
        m_layer = re.search(r'\(layer "([^"]+)"\)', b)
        pos = m_at.group(0) if m_at else 'no pos'
        layer = m_layer.group(1) if m_layer else 'no layer'
        if ref in ['U8', 'C59', 'Q7', 'R40', 'R41', 'R42', 'R43', 'U9', 'U10', 'D6', 'F1', 'J11', 'L1', 'D4']:
            print(f"{ref:6s}: {pos:25s} {layer}")
