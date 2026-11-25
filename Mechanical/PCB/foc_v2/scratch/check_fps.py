with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re

fps = ['J7', 'J8', 'J9', 'J10', 'J1', 'J2', 'J3', 'J11', 'Q1', 'IC1', 'U1', 'U2', 'C_BULK1', 'C63', 'H1', 'H2', 'H3', 'H4']

# KiCad 8/9/10 format: (footprint "..." ... (property "Reference" "J7" ...) ... (at X Y [rot]))
blocks = text.split('(footprint ')
for b in blocks[1:]:
    name = b.split('\n')[0].strip().strip('"')
    m_ref = re.search(r'\(property "Reference" "([^"]+)"', b)
    if m_ref and m_ref.group(1) in fps:
        ref = m_ref.group(1)
        m_at = re.search(r'\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)', b)
        at_str = m_at.group(0) if m_at else 'no pos'
        print(f'{ref:8s}: {at_str:25s} {name}')
