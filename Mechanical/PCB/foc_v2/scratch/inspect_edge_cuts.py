import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

edge_cuts = re.findall(r'\(gr_[^\)]+layer\s+"Edge\.Cuts"[^\)]*\)', text)
if not edge_cuts:
    # multiline search
    edge_cuts = re.findall(r'\(gr_\w+\s+.*?\blayer\s+"Edge\.Cuts".*?\)', text, re.DOTALL)

print(f"Total Edge.Cuts items: {len(edge_cuts)}")
for e in edge_cuts:
    print(e.strip())
