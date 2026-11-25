with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'Edge.Cuts' in line:
            print(f"{i}: {line.strip()}")
