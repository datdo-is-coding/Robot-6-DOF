import math, re

with open('foc_v2.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

def parse_footprints():
    pos = 0
    fps = {}
    while True:
        idx = text.find('(footprint ', pos)
        if idx == -1: break
        depth = 0
        end = idx
        for i in range(idx, len(text)):
            if text[i] == '(': depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        fp_text = text[idx:end]
        m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
        if m_ref:
            ref = m_ref.group(1)
            # find all CrtYd items (fp_line, fp_rect, fp_circle)
            lines = []
            for m in re.finditer(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\).*?\(layer\s+"[FB]\.CrtYd"\)', fp_text, re.DOTALL):
                lines.append((float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))
            rects = []
            for m in re.finditer(r'\(fp_rect\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\).*?\(layer\s+"[FB]\.CrtYd"\)', fp_text, re.DOTALL):
                rects.append((float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))
            circles = []
            for m in re.finditer(r'\(fp_circle\s+\(center\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\).*?\(layer\s+"[FB]\.CrtYd"\)', fp_text, re.DOTALL):
                cx, cy, ex, ey = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
                r = math.sqrt((ex-cx)**2 + (ey-cy)**2)
                circles.append((cx, cy, r))
            
            # extract local bounding box
            xs, ys = [], []
            for x1, y1, x2, y2 in lines + rects:
                xs.extend([x1, x2])
                ys.extend([y1, y2])
            for cx, cy, r in circles:
                xs.extend([cx - r, cx + r])
                ys.extend([cy - r, cy + r])
            
            # fallback to pads if no courtyard
            if not xs:
                for m in re.finditer(r'\(pad\s+"[^"]*"\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)\s+\(size\s+([-\d.]+)\s+([-\d.]+)\)', fp_text):
                    px, py, sx, sy = float(m.group(1)), float(m.group(2)), float(m.group(4)), float(m.group(5))
                    xs.extend([px - sx/2 - 0.25, px + sx/2 + 0.25])
                    ys.extend([py - sy/2 - 0.25, py + sy/2 + 0.25])
            
            if xs and ys:
                fps[ref] = (min(xs), max(xs), min(ys), max(ys))
            else:
                fps[ref] = (-1, 1, -1, 1)
        pos = end
    return fps

local_boxes = parse_footprints()
print(f"Parsed {len(local_boxes)} footprints:")
for ref in ['J7', 'J8', 'J9', 'J10', 'J11', 'J1', 'J2', 'J3', 'H1', 'H2', 'H3', 'H4', 'U1', 'IC1', 'Q1']:
    b = local_boxes.get(ref)
    if b:
        w = b[1] - b[0]
        h = b[3] - b[2]
        print(f"  {ref:8s}: X [{b[0]:6.2f}, {b[1]:6.2f}] (w={w:5.2f}), Y [{b[2]:6.2f}, {b[3]:6.2f}] (h={h:5.2f})")
