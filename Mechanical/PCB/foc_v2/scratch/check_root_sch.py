with open("foc_v2.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
sheets = re.findall(r'\(sheet[\s\S]*?\n\t\)', text)
for s in sheets:
    print(s[:200])
