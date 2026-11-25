with open('scratch/test_edge_drc.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'Edge\.Cuts', text)]
print("Total occurrences of Edge.Cuts:", len(matches))
for idx in matches[1:]:
    print("--- Edge.Cuts line ---")
    print(text[max(0, idx-60):min(len(text), idx+100)])
