with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines[:200]):
    if 'symbol "Connector' in l or 'symbol "Conn_' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+30)):
            if "(pin " in lines[j]:
                print(f"  {lines[j].strip()}")
