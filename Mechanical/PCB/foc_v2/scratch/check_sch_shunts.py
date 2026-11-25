import re

with open('gatedrv.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

for ref in ['R47', 'R48', 'R49', 'NT1', 'NT2']:
    m = re.search(r'\(symbol\b.*?"Reference"\s+"' + ref + r'".*?\n\t\)', text, re.DOTALL)
    if m:
        block = m.group(0)
        at = re.search(r'\(at\s+([\d\.-]+)\s+([\d\.-]+)(?:\s+([\d\.-]+))?\)', block)
        print(f"Ref {ref} at {at.groups() if at else 'unknown'}")
        # find pins
        pins = re.findall(r'\(pin\s+"([^"]+)"', block)
        print(f"  Pins: {pins}")
