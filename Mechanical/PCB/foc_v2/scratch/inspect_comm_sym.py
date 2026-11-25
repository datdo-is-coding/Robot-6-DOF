with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
in_sym = False
for i, l in enumerate(lines):
    if '(symbol "Connector_Generic_MountingPin:Conn_01x03_MountingPin"' in l:
        in_sym = True
    if in_sym:
        print(l)
        if l.strip() == "))":
            break
