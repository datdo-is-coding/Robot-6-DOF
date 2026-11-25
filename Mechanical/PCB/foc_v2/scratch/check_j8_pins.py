import re

with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    sch = f.read()

for ref in ["J8", "J9"]:
    m = re.search(r'\(property "Reference" "' + ref + r'"[\s\S]*?\(uuid "[^"]+"\)\n\t\)', sch)
    if m:
        print(f"=== {ref} pins ===")
        for line in m.group(0).splitlines():
            if "(pin " in line:
                print(" ", line.strip())
