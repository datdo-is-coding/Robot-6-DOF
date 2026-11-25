import re, math

def load_pcb_footprints(pcb_path):
    with open(pcb_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    footprints = {}
    in_fp = False
    curr_lines = []
    curr_ref = None
    
    for l in lines:
        if l.startswith('\t(footprint ') or l.startswith('(footprint '):
            in_fp = True
            curr_lines = [l]
            curr_ref = None
        elif in_fp:
            curr_lines.append(l)
            if '(property "Reference" "' in l:
                curr_ref = l.split('"')[3]
            elif l.startswith('\t)') or l.startswith(')'):
                if curr_ref:
                    footprints[curr_ref] = curr_lines
                in_fp = False
    return footprints

def parse_shapes(fp_lines):
    shapes = []
    layer_cu = 'F.Cu'
    for l in fp_lines:
        if '(layer "' in l:
            m = re.search(r'\(layer "([^"]+)"\)', l)
            if m:
                layer_cu = m.group(1)
                break
            
    is_bottom = 'B.Cu' in layer_cu
    
    i = 0
    while i < len(fp_lines):
        l = fp_lines[i]
        if '(layer "F.CrtYd")' in l or '(layer "B.CrtYd")' in l:
            start_k = i
            while start_k > 0 and not fp_lines[start_k].strip().startswith('(fp_'):
                start_k -= 1
            end_k = i
            while end_k < len(fp_lines) - 1 and not fp_lines[end_k].strip().startswith(')'):
                end_k += 1
            block = "".join(fp_lines[start_k:end_k+1])
            
            # Circle
            m_circ = re.search(r'\(fp_circle\s+\(center\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\)', block)
            if m_circ:
                cx, cy = float(m_circ.group(1)), float(m_circ.group(2))
                ex, ey = float(m_circ.group(3)), float(m_circ.group(4))
                r = math.hypot(ex - cx, ey - cy)
                shapes.append(('circle', cx, cy, r))
                i = end_k + 1
                continue
                
            # Rect
            m_rect = re.search(r'\(fp_rect\s+\(start\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\)', block)
            if m_rect:
                x1, y1 = float(m_rect.group(1)), float(m_rect.group(2))
                x2, y2 = float(m_rect.group(3)), float(m_rect.group(4))
                shapes.append(('rect', min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
                i = end_k + 1
                continue
                
            # Line
            m_line = re.search(r'\(fp_line\s+\(start\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\)', block)
            if m_line:
                x1, y1 = float(m_line.group(1)), float(m_line.group(2))
                x2, y2 = float(m_line.group(3)), float(m_line.group(4))
                shapes.append(('line', x1, y1, x2, y2))
                i = end_k + 1
                continue
                
            # Poly
            m_poly = re.search(r'\(fp_poly\s+\(pts(.*?)\)', block, re.DOTALL)
            if m_poly:
                pts = re.findall(r'\(xy\s+([-0-9.]+)\s+([-0-9.]+)\)', m_poly.group(1))
                poly_pts = [(float(px), float(py)) for px, py in pts]
                shapes.append(('poly', poly_pts))
                i = end_k + 1
                continue
        i += 1
        
    return is_bottom, shapes

def kicad_transform(x0, y0, rot_deg, lx, ly, is_bottom=False):
    if is_bottom:
        lx = -lx
    rad = math.radians(rot_deg)
    return (
        x0 + lx * math.cos(rad) + ly * math.sin(rad),
        y0 - lx * math.sin(rad) + ly * math.cos(rad)
    )

def get_world_bbox(ref, is_bottom, shapes, x, y, rot_deg):
    all_pts = []
    for s in shapes:
        stype = s[0]
        if stype == 'circle':
            cx, cy, r = s[1], s[2], s[3]
            for k in range(8):
                ang = k * math.pi / 4
                px = cx + r * math.cos(ang)
                py = cy + r * math.sin(ang)
                all_pts.append(kicad_transform(x, y, rot_deg, px, py, is_bottom))
        elif stype == 'rect':
            x1, y1, x2, y2 = s[1], s[2], s[3], s[4]
            all_pts.append(kicad_transform(x, y, rot_deg, x1, y1, is_bottom))
            all_pts.append(kicad_transform(x, y, rot_deg, x1, y2, is_bottom))
            all_pts.append(kicad_transform(x, y, rot_deg, x2, y1, is_bottom))
            all_pts.append(kicad_transform(x, y, rot_deg, x2, y2, is_bottom))
        elif stype == 'line':
            all_pts.append(kicad_transform(x, y, rot_deg, s[1], s[2], is_bottom))
            all_pts.append(kicad_transform(x, y, rot_deg, s[3], s[4], is_bottom))
        elif stype == 'poly':
            for px, py in s[1]:
                all_pts.append(kicad_transform(x, y, rot_deg, px, py, is_bottom))
                
    if not all_pts:
        all_pts = [kicad_transform(x, y, rot_deg, -0.5, -0.5, is_bottom),
                   kicad_transform(x, y, rot_deg, 0.5, 0.5, is_bottom)]
        
    min_x = min(p[0] for p in all_pts)
    max_x = max(p[0] for p in all_pts)
    min_y = min(p[1] for p in all_pts)
    max_y = max(p[1] for p in all_pts)
    
    return {
        'ref': ref,
        'layer': 'bottom' if is_bottom else 'top',
        'x1': min_x, 'x2': max_x,
        'y1': min_y, 'y2': max_y,
        'cx': (min_x + max_x) / 2,
        'cy': (min_y + max_y) / 2,
        'w': max_x - min_x,
        'h': max_y - min_y
    }
