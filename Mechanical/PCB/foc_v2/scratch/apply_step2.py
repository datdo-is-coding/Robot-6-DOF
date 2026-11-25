import re, math

with open("scratch/pcb_step1.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

# Define 32-point polygon generator for radius 3.0mm
def gen_poly_pts(cx, cy, r=3.0, n=32):
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n
        px = cx + r * math.cos(ang)
        py = cy + r * math.sin(ang)
        pts.append(f"(xy {px:.6f} {py:.6f})")
    # format in lines of 4 points
    lines = []
    for k in range(0, len(pts), 4):
        lines.append("\t\t\t\t" + " ".join(pts[k:k+4]))
    return "\n" + "\n".join(lines) + "\n\t\t\t"

# 4 hole centers:
holes = [
    (84.444, 84.444),   # NW (H3)
    (115.556, 84.444),  # NE (H4)
    (84.444, 115.556),  # SW (H2)
    (115.556, 115.556), # SE (H1)
]

# There are 8 keepout zones: 4 on F.Cu, 4 on B.Cu
# Each has (name "M2.5 screw head clearance")
# Let's find all zones named "M2.5 screw head clearance"
zones = re.findall(r'(\t\(zone[\s\S]*?\(name "M2\.5 screw head clearance"[\s\S]*?\n\t\))', pcb)
print(f"Found {len(zones)} screw head keepout zones.")

for i, z in enumerate(zones):
    # Find which hole it originally belonged to by checking average of pts
    pts_xy = re.findall(r'\(xy ([-0-9.]+) ([-0-9.]+)\)', z)
    avg_x = sum(float(x) for x, y in pts_xy) / len(pts_xy)
    avg_y = sum(float(y) for x, y in pts_xy) / len(pts_xy)
    
    # Match to closest old hole center
    # Old centers: (90.8076, 90.8076), (109.1924, 90.8076), (90.8076, 109.1924), (109.1924, 109.1924)
    if avg_x < 100 and avg_y < 100:
        target_center = (84.444, 84.444)
    elif avg_x > 100 and avg_y < 100:
        target_center = (115.556, 84.444)
    elif avg_x < 100 and avg_y > 100:
        target_center = (84.444, 115.556)
    else:
        target_center = (115.556, 115.556)
    
    new_pts_str = gen_poly_pts(target_center[0], target_center[1])
    # Replace (pts ...) inside this zone
    new_z = re.sub(r'\(pts[\s\S]*?\n\t\t\t\)', f'(pts{new_pts_str})', z)
    pcb = pcb.replace(z, new_z)
    print(f"Zone {i+1} updated to center {target_center}")

with open("scratch/pcb_step2.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(pcb)
print("Saved scratch/pcb_step2.kicad_pcb")
