import os, uuid, re, math

print("=== 1. Loading foc_v2_orig.kicad_pcb ===")
with open("scratch/foc_v2_orig.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# ==========================================================
# 1. UPDATE EDGE.CUTS (Watertight outline with y=130 and x=132 cuts)
# ==========================================================
ec_start = -1
ec_end = -1
for i, l in enumerate(lines):
    if '(layer "Edge.Cuts")' in l:
        if ec_start == -1:
            for k in range(i, max(0, i-10), -1):
                if lines[k].startswith("\t(gr_"):
                    ec_start = k
                    break
        for k in range(i, min(len(lines), i+10)):
            if lines[k].startswith("\t)"):
                ec_end = k
                break

# South flat cut at y = 130.0:
# dy = 30.0, dx = sqrt(35^2 - 30^2) = sqrt(325) = 18.027756
# x1 = 100 - 18.027756 = 81.972244, x2 = 100 + 18.027756 = 118.027756
# East flat cut at x = 132.0:
# dx = 32.0, dy = sqrt(35^2 - 32^2) = sqrt(201) = 14.177447
# y1 = 100 - 14.177447 = 85.822553, y2 = 100 + 14.177447 = 114.177447

new_ec_lines = [
    '\t(gr_line\n',
    '\t\t(start 81.9722 130)\n',
    '\t\t(end 118.0278 130)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-south-flat-line")\n',
    '\t)\n',
    '\t(gr_arc\n',
    '\t\t(start 118.0278 130)\n',
    '\t\t(mid 126.7909 123.0182)\n',
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
    '\t\t(mid 70.0891 121.2679)\n',
    '\t\t(end 81.9722 130)\n',
    '\t\t(stroke (width 0.05) (type default))\n',
    '\t\t(layer "Edge.Cuts")\n',
    '\t\t(uuid "edge-sw-corner-arc")\n',
    '\t)\n',
]

lines = lines[:ec_start] + new_ec_lines + lines[ec_end+1:]
print("Updated Edge.Cuts to watertight outline with y=130 South cut and x=132 East cut.")

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

i = 0
while i < len(lines):
    if lines[i].strip() == "(zone":
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
# 3. BUILD JST XH FOOTPRINTS FOR J8, J9, J10
# ==========================================================
p3 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
p5 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod"

with open(p3, "r", encoding="utf-8") as f:
    mod3_lines = f.readlines()
with open(p5, "r", encoding="utf-8") as f:
    mod5_lines = f.readlines()

def build_fp_lines(mod_lines, fp_name, ref, val, x, y, rot, path, sheetname, sheetfile, fp_uuid, pad_nets, extra_props=None):
    out = [
        f'\t(footprint "{fp_name}"\n',
        f'\t\t(layer "F.Cu")\n',
        f'\t\t(uuid "{fp_uuid}")\n',
        f'\t\t(at {x} {y} {rot})\n',
        f'\t\t(property "Reference" "{ref}"\n',
        f'\t\t\t(at 0 -4.0 {rot})\n',
        f'\t\t\t(layer "F.SilkS")\n',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
        f'\t\t)\n',
        f'\t\t(property "Value" "{val}"\n',
        f'\t\t\t(at 0 11.5 {rot})\n',
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
        f'\t\t(property "Description" "{extra_props.get(\"Description\", \"\") if extra_props else \"\"}"\n',
        f'\t\t\t(at 0 0 {rot})\n',
        f'\t\t\t(layer "F.Fab")\n',
        f'\t\t\t(hide yes)\n',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
        f'\t\t)\n',
    ]
    if extra_props:
        for k, v in extra_props.items():
            if k == "Description": continue
            out.extend([
                f'\t\t(property "{k}" "{v}"\n',
                f'\t\t\t(at 0 0 {rot})\n',
                f'\t\t\t(layer "F.Fab")\n',
                f'\t\t\t(hide yes)\n',
                f'\t\t\t(uuid "{str(uuid.uuid4())}")\n',
                f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))\n',
                f'\t\t)\n',
            ])
    out.extend([
        f'\t\t(path "{path}")\n',
        f'\t\t(sheetname "{sheetname}")\n',
        f'\t\t(sheetfile "{sheetfile}")\n',
        f'\t\t(attr through_hole)\n',
    ])
    
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
                pad_lines.pop()
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
    "J8", "Conn_01x03", 85.0, 120.0, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/c41a4043-0de8-4c55-a88b-648ceae017c3/76631f46-810c-4f88-99e6-e9e6bbe901b0",
    "/COMMUNICATION/", "communication.kicad_sch",
    "76631f46-810c-4f88-99e6-e9e6bbe901b0",
    {"1": "/COMMUNICATION/CAN_H", "2": "/COMMUNICATION/CAN_L", "3": "GND"},
    extra_props={"LCSC Part #": "C293630", "KLC_S3.3": "", "KLC_S4.1": "", "Availability": "", "Price": "", "SNAPEDA_PN": "", "Description": "Generic connectable mounting pin connector, single row, 01x03, script generated (kicad-library-utils/schlib/autogen/connector/)"}
)

