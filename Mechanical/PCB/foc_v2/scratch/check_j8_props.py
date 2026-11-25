with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find J8 properties
j8_idx = text.find('(property "Reference" "J8"')
j8_end = text.find('(instances', j8_idx)
print("J8 properties in sch:")
print(text[j8_idx:j8_end])
