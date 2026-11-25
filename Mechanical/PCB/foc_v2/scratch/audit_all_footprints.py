with open("scratch/foc_v2_orig.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Parse all footprint blocks
lines = text.splitlines()
in_fp = False
curr_ref = ""
curr_fp = ""
fp_lines = []
all_fps = {}

for l in lines:
    if l.startswith("\t(footprint ") or l.startswith("(footprint "):
        in_fp = True
        curr_fp = l.split('"')[1]
        curr_ref = ""
        fp_lines = [l]
    elif in_fp:
        fp_lines.append(l)
        if '(property "Reference" ' in l:
            curr_ref = l.split('"')[3]
        elif l.startswith("\t)") or l.startswith(")"):
            # Compute courtyard / size of this footprint from fp_line / fp_rect / pad
            pts_x = []
            pts_y = []
            for fl in fp_lines:
                # find (at x y)
                m_at = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)', fl)
                # find (start x y) (end x y)
                m_se = re.search(r'\(start\s+([0-9.-]+)\s+([0-9.-]+)\)\s+\(end\s+([0-9.-]+)\s+([0-9.-]+)\)', fl)
                if m_se:
                    pts_x.extend([float(m_se.group(1)), float(m_se.group(3))])
                    pts_y.extend([float(m_se.group(2)), float(m_se.group(4))])
                elif m_at and not fl.startswith("\t(footprint") and not fl.startswith("\t\t(property"):
                    pts_x.append(float(m_at.group(1)))
                    pts_y.append(float(m_at.group(2)))
            
            if pts_x and pts_y:
                min_x, max_x = min(pts_x), max(pts_x)
                min_y, max_y = min(pts_y), max(pts_y)
                w = max_x - min_x
                h = max_y - min_y
            else:
                w, h = 2.0, 2.0
            
            all_fps[curr_ref] = {
                "fp": curr_fp,
                "width": max(w, 1.5),
                "height": max(h, 1.5)
            }
            in_fp = False

print(f"Audited {len(all_fps)} footprints.")
for ref in sorted(all_fps.keys()):
    info = all_fps[ref]
    print(f"{ref:8s}: {info['width']:5.2f} x {info['height']:5.2f} mm - {info['fp']}")
