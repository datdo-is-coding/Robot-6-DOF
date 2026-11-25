import uuid

def generate_xh_s3b(ref, val, pos_x, pos_y, rot, path, sheetname, sheetfile, fp_uuid, pad_nets):
    p3 = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod"
    with open(p3, "r", encoding="utf-8") as f:
        mod = f.read()

    # mod lines
    lines = mod.splitlines()
    # Replace header: (footprint "JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"
    out = [
        f'\t(footprint "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"',
        f'\t\t(layer "F.Cu")',
        f'\t\t(uuid "{fp_uuid}")',
        f'\t\t(at {pos_x} {pos_y} {rot})',
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
        f'\t\t(property "Footprint" "Connector_JST:JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal"',
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

    # Now add lines from mod (skipping first line and closing line)
    in_pad = None
    for line in lines[1:-1]:
        stripped = line.strip()
        if stripped.startswith('(property "Reference"') or stripped.startswith('(property "Value"') or stripped.startswith('(property "Footprint"'):
            continue # already added
        if stripped.startswith('(pad "'):
            pad_num = stripped.split('"')[1]
            in_pad = pad_num
            out.append(f'\t\t{stripped}')
            continue
        if in_pad:
            if stripped.startswith('(uuid '):
                # insert net before uuid
                if in_pad in pad_nets:
                    out.append(f'\t\t\t(net "{pad_nets[in_pad]}")')
                out.append(f'\t\t{stripped}')
                in_pad = None
                continue
        out.append(f'\t\t{stripped}')

    out.append('\t)')
    return "\n".join(out)

# Test generation
test_out = generate_xh_s3b(
    "J8", "Conn_01x03_MountingPin", 79.5, 119.5, 0,
    "/b5c0d4be-7ad7-4dae-8125-334a612efd8d/c41a4043-0de8-4c55-a88b-648ceae017c3/76631f46-810c-4f88-99e6-e9e6bbe901b0",
    "/COMMUNICATION/", "communication.kicad_sch", "test-uuid-1234",
    {"1": "/COMMUNICATION/CAN_H", "2": "/COMMUNICATION/CAN_L", "3": "GND"}
)
print("Generated J8 length:", len(test_out))
print("Contains CAN_H:", "CAN_H" in test_out)
