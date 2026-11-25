import re

with open('MCU.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# find J10 symbol block
b = text.split('(property "Reference" "J10"')
if len(b) > 1:
    # print surrounding text
    print(b[0][-500:] + '(property "Reference" "J10"' + b[1][:1000])
