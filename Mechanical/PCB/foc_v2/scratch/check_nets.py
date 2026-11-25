with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if '(segment' in line:
            print(f"Segment at line {i+1}:")
            # print next 8 lines
            for _ in range(8):
                print(f.readline().rstrip())
            break
