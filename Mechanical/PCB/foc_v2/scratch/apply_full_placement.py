import os, uuid, re, math

# Load clean_step3.kicad_pcb
with open("scratch/clean_step3.kicad_pcb", "r", encoding="utf-8") as f:
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

print(f"Total footprints: {len(fp_blocks)}")

# Target positions and rotations:
# (x, y, rot)
positions = {
    # 4 Connectors (South bank)
    "J8": (79.0, 118.0, 0),
    "J9": (90.0, 118.0, 0),
    "J7": (101.5, 120.2, 0),
    "J10": (113.0, 118.0, 0),
    # Power connector (East bank)
    "J11": (122.5, 100.0, 90),
    # Phase terminals
    "J1": (84.0, 69.5, 0),
    "J2": (100.0, 68.0, 0),
    "J3": (116.0, 69.5, 0),
    # 6 MOSFETs
    "Q1": (81.0, 76.5, 0),
    "Q2": (87.0, 76.5, 180),
    "Q3": (97.0, 76.5, 0),
    "Q4": (103.0, 76.5, 180),
    "Q5": (113.0, 76.5, 0),
    "Q6": (119.0, 76.5, 180),
    # 3 Shunts
    "R47": (87.0, 83.5, 90),
    "R48": (103.0, 83.5, 90),
    "R49": (119.0, 83.5, 90),
    # Gate resistors
    "R1": (85.5, 87.5, 0),
    "R2": (88.5, 87.5, 0),
    "R3": (97.0, 87.5, 0),
    "R4": (100.0, 87.5, 0),
    "R5": (108.5, 87.5, 0),
    "R7": (111.5, 87.5, 0),
    # Gate Driver
    "IC1": (100.0, 92.5, 0),
    # MCU
    "U1": (100.0, 105.5, 0),
    # CAN transceiver & USB ESD
    "U9": (84.5, 112.5, 0),
    "U8": (101.5, 114.5, 0),
    # Power Input & Protection
    "D6": (123.0, 108.0, 90),
    "F1": (123.0, 92.0, 90),
    "U10": (114.0, 98.0, 0),
    # Bulk Caps
    "C63": (75.5, 78.5, 0),
    "C_BULK1": (124.5, 78.5, 0),
    # Crystal
    "Y1": (91.0, 105.5, 0),
    "C8": (88.5, 104.5, 90),
    "C9": (88.5, 106.5, 90),
    "R44": (91.0, 108.0, 0),
}

updated_count = 0
for start, end, ref in fp_blocks:
    if ref in positions:
        target_x, target_y, target_rot = positions[ref]
        for idx in range(start, end):
            if lines[idx].strip().startswith("(at "):
                lines[idx] = f"\t\t(at {target_x} {target_y} {target_rot})\n"
                updated_count += 1
                break

print(f"Updated {updated_count} component placements.")

with open("scratch/clean_step4.kicad_pcb", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Saved scratch/clean_step4.kicad_pcb successfully!")
