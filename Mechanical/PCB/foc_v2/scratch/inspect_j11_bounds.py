import re
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')
for r in ['J11', 'L1', 'D4', 'C16', 'C17', 'U10', 'C6', 'C7', 'C56', 'C57', 'C58', 'R53', 'R54', 'R59', 'R60']:
    lines = fps[r]
    for l in lines:
        if l.strip().startswith('(at '):
            m = re.search(r'\(at\s+([-0-9.]+)\s+([-0-9.]+)(?:\s+([-0-9.]+))?\)', l)
            if m:
                x = float(m.group(1))
                y = float(m.group(2))
                rot = float(m.group(3)) if m.group(3) else 0.0
                break
    is_b, shapes = parse_shapes(lines)
    box = get_world_bbox(r, is_b, shapes, x, y, rot)
    print(f"{r:6s}: at=({x:.1f}, {y:.1f}, {rot:.0f}) -> X=[{box['x1']:.2f}, {box['x2']:.2f}], Y=[{box['y1']:.2f}, {box['y2']:.2f}]")
