import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# find any occurrence of "(zone "
zone_starts = [m.start() for m in re.finditer(r'\(zone\b', text)]
print(f"Total zone occurrences: {len(zone_starts)}")
for i, start in enumerate(zone_starts[:15]):
    snippet = text[start:start+300]
    print(f"--- Zone #{i+1} ---")
    print(snippet)
