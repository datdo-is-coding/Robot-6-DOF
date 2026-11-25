import os, uuid, re, math

print("1. Reading original clean foc_v2.kicad_pcb...")
with open("foc_v2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# ==========================================================
# 1. UPDATE EDGE.CUTS (around lines 32568 - 32611)
# ==========================================================
ec_start = -1
ec_end = -1
for i, l in enumerate(lines):
    if '(layer "Edge.Cuts")' in l:
        # find the start of the first gr_arc / gr_line
        if ec_start == -1:
            for k in range(i, max(0, i-10), -1):
                if lines[k].startswith("\t(gr_"):
                    ec_start = k
                    break
        # update ec_end
        for k in range(i, min(len(lines), i+10)):
            if lines[k].startswith("\t)"):
                ec_end = k
                break

print(f"Edge.Cuts lines: {ec_start+1} to {ec_end+1}")

new_ec_lines = [
    '\t(gr_line\n',
    '\t\t(start 75.5051 125)\n',
    '\t\t(end 124.4949 125)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-south-flat-line")\n',
    '\t)\n',
    '\t(gr_arc\n',
    '\t\t(start 124.4949 125)\n',
    '\t\t(mid 128.7611 119.9449)\n',
    '\t\t(end 132 114.1774)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-se-corner-arc")\n',
    '\t)\n',
    '\t(gr_line\n',
    '\t\t(start 132 114.1774)\n',
    '\t\t(end 132 85.8226)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-east-flat-line")\n',
    '\t)\n',
    '\t(gr_arc\n',
    '\t\t(start 132 85.8226)\n',
    '\t\t(mid 119.0891 70.6639)\n',
    '\t\t(end 100 65)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-ne-corner-arc")\n',
    '\t)\n',
    '\t(gr_arc\n',
    '\t\t(start 100 65)\n',
    '\t\t(mid 75.2513 75.2513)\n',
    '\t\t(end 65 100)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-nw-corner-arc")\n',
    '\t)\n',
    '\t(gr_arc\n',
    '\t\t(start 65 100)\n',
    '\t\t(mid 67.733 113.5587)\n',
    '\t\t(end 75.5051 125)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-sw-corner-arc")\n',
    '\t)\n',
]

lines = lines[:ec_start] + new_ec_lines + lines[ec_end+1:]
print("Updated Edge.Cuts")

# ==========================================================
# 2. UPDATE 8 SCREW HEAD KEEPOUTS (PCD 44 mm)
# ==========================================================
def gen_poly_lines(cx, cy, r=3.0, n=32):
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n
        px = cx + r * math.cos(ang)
        py = cy + r * math.sin(ang)
        pts.append(f"(xy {px:.6f} {py:.6f})")
    out = []
    for k in range(0, len(pts), 4):
        out.append("\t\t\t\t" + " ".join(pts[k:k+4]) + "\n")
    return out

# Scan lines for (zone ... (name "M2.5 screw head clearance")
i = 0
while i < len(lines):
    if lines[i].strip() == "(zone":
        # check if this zone is M2.5 screw head clearance
        is_screw_ko = False
        zone_end = -1
        pts_start = -1
        pts_end = -1
        for k in range(i, min(len(lines), i+60)):
            if '(name "M2.5 screw head clearance")' in lines[k]:
                is_screw_ko = True
            if lines[k].strip() == "(pts":
                pts_start = k
            if pts_start != -1 and lines[k].strip() == ")":
                pts_end = k
            if lines[k].strip() == ")" and k > i + 10:
                zone_end = k
                break
        
        if is_screw_ko and pts_start != -1 and pts_end != -1:
            # find average x and y of old points to determine quadrant
            old_pts_text = "".join(lines[pts_start:pts_end])
            coords = re.findall(r'\(xy ([-0-9.]+) ([-0-9.]+)\)', old_pts_text)
            avg_x = sum(float(x) for x, y in coords) / len(coords)
            avg_y = sum(float(y) for x, y in coords) / len(coords)
            
            if avg_x < 100 and avg_y < 100:
                new_c = (84.444, 84.444)
            elif avg_x > 100 and avg_y < 100:
                new_c = (115.556, 84.444)
            elif avg_x < 100 and avg_y > 100:
                new_c = (84.444, 115.556)
            else:
                new_c = (115.556, 115.556)
            
            new_poly = ["\t\t\t(pts\n"] + gen_poly_lines(new_c[0], new_c[1]) + ["\t\t\t)\n"]
            lines = lines[:pts_start] + new_poly + lines[pts_end+1:]
            print(f"Updated screw keepout at line {i+1} to center {new_c}")
            i = pts_start + len(new_poly)
            continue
    i += 1

# ==========================================================
# 3. UPDATE FOOTPRINTS: H1..H4, J8, J9, J10, J7, J11
# ==========================================================
# Load mod files for JST XH
p3 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
p5 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod"

with open(p3, "r", encoding="utf-8") as f:
    mod3_lines = f.readlines()
with open(p5, "r", encoding="utf-8") as f:
    mod5_lines = f.readlines()

def build_fp_lines(mod_lines, fp_name, ref, val, x, y, rot, path, sheetname, sheetfile, fp_uuid, pad_nets):
    out = [
        f'\t(footprint "{fp_name}"\n',
        f'\t\t(layer "F.Cu")\n',
        f'\t\t(uuid "{fp_uuid}")\n',
        f'\t\t(at {x} {y} {rot})\n',
        f'\t\t(property "Reference" "{ref}"\n',
        f'\t\t\t(at 2.5 -3.5 {rot})\n',
        f'\t\t\t(layer "F.SilkS")\n',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
        f'\t\t)\n',
        f'\t\t(property "Value" "{val}"\n',
        f'\t\t\t(at 2.5 11.5 {rot})\n',
        f'\t\t\t(layer "F.Fab")\n',
        f'\t\t\t(hide yes)\n',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
        f'\t\t)\n',
        f'\t\t(property "Footprint" "{fp_name}"\n',
        f'\t\t\t(at 0 0 {rot})\n',
        f'\t\t\t(layer "F.Fab")\n',
        f'\t\t\t(hide yes)\n',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
        f'\t\t)\n',
        f'\t\t(property "Datasheet" ""\n',
        f'\t\t\t(at 0 0 {rot})\n',
        f'\t\t\t(layer "F.Fab")\n',
        f'\t\t\t(hide yes)\n',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
        f'\t\t)\n',
        f'\t\t(property "Description" ""\n',
        f'\t\t\t(at 0 0 {rot})\n',
        f'\t\t\t(layer "F.Fab")\n',
        f'\t\t\t(hide yes)\n',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
        f'\t\t)\n',
        f'\t\t(path "{path}")\n',
        f'\t\t(sheetname "{sheetname}")\n',
        f'\t\t(sheetfile "{sheetfile}")\n',
        f'\t\t(attr through_hole)\n',
    ]
    
    # Find start of graphic/pad elements (after all properties)
    start_body = 0
    for idx, line in enumerate(mod_lines):
        if line.startswith('\t(duplicate_pad_numbers_are_jumpers') or line.startswith('\t(fp_line'):
            start_body = idx
            break

    in_pad = None
    pad_lines = []
    for line in mod_lines[start_body:]:
        stripped = line.strip()
        if stripped.startswith('(pad "'):
            in_pad = stripped.split('"')[1]
            pad_lines = [line]
            continue
        if in_pad:
            pad_lines.append(line)
            if stripped == ")":
                net_name = pad_nets.get(in_pad, "")
                pad_lines.pop() # remove ')'
                if net_name:
                    pad_lines.append(f'\t\t(net "{net_name}")\n')
                pad_lines.append(f'\t\t(uuid "{str(uuid.uuid4())}")\n')
                pad_lines.append('\t)\n')
                for pl in pad_lines:
                    out.append('\t' + pl)
                in_pad = None
            continue
        if stripped == ")" and line == mod_lines[-1]:
            continue
        out.append('\t' + line)
        
    out.append('\t)\n')
    return out

fp_j8_lines = build_fp_lines(
    mod3_lines, "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal",
    "J8", "Conn_01x03_MountingPin", 79.5, 119.5, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/c41a4043-0de8-4c55-a88b-648ceae017c3/76631f46-810c-4f88-99e6-e9e6bbe901b0",
    "/COMMUNICATION/", "communication.kicad_sch",
    "76631f46-810c-4f88-99e6-e9e6bbe901b0",
    {"1": "/COMMUNICATION/CAN_H", "2": "/COMMUNICATION/CAN_L", "3": "GND"}
)

fp_j9_lines = build_fp_lines(
    mod3_lines, "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal",
    "J9", "Conn_01x03_MountingPin", 90.5, 119.5, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/c41a4043-0de8-4c55-a88b-648ceae017c3/8ba114b8-86cd-4514-8dd7-644af4102cf4",
    "/COMMUNICATION/", "communication.kicad_sch",
    "8ba114b8-86cd-4514-8dd7-644af4102cf4",
    {"1": "/COMMUNICATION/CAN_H", "2": "/COMMUNICATION/CAN_L", "3": "GND"}
)

fp_j10_lines = build_fp_lines(
    mod5_lines, "Connector_JST:JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal",
    "J10", "SWD", 112.5, 119.5, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/6a6ae277-51ef-46ec-a09b-86576920fc4f/fdf38b01-c2ba-4054-8b77-5c33166b802e",
    "/MCU/", "MCU.kicad_sch",
    "443c9290-4a7d-44bc-87ca-ae2112af1efc",
    {"1": "+3V3", "2": "/MCU/SWDIO", "3": "/MCU/SWCLK", "4": "/MCU/NRST", "5": "GND"}
)

# Collect all footprint blocks
fp_blocks = []
in_fp = False
start_idx = -1
curr_ref = None

for i, l in enumerate(lines):
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        start_idx = i
        curr_ref = None
    elif in_fp:
        if '(property "Reference" ' in l:
            ref = l.split('"')[3]
            curr_ref = ref
        elif l.startswith("\t)") or l.startswith(")"):
            fp_blocks.append((start_idx, i, curr_ref))
            in_fp = False

hole_positions = {
    "H3": (84.444, 84.444),
    "H4": (115.556, 84.444),
    "H2": (84.444, 115.556),
    "H1": (115.556, 115.556)
}

fp_replacements = {
    "J8": fp_j8_lines,
    "J9": fp_j9_lines,
    "J10": fp_j10_lines
}

for start, end, ref in sorted(fp_blocks, key=lambda x: x[0], reverse=True):
    if ref in fp_replacements:
        print(f"Replacing footprint {ref} (lines {start+1}..{end+1})")
        lines = lines[:start] + fp_replacements[ref] + lines[end+1:]
    elif ref in hole_positions:
        hx, hy = hole_positions[ref]
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = f"\t\t(at {hx} {hy})\n"
                print(f"Updated hole {ref} position to ({hx}, {hy})")
                break
    elif ref == "J7":
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = "\t\t(at 101.5 121.2 0)\n"
                print("Updated J7 position to (101.5, 121.2, 0)")
                break
    elif ref == "J11":
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = "\t\t(at 122.0 100.0 90)\n"
                print("Updated J11 position to (122.0, 100.0, 90)")
                break

with open("scratch/clean_step3.kicad_pcb", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Saved scratch/clean_step3.kicad_pcb successfully!")
