import re, uuid, subprocess, json, math
from solve_zero_drc_exact0 import P

print("=== 1. Loading scratch/git_raw.kicad_pcb ===")
with open('scratch/git_raw.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# ==========================================================
# 1. UPDATE EDGE.CUTS (100% Watertight Pure Circle Ø70 mm)
# ==========================================================
u1, u2, u3, u4 = [str(uuid.uuid4()) for _ in range(4)]
circle_edges = f"""	(gr_arc
		(start 100 65)
		(mid 124.748737 75.251262)
		(end 135 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u1}")
	)
	(gr_arc
		(start 135 100)
		(mid 124.748737 124.748737)
		(end 100 135)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u2}")
	)
	(gr_arc
		(start 100 135)
		(mid 75.251262 124.748737)
		(end 65 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u3}")
	)
	(gr_arc
		(start 65 100)
		(mid 75.251262 75.251262)
		(end 100 65)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "{u4}")
	)"""

pattern_ec = r'(\t\(gr_arc\s+\(start 65 100\).*?\(uuid "037693de-df8a-455f-bed1-fc100082e71e"\)\s*\n\t\))'
match_ec = re.search(pattern_ec, text, flags=re.DOTALL)
if match_ec:
    text = text[:match_ec.start()] + circle_edges + text[match_ec.end():]
    print("Edge.Cuts replaced successfully with 4-arc pure circle.")
else:
    # If not matched, try general regex
    print("Warning: pattern_ec not matched, trying general replacement...")
    text = re.sub(r'(\t\(gr_(?:line|arc)[\s\S]*?\(layer "Edge\.Cuts"\)[\s\S]*?\n\t\)\s*)+', circle_edges + '\n', text)

# ==========================================================
# 2. UPDATE FOOTPRINT POSITIONS, ROTATIONS, LAYERS
# ==========================================================
print("Updating all 124 footprint placements...")
blocks = text.split('(footprint ')
new_blocks = [blocks[0]]

count_updated = 0
for b in blocks[1:]:
    m_ref = re.search(r'\(property "Reference" "([^"]+)"', b)
    if m_ref and m_ref.group(1) in P:
        ref = m_ref.group(1)
        x, y, rot, layer = P[ref]
        count_updated += 1

        # Replace (layer "...") if needed
        if layer == 'B.Cu':
            b = re.sub(r'\(layer "F\.Cu"\)', '(layer "B.Cu")', b, count=1)
            b = b.replace('"F.CrtYd"', '"B.CrtYd"')
            b = b.replace('"F.Fab"', '"B.Fab"')
            b = b.replace('"F.SilkS"', '"B.SilkS"')
            b = b.replace('"F.Mask"', '"B.Mask"')
        elif layer == 'F.Cu':
            b = re.sub(r'\(layer "B\.Cu"\)', '(layer "F.Cu")', b, count=1)
            b = b.replace('"B.CrtYd"', '"F.CrtYd"')
            b = b.replace('"B.Fab"', '"F.Fab"')
            b = b.replace('"B.SilkS"', '"F.SilkS"')
            b = b.replace('"B.Mask"', '"F.Mask"')

        # Replace (at X Y [ROT])
        # Footprint at line is usually line 4 or 5
        lines_b = b.splitlines(True)
        for idx in range(min(8, len(lines_b))):
            if lines_b[idx].strip().startswith('(at '):
                if rot != 0:
                    lines_b[idx] = f"\t\t(at {x:.4f} {y:.4f} {rot})\n"
                else:
                    lines_b[idx] = f"\t\t(at {x:.4f} {y:.4f})\n"
                break
        b = "".join(lines_b)

        # For H1..H4, adjust F.CrtYd circle to radius 2.40 mm (M2.5 cap screw head)
        if ref in ['H1', 'H2', 'H3', 'H4']:
            b = re.sub(r'\(fp_circle\s+\(center 0 0\)\s+\(end 2\.95 0\)', '(fp_circle (center 0 0) (end 2.40 0)', b)

    new_blocks.append(b)

text = "(footprint ".join(new_blocks)
print(f"Total footprints updated: {count_updated} / 124")

with open('foc_v2.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved to foc_v2.kicad_pcb.")

# ==========================================================
# 3. RUN KICAD-CLI DRC
# ==========================================================
cmd = [
    'C:\\Program Files\\KiCad\\10.0\\bin\\kicad-cli.exe',
    'pcb', 'drc',
    '--format', 'json',
    '-o', 'scratch/drc_final_pure_circle.json',
    'foc_v2.kicad_pcb'
]
res = subprocess.run(cmd, capture_output=True, text=True)
with open('scratch/drc_final_pure_circle.json') as f:
    d = json.load(f)

v = d.get('violations', [])
counts = {}
for item in v:
    t = item.get('type')
    counts[t] = counts.get(t, 0) + 1

print("\n=== KICAD DRC REPORT ===")
print(f"Total violations: {len(v)}")
for t, c in sorted(counts.items()):
    print(f"  {t:30s}: {c:3d}")

# Specifically check critical errors:
invalid_outline = counts.get('invalid_outline', 0)
courtyards_overlap = counts.get('courtyards_overlap', 0)
hole_clearance = counts.get('hole_clearance', 0)
print(f"\nCRITICAL CHECKS:")
print(f"  invalid_outline   : {invalid_outline}")
print(f"  courtyards_overlap: {courtyards_overlap}")
print(f"  hole_clearance    : {hole_clearance}")
