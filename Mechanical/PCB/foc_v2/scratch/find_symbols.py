import re

with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

symbols = re.findall(r'\(symbol "([^"]+)"', text)
for s in sorted(set(symbols)):
    print(s)
