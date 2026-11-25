import re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract footprints
fps = re.findall(r'\(footprint\s+"([^"]+)"\s+\(layer\s+"([^"]+)"\)\s+\(uuid\s+"([^"]+)"\)(.*?)\n\t\)', text, flags=re.DOTALL)
print(f"Total footprints found: {len(fps)}")

items = []
for fp_name, layer, fp_uuid, body in fps:
    # find reference
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', body)
    ref = m_ref.group(1) if m_ref else "Unknown"
    # find pos and rot
    m_at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', body)
    if m_at:
        x = float(m_at.group(1))
        y = float(m_at.group(2))
        rot = float(m_at.group(3)) if m_at.group(3) else 0.0
    else:
        x, y, rot = 0, 0, 0
    items.append((ref, fp_name, layer, x, y, rot, fp_uuid))

print("Sample footprints:")
for item in sorted(items, key=lambda x: x[0])[:25]:
    print(f"  {item[0]:8s} at ({item[3]:6.2f}, {item[4]:6.2f}) rot={item[5]:5.1f} layer={item[2]:8s} fp={item[1][:30]}")
