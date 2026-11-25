import math

# Let's design the exact closed Edge.Cuts loop:
# Coordinates:
# 1. North Arc (circle R=35.0, center 100, 100):
#    From West top (66.5, 89.8634) over the top (100.0, 65.0) to East top (133.5, 89.8634)
#    In KiCad 10, gr_arc syntax is:
#    (gr_arc (start X1 Y1) (mid Xm Ym) (end X2 Y2) (stroke (width 0.05) (type default)) (layer "Edge.Cuts") (uuid "..."))
#    Arc 1 (NW to N): start (66.5, 89.8634) -> mid (78.36, 72.48) -> end (100.0, 65.0)
#    Arc 2 (N to NE): start (100.0, 65.0) -> mid (121.64, 72.48) -> end (133.5, 89.8634)

# 2. East Flat Line (at x = 135.0 or 134.5):
#    Line from (133.5, 89.8634) to (134.5, 92.0)
#    Line from (134.5, 92.0) to (134.5, 110.0) [East flat face for XT30]
#    Line from (134.5, 110.0) to (122.5, 132.5) [SE transition]

# 3. South Flat Line (at y = 132.5):
#    Line from (122.5, 132.5) to (82.5, 132.5) [South flat face for J8, J9, J7]

# 4. SW transition:
#    Line from (82.5, 132.5) to (66.5, 110.0)

# 5. West Flat Line (at x = 66.5):
#    Line from (66.5, 110.0) to (66.5, 89.8634) [West flat face for J10]

# Let's verify every start/end matches perfectly:
segments = [
    ("arc", (66.5, 89.8634), (79.25, 72.75), (100.0, 65.0)),
    ("arc", (100.0, 65.0), (120.75, 72.75), (133.5, 89.8634)),
    ("line", (133.5, 89.8634), (134.5, 92.0)),
    ("line", (134.5, 92.0), (134.5, 110.0)),
    ("line", (134.5, 110.0), (122.5, 132.5)),
    ("line", (122.5, 132.5), (82.5, 132.5)),
    ("line", (82.5, 132.5), (66.5, 110.0)),
    ("line", (66.5, 110.0), (66.5, 89.8634)),
]

print("Loop continuity check:")
for i in range(len(segments)):
    prev_seg = segments[i - 1]
    curr_seg = segments[i]
    prev_end = prev_seg[3] if prev_seg[0] == "arc" else prev_seg[2]
    curr_start = curr_seg[1]
    dist = math.hypot(prev_end[0] - curr_start[0], prev_end[1] - curr_start[1])
    assert dist < 1e-4, f"Gap between {prev_seg[0]} and {curr_seg[0]}: dist={dist}"
    print(f"Segment {i}: {curr_seg[0]} from {curr_start} to {curr_seg[-1]} - OK")

print("Continuity: 100% Watertight Closed Loop!")
