import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's write an exact East Wing solver:
# Obstacles:
# H4: (115.556, 84.444), R_ko = 2.40
# H1: (115.556, 115.556), R_ko = 2.40
# C63: can center (126.0, 84.5), R = 5.25
# J9: (121.0, 110.30), box X in [118.3, 128.7], Y in [107.5, 120.0]
# IC1/MCU flank: X <= 111.0

# Available East Wing box:
# X in [112.0, 131.0], Y in [82.0, 107.0]
# Inside circle: (x-100)^2 + (y-100)^2 <= 34.8^2

# Let's test a clean, logical layout:
# 1. J11 (XT30): on outer perimeter at X = 120.0, Y = 98.0, rot = 270
# 2. F1 (Fuseholder):
# F1 at rot=0: width 16.50, height 7.24. X in [-3.29, 13.21], Y in [-1.92, 5.32]
# If F1 is at (114.5, 104.5, rot=0):
# X in [111.21, 127.71], Y in [102.58, 109.82]
# Gap to J9 (top at 107.5)? J9 is at Y=107.5..120.0. So F1 at Y=104.5 would overlap with J9!
# What if F1 is at rot=90 or rot=270 (vertical)?
# F1 at rot=270: width 7.24, height 16.50. X in [-5.32, 1.92], Y in [-3.29, 13.21]
# If F1 is at (114.5, 92.5, rot=270):
# X in [114.5 - 5.32, 114.5 + 1.92] = [109.18, 116.42] (too close to MCU flank!)
# What if F1 is at rot=90:
# X in [-1.92, 5.32], Y in [-13.21, 3.29]
# If F1 is at (122.5, 96.0, rot=90)?

def solve_east():
    # Let's define the components:
    # J11, F1, D6, L1, D4, C16, C17, R53, R54, U10, C57, C58
    pass
