import re

def inspect_symbol(sch_file, ref_names):
    with open(sch_file, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"=== {sch_file} ===")
    for ref in ref_names:
        m = re.search(r'\(symbol[\s\S]*?\(property "Reference" "' + ref + r'"[\s\S]*?\n\t\)', content)
        if not m:
            m = re.search(r'\(symbol [^\n]+[\s\S]*?\(property "Reference" "' + ref + r'"[\s\S]*?\n  \)', content)
        if m:
            print(f"Found {ref}:")
            for line in m.group(0).splitlines():
                if "property " in line or "at " in line:
                    print("  ", line.strip())
        else:
            print(f"Not found {ref}")

inspect_symbol("communication.kicad_sch", ["J8", "J9"])
inspect_symbol("MCU.kicad_sch", ["J10"])
