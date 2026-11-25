import re

with open('foc_v2.kicad_pcb', 'r') as f:
    text = f.read()

# find H1 or H2 block
for b in text.split('(footprint '):
    if '"H1"' in b or '"H2"' in b:
        print("=== Mounting Hole Block ===")
        for line in b.splitlines()[:30]:
            print(" ", line)
        break
