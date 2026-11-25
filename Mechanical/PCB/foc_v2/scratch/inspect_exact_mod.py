def parse_kicad_mod(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    import re
    pads = re.findall(r'\(pad\s+"([^"]+)"\s+(?:thru_hole|smd)\s+[^\(]*\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', text)
    print("File:", path)
    print("Pads:", pads)
    # Courtyard
    lines = text.splitlines()
    crtyd_x, crtyd_y = [], []
    for l in lines:
        if 'layer "F.CrtYd"' in l:
            # find starts and ends
            pts = re.findall(r'\((?:start|end|xy)\s+([0-9\.\-]+)\s+([0-9\.\-]+)\)', l)
            for x, y in pts:
                crtyd_x.append(float(x))
                crtyd_y.append(float(y))
    if crtyd_x:
        print(f"CrtYd X: [{min(crtyd_x):.2f}, {max(crtyd_x):.2f}] (width: {max(crtyd_x)-min(crtyd_x):.2f})")
        print(f"CrtYd Y: [{min(crtyd_y):.2f}, {max(crtyd_y):.2f}] (height: {max(crtyd_y)-min(crtyd_y):.2f})")

parse_kicad_mod(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S3B-XH-A_1x03_P2.50mm_Horizontal.kicad_mod")
parse_kicad_mod(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_JST.pretty\JST_XH_S5B-XH-A_1x05_P2.50mm_Horizontal.kicad_mod")
parse_kicad_mod(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_USB.pretty\USB_C_Receptacle_HRO_TYPE-C-31-M-12.kicad_mod")
