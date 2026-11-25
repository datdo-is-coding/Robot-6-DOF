import subprocess, re

cmd = ['git', 'show', 'a0922b7:Mechanical/PCB/foc_v2/foc_v2.kicad_pcb']
text = subprocess.check_output(cmd, encoding='utf-8')

blocks = text.split('(footprint ')
fps = ['J7', 'J8', 'J9', 'J10', 'J11', 'H1', 'H2', 'H3', 'H4', 'U1', 'IC1', 'U2', 'C_BULK1', 'C63']
for b in blocks[1:]:
    name = b.split('\n')[0].strip().strip('"')
    m_ref = re.search(r'\(property "Reference" "([^"]+)"', b)
    if m_ref and m_ref.group(1) in fps:
        ref = m_ref.group(1)
        m_at = re.search(r'\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)', b)
        at_str = m_at.group(0) if m_at else 'no pos'
        print(f'{ref:8s}: {at_str:25s} {name}')
