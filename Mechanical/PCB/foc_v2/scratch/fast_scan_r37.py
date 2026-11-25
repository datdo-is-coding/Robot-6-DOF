with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_fp = None
current_ref = None
pads = {}

for line in lines:
    line = line.strip()
    if line.startswith('(footprint '):
        current_fp = line
        current_ref = None
        pads = {}
    elif 'property "Reference"' in line:
        parts = line.split('"')
        if len(parts) >= 4:
            current_ref = parts[3]
    elif line.startswith('(pad ') and current_ref in ['R37', 'R38', 'R39', 'U8', 'Q7', 'D1', 'D2', 'D3', 'R33', 'R35', 'R36', 'J8']:
        parts = line.split('"')
        pad_num = parts[1] if len(parts) > 1 else '?'
        net_name = ''
        if '(net ' in line:
            net_idx = line.find('(net ')
            net_parts = line[net_idx:].split('"')
            if len(net_parts) >= 2:
                net_name = net_parts[1]
        pads[pad_num] = net_name
    elif line.startswith(')') and current_ref in ['R37', 'R38', 'R39', 'U8', 'Q7', 'D1', 'D2', 'D3', 'R33', 'R35', 'R36', 'J8']:
        print(f"{current_ref}: {pads}")
        current_ref = None
