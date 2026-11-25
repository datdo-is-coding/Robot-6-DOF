import re

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(J7|J8|J9|J10|H1|H2|H3|H4)"', block)
    if ref_m:
        at_m = re.search(r'\(at\s+([^\)]+)\)', block)
        print(f"{ref_m.group(1):8s}: {at_m.group(1)}")
