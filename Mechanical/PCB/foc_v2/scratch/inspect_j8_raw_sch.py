import re

with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

for b in text.split('(symbol '):
    if '"J8"' in b:
        print("=== J8 symbol block ===")
        for line in b.splitlines()[:20]:
            print(" ", line)
