import os

for fname in os.listdir('.'):
    if fname.endswith('.kicad_sch'):
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
            for r in ['R37', 'R38', 'R39', 'U8', 'Q7', 'D1', 'D2', 'D3', 'R33', 'R35', 'R36', 'J10']:
                if f'"{r}"' in content or f' {r} ' in content:
                    print(f"{r} is in {fname}")
