import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox
from test_zero_exact import P, bboxes, HOLES, R_KO, ALLOWED

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# We need slots for:
# D1, D2, D3 (0603 size: 1.65 x 0.73)
# R33, R35, R36 (0402 size: 1.11 x 0.47)
# Buck passives: D4, C16, C17, R53, R54
# Let's find valid (x, y) positions for these components!

def is_point_free(x, y, w, h, layer='F.Cu', exclude_refs=()):
    hw = w / 2
    hh = h / 2
    bx1, bx2 = x - hw, x + hw
    by1, by2 = y - hh, y + hh
    
    # Check board boundary (within 35mm circle)
    for px, py in [(bx1, by1), (bx1, by2), (bx2, by1), (bx2, by2)]:
        d = math.hypot(px - 100.0, py - 100.0)
        if d > 33.5:
            # check if in flat cut
            if py > 132.5 or px < 66.5 or px > 135.0:
                return False
            if py > 120.0 and (px < 75.0 or px > 125.0):
                return False
                
    # Check holes
    for hname, (hx, hy) in HOLES.items():
        cx = max(bx1, min(hx, bx2))
        cy = max(by1, min(hy, by2))
        if math.hypot(cx - hx, cy - hy) < R_KO:
            return False
            
    # Check all existing bboxes
    for r, b in bboxes.items():
        if r in exclude_refs: continue
        if b['layer'] != ('bottom' if layer == 'B.Cu' else 'top'): continue
        if (bx1 < b['x2'] + 0.1 and bx2 > b['x1'] - 0.1 and
            by1 < b['y2'] + 0.1 and by2 > b['y1'] - 0.1):
            return False
    return True

print("Searching for LED bank slots (F.Cu)...")
led_slots = []
for y in [i * 0.5 for i in range(140, 260)]:
    for x in [j * 0.5 for j in range(140, 260)]:
        if is_point_free(x, y, 3.5, 1.8, 'F.Cu', exclude_refs=('D1', 'D2', 'D3', 'R33', 'R35', 'R36')):
            led_slots.append((x, y))

print(f"Found {len(led_slots)} free slots for LEDs on F.Cu!")
# Group by region
top = [p for p in led_slots if p[1] < 75]
print("Top slots (near North edge):", len(top), top[:6])
mid_right = [p for p in led_slots if p[0] > 115 and 75 < p[1] < 115]
print("Mid-right slots (East):", len(mid_right), mid_right[:6])
south = [p for p in led_slots if p[1] > 115]
print("South slots:", len(south), south[:6])
