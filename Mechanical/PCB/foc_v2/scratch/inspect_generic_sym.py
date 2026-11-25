p = r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Connector_Generic.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(symbol "Conn_01x03"')
if idx != -1:
    print(text[idx:idx+2500])
