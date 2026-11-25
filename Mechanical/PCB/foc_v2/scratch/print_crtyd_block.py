with open(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod", 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'F.CrtYd' in l:
        for j in range(max(0, i-10), min(len(lines), i+10)):
            print(lines[j].rstrip())
