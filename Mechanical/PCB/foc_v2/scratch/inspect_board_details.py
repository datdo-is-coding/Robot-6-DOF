import re

with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

# Find Edge.Cuts
print("--- EDGE.CUTS ---")
edge_cuts = re.findall(r'\(gr_[^)]+\(layer "Edge.Cuts"\)[^)]*\)', pcb)
for ec in edge_cuts:
    print(ec)

# Find mounting holes H1..H4
print("\n--- MOUNTING HOLES ---")
for h in ["H1", "H2", "H3", "H4"]:
    m = re.search(r'(\(footprint[^\n]+MountingHole[^\n]+Reference "' + h + r'"[\s\S]*?\n  \))', pcb)
    if not m:
        # try general footprint with Reference "H"
        m = re.search(r'(\(footprint [^\n]+[\s\S]*?Reference "' + h + r'"[\s\S]*?\n  \))', pcb)
    if m:
        # print position and footprint name
        fp_str = m.group(1)
        fp_line = fp_str.split("\n")[0]
        pos_m = re.search(r'\(at ([-0-9.]+) ([-0-9.]+)(?: ([-0-9.]+))?\)', fp_str)
        print(f"{h}: {fp_line} at {pos_m.group(0) if pos_m else 'None'}")

# Find connectors J7, J8, J9, J10, J11, J1, J2, J3
print("\n--- CONNECTORS ---")
for j in ["J1", "J2", "J3", "J7", "J8", "J9", "J10", "J11"]:
    m = re.search(r'(\(footprint [^\n]+[\s\S]*?Reference "' + j + r'"[\s\S]*?\n  \))', pcb)
    if m:
        fp_str = m.group(1)
        fp_line = fp_str.split("\n")[0]
        pos_m = re.search(r'\(at ([-0-9.]+) ([-0-9.]+)(?: ([-0-9.]+))?\)', fp_str)
        print(f"{j}: {fp_line} at {pos_m.group(0) if pos_m else 'None'}")

# Find keepout zones
print("\n--- KEEPOUTS ---")
keepouts = re.findall(r'(\(zone[\s\S]*?\(keepout[\s\S]*?\n  \))', pcb)
for ko in keepouts:
    net_m = re.search(r'\(net [0-9]+', ko)
    name_m = re.search(r'\(name "([^"]+)"', ko)
    pts_m = re.search(r'\(pts[\s\S]*?\)', ko)
    print(f"Keepout: {name_m.group(1) if name_m else 'unnamed'}, pts count: {len(re.findall(r'\(xy', pts_m.group(0))) if pts_m else 0}")