fp_j9_lines = build_fp_lines(
    mod3_lines, "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal",
    "J9", "Conn_01x03", 95.0, 120.0, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/c41a4043-0de8-4c55-a88b-648ceae017c3/8ba114b8-86cd-4514-8dd7-644af4102cf4",
    "/COMMUNICATION/", "communication.kicad_sch",
    "8ba114b8-86cd-4514-8dd7-644af4102cf4",
    {"1": "/COMMUNICATION/CAN_H", "2": "/COMMUNICATION/CAN_L", "3": "GND"},
    extra_props={"LCSC Part #": "C293630", "KLC_S3.3": "", "KLC_S4.1": "", "Availability": "", "Price": "", "SNAPEDA_PN": "", "Description": "Generic connectable mounting pin connector, single row, 01x03, script generated (kicad-library-utils/schlib/autogen/connector/)"}
)

fp_j10_lines = build_fp_lines(
    mod5_lines, "Connector_JST:JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal",
    "J10", "SWD", 114.0, 120.0, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/6a6ae277-51ef-46ec-a09b-86576920fc4f/fdf38b01-c2ba-4054-8b77-5c33166b802e",
    "/MCU/", "MCU.kicad_sch",
    "443c9290-4a7d-44bc-87ca-ae2112af1efc",
    {"1": "+3V3", "2": "/MCU/SWDIO", "3": "/MCU/SWCLK", "4": "/MCU/NRST", "5": "GND"},
    extra_props={}
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
        lines = lines[:start] + fp_replacements[ref] + lines[end+1:]
    elif ref in hole_positions:
        hx, hy = hole_positions[ref]
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = f"\t\t(at {hx} {hy})\n"
                break

# ==========================================================
# 4. MASTER PLACEMENT DICTIONARY: ALL 124 COMPONENTS
# ==========================================================
# Load dictionary from scratch/test_complete_placement.py
import sys
sys.path.append("scratch")
from test_complete_placement import placements

print(f"Applying placement for all {len(placements)} components...")

# Re-scan footprint blocks after replacements
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

count_updated = 0
for start, end, ref in fp_blocks:
    if ref in placements:
        tx, ty, trot, _, _, _ = placements[ref]
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = f"\t\t(at {tx} {ty} {trot})\n"
                count_updated += 1
                break

print(f"Successfully placed {count_updated} components!")

# Filter out old obsolete tracks and vias that belonged to old component locations
clean_lines = []
in_track = False
for l in lines:
    if l.startswith("\t(segment ") or l.startswith("(segment ") or l.startswith("\t(via ") or l.startswith("(via "):
        in_track = True
    elif in_track:
        if l.startswith("\t)") or l.startswith(")"):
            in_track = False
    else:
        clean_lines.append(l)

with open("foc_v2.kicad_pcb", "w", encoding="utf-8") as f:
    f.writelines(clean_lines)

print("Saved foc_v2.kicad_pcb successfully!")
