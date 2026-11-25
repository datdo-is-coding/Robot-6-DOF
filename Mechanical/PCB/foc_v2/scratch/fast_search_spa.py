with open('work/2026-11-13-pcb-layout/before-grid.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Read {len(lines)} lines")
count = 0
for i, line in enumerate(lines):
    if '"/GATE_DRV/SPA"' in line:
        count += 1
        print(f"Match at line {i+1}:")
        for j in range(max(0, i-6), min(len(lines), i+4)):
            print(f"  {lines[j].strip()}")
        print("-" * 30)
        if count >= 5:
            break
print(f"Total matches: {count}")
