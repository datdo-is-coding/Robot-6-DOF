with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    git_text = f.read()

import re
git_arcs = re.findall(r'\(gr_arc[^)]+\(layer "Edge\.Cuts"\)[^)]*\)', git_text, flags=re.DOTALL)
print("Git Edge.Cuts elements count:", len(git_arcs))
for a in git_arcs:
    print(a)
    print('---')
