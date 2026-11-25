with open("scratch/foc_v2_orig.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

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
            pts_x = []
            pts_y = []
            for fl in fp_lines[1:]:
                # find (at x y ...) of pads or lines
                if fl.strip().startswith("(pad ") or fl.strip().startswith("(fp_"):
                    m_se = re.search(r'\(start\s+([0-9.-]+)\s+([0-9.-]+)\)\s+\(end\s+([0-9.-]+)\s+([0-9.-]+)\)', fl)
                    if m_se:
                        pts_x.extend([float(m_se.group(1)), float(m_se.group(3))])
                        pts_y.extend([float(m_se.group(2)), float(m_se.group(4))])
                    m_at = re.search(r'\(at\s+([0-9.-]+)\s+([0-9.-]+)', fl)
                    if m_at:
                        pts_x.append(float(m_at.group(1)))
                        pts_y.append(float(m_at.group(2)))
            
            if pts_x and pts_y:
                w = max(pts_x) - min(pts_x)
                h = max(pts_y) - min(pts_y)
            else:
                w, h = 1.0, 1.0
            all_fps[curr_ref] = (curr_fp, max(w, 0.5), max(h, 0.5))
            in_fp = False

# Print footprint dimensions grouped by footprint type
by_fp = {}
for ref, (fp, w, h) in all_fps.items():
    if fp not in by_fp:
        by_fp[fp] = (w, h, [])
    by_fp[fp][2].append(ref)

print(f"Unique footprints: {len(by_fp)}")
for fp, (w, h, refs) in sorted(by_fp.items()):
    print(f"{fp:70s} {w:5.2f} x {h:5.2f} mm : {len(refs)} components ({', '.join(refs[:5])}...)")
