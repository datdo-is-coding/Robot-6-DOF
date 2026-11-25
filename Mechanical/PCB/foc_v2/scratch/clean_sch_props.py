with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re

props_to_remove = ["KLC_S3.3", "KLC_S4.1", "Availability", "Price", "SNAPEDA_PN"]

for p in props_to_remove:
    # regex to remove (property "<p>" ... )
    pattern = r'\t\t\(property\s+"' + re.escape(p) + r'"[\s\S]*?\t\t\)\n'
    text = re.sub(pattern, '', text)

with open("communication.kicad_sch", "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned up extra properties from communication.kicad_sch")
