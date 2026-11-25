import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# find all footprints
fps = re.findall(r'\(footprint "([^"]+)"', text)
print(f"Total footprints: {len(fps)}")

# list all footprints with ref, value, layer, position
pattern = re.compile(
    r'\(footprint "([^"]+)"\s+'
    r'(?:\(layer "([^"]+)"\)\s+)?'
    r'.*?'
    r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)'
    r'.*?'
    r'\(property "Reference" "([^"]+)"',
    re.DOTALL
)

matches = pattern.findall(text)
print(f"Matched footprints: {len(matches)}")

# Let's inspect references
refs = {}
for m in matches:
    fp_name, layer, x, y, rot, ref = m
    refs[ref] = {
        'fp': fp_name,
        'layer': layer,
        'x': float(x),
        'y': float(y),
        'rot': float(rot) if rot else 0.0
    }

print("Sample refs:", list(refs.keys())[:20])
print(f"Total unique refs: {len(refs)}")
