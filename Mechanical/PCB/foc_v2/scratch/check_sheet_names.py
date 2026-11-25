with open("foc_v2.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'\(property "Sheetname" "([^"]+)"[\s\S]*?\(property "Sheetfile" "([^"]+)"', text)
for m in matches:
    print(m)
