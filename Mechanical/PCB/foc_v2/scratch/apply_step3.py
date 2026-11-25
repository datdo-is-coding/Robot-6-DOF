import re, uuid

p3 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
p5 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod"

with open(p3, "r", encoding="utf-8") as f:
    mod3_lines = f.readlines()

with open(p5, "r", encoding="utf-8") as f:
    mod5_lines = f.readlines()

def build_fp(mod_lines, fp_name, ref, val, x, y, rot, path, sheetname, sheetfile, fp_uuid, pad_nets):
    out = [
        f'\t(footprint "{fp_name}"',
        f'\t\t(layer "F.Cu")',
        f'\t\t(uuid "{fp_uuid}")',
        f'\t\t(at {x} {y} {rot})',
        f'\t\t(property "Reference" "{ref}"',
        f'\t\t\t(at 2.5 -3.5 {rot})',
        f'\t\t\t(layer "F.SilkS")',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))',
        f'\t\t)',
        f'\t\t(property "Value" "{val}"',
        f'\t\t\t(at 2.5 11.5 {rot})',
        f'\t\t\t(layer "F.Fab")',
        f'\t\t\t(hide yes)',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))',
        f'\t\t)',
        f'\t\t(property "Footprint" "{fp_name}"',
        f'\t\t\t(at 0 0 {rot})',
        f'\t\t\t(layer "F.Fab")',
        f'\t\t\t(hide yes)',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))',
        f'\t\t)',
        f'\t\t(property "Datasheet" ""',
        f'\t\t\t(at 0 0 {rot})',
        f'\t\t\t(layer "F.Fab")',
        f'\t\t\t(hide yes)',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))',
        f'\t\t)',
        f'\t\t(property "Description" ""',
        f'\t\t\t(at 0 0 {rot})',
        f'\t\t\t(layer "F.Fab")',
        f'\t\t\t(hide yes)',
        f'\t\t\t(uuid "{str(uuid.uuid4())}")',
        f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))',
        f'\t\t)',
        f'\t\t(path "{path}")',
        f'\t\t(sheetname "{sheetname}")',
        f'\t\t(sheetfile "{sheetfile}")',
        f'\t\t(attr through_hole)',
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
                # closing pad tag: insert net and uuid before closing )
                net_name = pad_nets.get(in_pad, "")
                # remove the closing ')' line, append net, uuid, then ')'
                pad_lines.pop()
                if net_name:
                    pad_lines.append(f'\t\t(net "{net_name}")\n')
                pad_lines.append(f'\t\t(uuid "{str(uuid.uuid4())}")\n')
                pad_lines.append('\t)\n')
                for pl in pad_lines:
                    out.append('\t' + pl.rstrip())
                in_pad = None
            continue
        if stripped == ")" and line == mod_lines[-1]:
            continue
        out.append('\t' + line.rstrip())
        
    out.append('\t)')
    return "\n".join(out)

# Build J8
fp_j8 = build_fp(
    mod3_lines, "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal",
    "J8", "Conn_01x03_MountingPin", 79.5, 119.5, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/c41a4043-0de8-4c55-a88b-648ceae017c3/76631f46-810c-4f88-99e6-e9e6bbe901b0",
    "/COMMUNICATION/", "communication.kicad_sch",
    "76631f46-810c-4f88-99e6-e9e6bbe901b0",
    {"1": "/COMMUNICATION/CAN_H", "2": "/COMMUNICATION/CAN_L", "3": "GND"}
)

# Build J9
fp_j9 = build_fp(
    mod3_lines, "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal",
    "J9", "Conn_01x03_MountingPin", 90.5, 119.5, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/c41a4043-0de8-4c55-a88b-648ceae017c3/8ba114b8-86cd-4514-8dd7-644af4102cf4",
    "/COMMUNICATION/", "communication.kicad_sch",
    "8ba114b8-86cd-4514-8dd7-644af4102cf4",
    {"1": "/COMMUNICATION/CAN_H", "2": "/COMMUNICATION/CAN_L", "3": "GND"}
)

# Build J10
fp_j10 = build_fp(
    mod5_lines, "Connector_JST:JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal",
    "J10", "SWD", 112.5, 119.5, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/6a6ae277-51ef-46ec-a09b-86576920fc4f/fdf38b01-c2ba-4054-8b77-5c33166b802e",
    "/MCU/", "MCU.kicad_sch",
    "443c9290-4a7d-44bc-87ca-ae2112af1efc",
    {"1": "+3V3", "2": "/MCU/SWDIO", "3": "/MCU/SWCLK", "4": "/MCU/NRST", "5": "GND"}
)

print("J8 build success, lines:", len(fp_j8.splitlines()))
print("J9 build success, lines:", len(fp_j9.splitlines()))
print("J10 build success, lines:", len(fp_j10.splitlines()))

# Now read scratch/pcb_step2.kicad_pcb and replace old footprints
with open("scratch/pcb_step2.kicad_pcb", "r", encoding="utf-8") as f:
    pcb = f.read()

# Replace J8 footprint
pat_j8 = r'\t\(footprint [^\n]*Molex_PicoBlade[^\n]*\n[\s\S]*?\(property "Reference" "J8"[\s\S]*?\n\t\)'
assert re.search(pat_j8, pcb), "Could not find J8"
pcb = re.sub(pat_j8, lambda m: fp_j8, pcb, count=1)
print("Replaced J8 in PCB")

# Replace J9 footprint
pat_j9 = r'\t\(footprint [^\n]*Molex_PicoBlade[^\n]*\n[\s\S]*?\(property "Reference" "J9"[\s\S]*?\n\t\)'
assert re.search(pat_j9, pcb), "Could not find J9"
pcb = re.sub(pat_j9, lambda m: fp_j9, pcb, count=1)
print("Replaced J9 in PCB")

# Replace J10 footprint
pat_j10 = r'\t\(footprint [^\n]*PinHeader_1x05[^\n]*\n[\s\S]*?\(property "Reference" "J10"[\s\S]*?\n\t\)'
assert re.search(pat_j10, pcb), "Could not find J10"
pcb = re.sub(pat_j10, lambda m: fp_j10, pcb, count=1)
print("Replaced J10 in PCB")

# Update J7 position to (101.5, 121.2, 0)
pat_j7_pos = r'(\(footprint [^\n]*USB_C_Receptacle[^\n]*\n[\s\S]*?\(at )[-0-9.]+ [-0-9.]+( [^)]+)?(\)[\s\S]*?\(property "Reference" "J7")'
m_j7 = re.search(pat_j7_pos, pcb)
assert m_j7, "Could not find J7 position"
pcb = pcb[:m_j7.start()] + m_j7.group(1) + "101.5 121.2 0" + m_j7.group(3) + pcb[m_j7.end():]
print("Updated J7 position to (101.5, 121.2, 0)")

# Update J11 (XT30PW-M) position to (122.0, 100.0, 90)
pat_j11_pos = r'(\(footprint [^\n]*XT30PW-M[^\n]*\n[\s\S]*?\(at )[-0-9.]+ [-0-9.]+( [^)]+)?(\)[\s\S]*?\(property "Reference" "J11")'
m_j11 = re.search(pat_j11_pos, pcb)
assert m_j11, "Could not find J11 position"
pcb = pcb[:m_j11.start()] + m_j11.group(1) + "122.0 100.0 90" + m_j11.group(3) + pcb[m_j11.end():]
print("Updated J11 position to (122.0, 100.0, 90)")

with open("scratch/pcb_step3.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(pcb)
print("Saved scratch/pcb_step3.kicad_pcb")
