import re

try:
    content = open('foc_v2.kicad_pcb', 'r', encoding='utf-8').read()
    # Find footprints and their reference and at
    blocks = re.findall(r'\(footprint [^)]+\n(?:\s+\([^\n]+\n)+', content)
    for ref in ['J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54']:
        m = re.search(r'\(property "Reference" "' + ref + r'"\n\s+\(at ([0-9.-]+) ([0-9.-]+)(?: ([0-9.-]+))?\)', content)
        if m:
            print(ref, m.groups())
except Exception as e:
    print(e)
