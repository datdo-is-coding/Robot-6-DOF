with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# 1. Edge.Cuts
print("--- EDGE.CUTS ---")
for i, line in enumerate(lines):
    if "Edge.Cuts" in line:
        print(f"Line {i+1}: {line.strip()}")
        # print context
        for j in range(max(0, i-2), min(len(lines), i+4)):
            print(f"  {lines[j].strip()}")

# 2. Footprints of interest
targets = {"H1", "H2", "H3", "H4", "J1", "J2", "J3", "J7", "J8", "J9", "J10", "J11"}
curr_fp = None
curr_ref = None
curr_pos = None

for line in lines:
    stripped = line.strip()
    if stripped.startswith("(footprint "):
        curr_fp = stripped.split()[1].strip('"')
        curr_ref = None
        curr_pos = None
    elif stripped.startswith("(at "):
        if curr_pos is None:
            curr_pos = stripped
    elif stripped.startswith('(property "Reference" '):
        ref = stripped.split('"')[3]
        curr_ref = ref
        if ref in targets:
            print(f"Footprint {ref}: {curr_fp} at {curr_pos}")

# 3. Keepouts
print("\n--- KEEPOUTS ---")
in_zone = False
zone_header = ""
for line in lines:
    stripped = line.strip()
    if stripped.startswith("(zone"):
        in_zone = True
        zone_header = stripped
    elif in_zone:
        if "keepout" in stripped:
            print(f"Zone keepout: {stripped}")
        if stripped == ")":
            in_zone = False
