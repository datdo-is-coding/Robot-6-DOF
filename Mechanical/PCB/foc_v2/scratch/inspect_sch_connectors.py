import re

files = ["communication.kicad_sch", "MCU.kicad_sch", "foc_v2.kicad_sch"]
for fn in files:
    try:
        with open(fn, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"=== {fn} ===")
        syms = re.findall(r'\(symbol[\s\S]*?\(property "Reference" "([^"]+)"[\s\S]*?\(property "Value" "([^"]+)"[\s\S]*?\(property "Footprint" "([^"]+)"', content)
        for ref, val, fp in syms:
            if ref.startswith("J") or ref.startswith("H"):
                print(f"  {ref} ({val}): {fp}")
    except Exception as e:
        print(f"Error {fn}: {e}")
