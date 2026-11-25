with open(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_USB.pretty\USB_C_Receptacle_HRO_TYPE-C-31-M-12.kicad_mod", 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'F.CrtYd' in l:
        for j in range(max(0, i-15), min(len(lines), i+5)):
            print(lines[j].rstrip())
