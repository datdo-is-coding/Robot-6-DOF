with open(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_AMASS.pretty\AMASS_XT30PW-M_1x02_P2.50mm_Horizontal.kicad_mod", 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'F.CrtYd' in l or 'pad ' in l:
        for j in range(max(0, i-4), min(len(lines), i+6)):
            print(lines[j].rstrip())
