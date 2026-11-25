import re

with open('work/2026-11-13-pcb-layout/before-grid.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

segments = re.findall(r'\(segment\s+\(start\s+[\d\.-]+\s+[\d\.-]+\)\s+\(end\s+[\d\.-]+\s+[\d\.-]+\).*?\(net\s+"([^"]+)"\).*?\)', text, re.DOTALL)
spa_segs = re.findall(r'\(segment\s+\(start\s+[\d\.-]+\s+[\d\.-]+\)\s+\(end\s+[\d\.-]+\s+[\d\.-]+\).*?\(net\s+"(/GATE_DRV/SP[ABC])"\).*?\)', text, re.DOTALL)

print(f"Total segments: {len(segments)}")
print(f"SPA/SPB/SPC segments: {len(spa_segs)}")

# search for exact segments with net SPA
spa_blocks = re.findall(r'\(segment\b[^\)]+\(net\s+"/GATE_DRV/SPA"\)[^\)]*\)', text)
if not spa_blocks:
    # search across multiple lines
    for m in re.finditer(r'\(segment\b.*?\(/GATE_DRV/SPA\).*?\)', text, re.DOTALL):
        print(m.group(0))
    # let's just search for /GATE_DRV/SPA in text
    lines = text.split('\n')
    for i, l in enumerate(lines):
        if '/GATE_DRV/SPA"' in l:
            for j in range(max(0, i-4), min(len(lines), i+5)):
                print(lines[j])
            print("---")
            if i > 1000: break
