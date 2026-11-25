import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find each footprint by finding (property "Reference" "REF") and searching backwards for (footprint and (at
refs = ['J1', 'J2', 'J3', 'J7', 'J8', 'J9', 'J10', 'H1', 'H2', 'H3', 'H4', 'C_BULK1', 'C63', 'IC1', 'U1', 'U2']
for ref in refs:
    patt = r'\((?:footprint|module)\s+"[^"]+"[\s\S]*?\(property\s+"Reference"\s+"' + ref + r'"'
    m = re.search(patt, text)
    if m:
        block = m.group(0)
        # find the (at ...) right after footprint
        at_m = re.search(r'\(at\s+([^\)]+)\)', block)
        print(f"{ref:8s}: {at_m.group(1) if at_m else 'unknown'}")
    else:
        print(f"{ref:8s}: NOT FOUND")
