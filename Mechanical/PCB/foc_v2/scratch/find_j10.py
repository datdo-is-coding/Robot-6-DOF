import re, glob

for sch in glob.glob('*.kicad_sch'):
    with open(sch, 'r', encoding='utf-8') as f:
        text = f.read()
    if 'J10' in text:
        print(f"=== Found in {sch} ===")
        symbols = text.split('(symbol')
        for s in symbols:
            if '"J10"' in s:
                for line in s.split('\n')[:25]:
                    print(" ", line)
