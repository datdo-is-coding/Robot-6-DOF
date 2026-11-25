import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Boundaries and obstacles on East:
# Circle: (100, 100), R = 35.0
# Y_cut: 120.0
# Obstacles:
# H4: (115.556, 84.444), R_ko = 2.40
# H1: (115.556, 115.556), R_ko = 2.40
# C63: can center (125.0, 85.0), R = 5.25
# J9: (121.0, 110.30, 0), box X in [118.3, 128.7], Y in [107.5, 120.0]
# IC1: (100.0, 89.0 or 93.5), right edge around X = 105.0 .. 106.0
# U1: (100.0, 102.0), right edge around X = 108.0

# Components to place:
# J11: XT30
# F1: Fuseholder
# D6: TVS
# L1: Inductor (7x6.5)
# D4: Diode (7x3.5)
# C16, C17: Caps
# R53, R54: Resistors
# U10: LDO (4.1x3.4)
# C57, C58: Caps

# Let's inspect J11 at rot=90, 180, 270:
for rot in [0, 90, 180, 270]:
    b = get_world_bbox('J11', False, parse_shapes(fps['J11'])[1], 0, 0, rot)
    print(f"J11 rot={rot}: X in [{b['x1']:.2f}, {b['x2']:.2f}], Y in [{b['y1']:.2f}, {b['y2']:.2f}]")

for rot in [0, 90, 180, 270]:
    b = get_world_bbox('F1', False, parse_shapes(fps['F1'])[1], 0, 0, rot)
    print(f"F1 rot={rot}: X in [{b['x1']:.2f}, {b['x2']:.2f}], Y in [{b['y1']:.2f}, {b['y2']:.2f}]")
