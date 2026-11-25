import os, uuid, re

# Load mod files
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
    
    in_pad = None
    pad_lines = []
    for line in mod_lines[1:]:
        stripped = line.strip()
        if stripped.startswith('(property "Reference"') or stripped.startswith('(property "Value"') or stripped.startswith('(property "Footprint"'):
            continue
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

# Read pcb_step2
with open("scratch/pcb_step2.kicad_pcb", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Collect footprint blocks
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

# We will replace in reverse order of start_idx so line numbers remain valid
fp_replacements = {
    "J8": fp_j8_lines,
    "J9": fp_j9_lines,
    "J10": fp_j10_lines
}

for start, end, ref in sorted(fp_blocks, key=lambda x: x[0], reverse=True):
    if ref in fp_replacements:
        print(f"Replacing {ref} (lines {start+1} to {end+1})")
        lines = lines[:start] + fp_replacements[ref] + lines[end+1:]
    elif ref == "J7":
        # Update J7 position in place
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = "\t\t(at 101.5 121.2 0)\n"
                print(f"Updated J7 position to (101.5, 121.2, 0)")
                break
    elif ref == "J11":
        # Update J11 position in place
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = "\t\t(at 122.0 100.0 90)\n"
                print(f"Updated J11 position to (122.0, 100.0, 90)")
                break

with open("scratch/pcb_step3.kicad_pcb", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Saved scratch/pcb_step3.kicad_pcb successfully!")
