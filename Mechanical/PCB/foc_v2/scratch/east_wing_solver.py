import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# Let's fix all other components and only solve East Wing:
# East Wing items: J11, F1, D6, L1, D4, C16, C17, R53, R54, U10, C57, C58
# Surrounding constraints:
# H4 at (115.556, 84.444)
# H1 at (115.556, 115.556)
# J9 at (121.0, 110.69) -> X in [118.44, 128.56], Y in [108.28, 120.00]
# C63 cylinder at (124.5, 84.5), r = 5.25
# U1 at (100.0, 100.5) -> X in [93.3, 106.7], Y in [93.8, 107.2]
# IC1 at (100.0, 88.5) -> X in [95.87, 104.13], Y in [84.37, 92.63]
# DRV passives: C15, C18, C19, C20, C21, C64 at X = 106.0, Y in [85, 96]
# R55..R60, TP3 at X = 109.2, Y in [85, 98]

print("Ready to solve East Wing placement.")
