import re

with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

tokens = re.split(r'\n\t\((?:footprint|module)\s+', text)
for block in tokens[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(F1|D6|J11|L1|D4)"', block)
    if ref_m:
        at_m = re.search(r'\(at\s+([^\)]+)\)', block)
        print(f"{ref_m.group(1):8s}: {at_m.group(1)}")
