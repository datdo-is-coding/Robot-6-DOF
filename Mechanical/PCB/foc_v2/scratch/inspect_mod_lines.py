with open(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod", 'r', encoding='utf-8') as f:
    for line in f:
        if 'CrtYd' in line or 'Fab' in line or 'SilkS' in line:
            print(line.rstrip())
