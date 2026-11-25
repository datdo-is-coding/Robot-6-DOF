import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('scratch/git_raw.kicad_pcb')

east_refs = ['J11', 'F1', 'D6', 'L1', 'D4', 'C16', 'C17', 'R53', 'R54', 'U10', 'C57', 'C58', 'C63', 'H4', 'H1', 'J9']

# Let's inspect where J9, H4, H1, C63 are fixed:
# H4: (115.556, 84.444)
# H1: (115.556, 115.556)
# C63: (122.5, 86.5, rot=0) -> can center (125.0, 86.5)
# J9: (121.0, 111.0, rot=0)

# Available space in East:
# Y in [92.0, 108.0], X in [112.0, 132.0]
# At Y=100.0, max circle X is 135.0 mm.
# At Y=92.0, dy = -8.0, max X = 100 + sqrt(35^2 - 64) = 100 + 34.07 = 134.07 mm.
# At Y=108.0, dy = +8.0, max X = 134.07 mm.

# Let's test a clean, non-overlapping placement of the 12 East components!
