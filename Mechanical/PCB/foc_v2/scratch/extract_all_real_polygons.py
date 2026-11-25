import re, math

def parse_pcb_courtyards(pcb_path):
    with open(pcb_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_fp = False
    curr_ref = None
    curr_at = (0.0, 0.0, 0.0)
    curr_layer = "F.Cu"
    fp_elements = []
    footprints = {}

    for l in lines:
        if l.startswith('\t(footprint ') or l.startswith('(footprint '):
            in_fp = True
            curr_ref = None
            curr_at = (0.0, 0.0, 0.0)
            curr_layer = "F.Cu"
            fp_elements = []
        elif in_fp:
            if '(layer "' in l and curr_layer == "F.Cu":
                m = re.search(r'\(layer "([^"]+)"\)', l)
                if m: curr_layer = m.group(1)
            if '(at ' in l and curr_ref is None:
                # footprint at
                m = re.search(r'\(at\s+([-0-9.]+)\s+([-0-9.]+)(?:\s+([-0-9.]+))?\)', l)
                if m:
                    x = float(m.group(1))
                    y = float(m.group(2))
                    rot = float(m.group(3)) if m.group(3) else 0.0
                    curr_at = (x, y, rot)
            if '(property "Reference" "' in l:
                curr_ref = l.split('"')[3]
            fp_elements.append(l)
            if l.startswith('\t)') or l.startswith(')'):
                if curr_ref:
                    footprints[curr_ref] = {
                        'at': curr_at,
                        'layer': curr_layer,
                        'lines': fp_elements
                    }
                in_fp = False
    return footprints

def get_footprint_local_crtyd(fp_data):
    lines = fp_data['lines']
    pts = []
    i = 0
    while i < len(lines):
        l = lines[i]
        if '(layer "F.CrtYd")' in l or '(layer "B.CrtYd")' in l:
            # check previous lines in element
            block = []
            for k in range(max(0, i-6), min(len(lines), i+8)):
                block.append(lines[k])
            block_text = "".join(block)
            
            # fp_line
            m_line = re.search(r'\(fp_line\s+\(start\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\)', block_text)
            if m_line:
                pts.append((float(m_line.group(1)), float(m_line.group(2))))
                pts.append((float(m_line.group(3)), float(m_line.group(4))))
            
            # fp_rect
            m_rect = re.search(r'\(fp_rect\s+\(start\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\)', block_text)
            if m_rect:
                x1, y1 = float(m_rect.group(1)), float(m_rect.group(2))
                x2, y2 = float(m_rect.group(3)), float(m_rect.group(4))
                pts.extend([(x1, y1), (x1, y2), (x2, y1), (x2, y2)])
                
            # fp_circle
            m_circ = re.search(r'\(fp_circle\s+\(center\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\)', block_text)
            if m_circ:
                cx, cy = float(m_circ.group(1)), float(m_circ.group(2))
                ex, ey = float(m_circ.group(3)), float(m_circ.group(4))
                r = math.hypot(ex - cx, ey - cy)
                pts.extend([(cx - r, cy - r), (cx + r, cy + r)])
                
            # fp_poly pts
            m_poly = re.search(r'\(fp_poly\s+\(pts(.*?)\)', block_text, re.DOTALL)
            if m_poly:
                poly_pts = re.findall(r'\(xy\s+([-0-9.]+)\s+([-0-9.]+)\)', m_poly.group(1))
                for px, py in poly_pts:
                    pts.append((float(px), float(py)))
        i += 1
    
    if not pts:
        # Fallback: find pads
        for l in lines:
            if '(pad ' in l:
                m_pad = re.search(r'\(at\s+([-0-9.]+)\s+([-0-9.]+)', l)
                if m_pad:
                    px, py = float(m_pad.group(1)), float(m_pad.group(2))
                    pts.extend([(px - 1.0, py - 1.0), (px + 1.0, py + 1.0)])
    
    if not pts:
        pts = [(-0.5, -0.5), (0.5, 0.5)]
        
    return pts

fps = parse_pcb_courtyards('foc_v2.kicad_pcb')
print(f"Loaded {len(fps)} footprints.")

crtyd_boxes = {}
for ref, data in fps.items():
    pts = get_footprint_local_crtyd(data)
    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    max_y = max(p[1] for p in pts)
    crtyd_boxes[ref] = {
        'at': data['at'],
        'layer': 'B.Cu' if 'B.Cu' in data['layer'] or 'B.CrtYd' in "".join(data['lines']) else 'F.Cu',
        'local_bounds': (min_x, min_y, max_x, max_y)
    }

print("Sample exact footprints:")
for r in ['J11', 'Q1', 'H3', 'U1', 'J8', 'J10', 'C_BULK1']:
    b = crtyd_boxes[r]
    print(f"  {r:10s}: at={b['at']}, layer={b['layer']}, local_bounds={b['local_bounds']}")
