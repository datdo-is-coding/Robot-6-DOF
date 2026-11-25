with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_ref = None
for l in lines:
    if 'property "Reference"' in l:
        current_ref = l.split('"')[3]
    if current_ref in ['R37', 'R38', 'R39', 'C54', 'C55', 'C56', 'D1', 'D2', 'D3', 'R33', 'R35', 'R36', 'U8', 'Q7']:
        if '(pad ' in l:
            p_num = l.split('"')[1]
            # find net
            net = ''
            if '(net ' in l:
                net = l.split('(net ')[1].split(')')[0].replace('"', '').strip()
            print(f"{current_ref} pad {p_num}: {net}")
