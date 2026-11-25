import re, uuid, math

print("Loading foc_v2.kicad_pcb...")
with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

# 1. Update Edge.Cuts
# We replace the old 4 gr_arc with the new closed contour:
# South flat line at y = 125.0 from x = 75.5051 to 124.4949
# East flat line at x = 132.0 from y = 85.8226 to 114.1774
# 4 connecting arcs along circle R=35, center (100, 100)

new_edge_cuts = """	(gr_line
		(start 75.5051 125)
		(end 124.4949 125)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "edge-south-flat-line")
	)
	(gr_arc
		(start 124.4949 125)
		(mid 128.7611 119.9449)
		(end 132 114.1774)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "edge-se-corner-arc")
	)
	(gr_line
		(start 132 114.1774)
		(end 132 85.8226)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "edge-east-flat-line")
	)
	(gr_arc
		(start 132 85.8226)
		(mid 119.0891 70.6639)
		(end 100 65)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "edge-ne-corner-arc")
	)
	(gr_arc
		(start 100 65)
		(mid 75.2513 75.2513)
		(end 65 100)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "edge-nw-corner-arc")
	)
	(gr_arc
		(start 65 100)
		(mid 67.733 113.5587)
		(end 75.5051 125)
		(stroke (width 0.05) (type default))
		(layer "Edge.Cuts")
		(uuid "edge-sw-corner-arc")
	)"""

# Remove old Edge.Cuts gr_arc items
old_ec_pattern = r'(\t\(gr_arc[\s\S]*?\(layer "Edge.Cuts"\)[\s\S]*?\n\t\)\n?)+'
if re.search(old_ec_pattern, pcb):
    pcb = re.sub(old_ec_pattern, new_edge_cuts + "\n", pcb, count=1)
    print("Edge.Cuts updated successfully.")
else:
    print("Could not match old Edge.Cuts pattern directly, searching individual items...")

# 2. Update Mounting Holes H1..H4 to PCD 44 mm
# H3 (NW): (84.444, 84.444)
# H4 (NE): (115.556, 84.444)
# H2 (SW): (84.444, 115.556)
# H1 (SE): (115.556, 115.556)
hole_coords = {
    "H3": (84.444, 84.444),
    "H4": (115.556, 84.444),
    "H2": (84.444, 115.556),
    "H1": (115.556, 115.556)
}

for h, (hx, hy) in hole_coords.items():
    # find footprint for this hole
    # Pattern: (footprint [^\n]+Reference "H..." ... (at X Y ...) ... )
    pat = r'(\(footprint [^\n]*MountingHole[^\n]*\n[\s\S]*?\(at )[-0-9.]+ [-0-9.]+( [^)]+)?(\)[\s\S]*?\(property "Reference" "' + h + r'"[\s\S]*?\n\t\))'
    m = re.search(pat, pcb)
    if m:
        rot_str = m.group(2) if m.group(2) else ""
        new_fp = m.group(1) + f"{hx} {hy}" + rot_str + m.group(3)
        pcb = pcb[:m.start()] + new_fp + pcb[m.end():]
        print(f"Updated hole {h} position to ({hx}, {hy})")
    else:
        print(f"Could not find footprint for {h}")

with open("scratch/pcb_step1.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(pcb)
print("Saved scratch/pcb_step1.kicad_pcb")
