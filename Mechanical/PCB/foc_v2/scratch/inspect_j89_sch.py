import re

with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

for ref in ['J8', 'J9']:
    m = re.search(r'\(symbol\s+[\s\S]*?\(property\s+"Reference"\s+"' + ref + r'"[\s\S]*?\n\t\)', text)
    if m:
        fp = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', m.group(0))
        val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', m.group(0))
        print(f"{ref}: val={val.group(1) if val else ''}, fp={fp.group(1) if fp else ''}")
    else:
        # search with instances
        print(f"{ref} search by instances...")
        for b in text.split('(symbol '):
            if f'(reference "{ref}")' in b:
                fp = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', b)
                val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', b)
                print(f"  {ref}: val={val.group(1) if val else ''}, fp={fp.group(1) if fp else ''}")
