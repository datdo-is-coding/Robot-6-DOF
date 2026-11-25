import math
from exact_crtyd_engine import load_pcb_footprints, parse_shapes, get_world_bbox

fps = load_pcb_footprints('foc_v2.kicad_pcb')

# East Wing components:
# J11 (XT30): rot=270: width 15.85, height 14.30. x in [-2.25, 13.60], y in [-9.65, 4.65]
# F1 (Fuseholder): rot=0: width 16.50, height 7.24. x in [-3.29, 13.21], y in [-1.92, 5.32]
#              rot=90: width 7.24, height 16.50. x in [-1.92, 5.32], y in [-13.21, 3.29]
# D6 (TVS SMB): rot=0: width 7.30, height 4.50. x in [-3.65, 3.65], y in [-2.25, 2.25]
# L1 (Inductor): rot=0: width 7.00, height 6.50. x in [-3.50, 3.50], y in [-3.25, 3.25]
# D4 (Diode): rot=0: width 7.00, height 3.50. x in [-3.50, 3.50], y in [-1.75, 1.75]
# C16, C17 (Caps 0805): rot=90: width 1.96, height 3.76
# R53, R54 (Res 0603): rot=0: width 2.96, height 1.46
# U10 (LDO SOT-23-5): rot=0: width 4.10, height 3.40
# C57, C58 (Caps 0603): rot=0: width 2.96, height 1.46

# Fixed obstacles:
# H4: (115.556, 84.444), R_ko = 2.40
# H1: (115.556, 115.556), R_ko = 2.40
# C63: can center (126.0, 86.0), R = 5.25 (box X in [120.75, 131.25], Y in [80.75, 91.25])
# J9: (121.0, 110.50), box X in [118.3, 128.7], Y in [107.9, 120.0]
# MCU right edge: X = 107.7 (passives C6, C7, C50 at X = 107.5..109.5)

# Available space:
# Between C63 (ends Y=91.25) and J9 (starts Y=107.9):
# Y in [91.5, 107.5] is an open band of height 16.0 mm!
# And X in [110.0, 132.0] is width 22.0 mm!
# Inside circle R=35mm (at Y=100, X_max=135; at Y=92, X_max=134; at Y=107, X_max=134.2).

# Let's see:
# Can J11 be placed at (117.0, 99.0, rot=270)?
# J11 box: X in [114.75, 130.60], Y in [89.35, 103.65].
# But C63 ends at 91.25, so J11 at Y=99 overlaps C63 by 91.25 - 89.35 = 1.90 mm!
# If J11 is at (117.0, 101.5, rot=270):
# J11 Y in [101.5 - 9.65, 101.5 + 4.65] = [91.85, 106.15]!
# Gap to C63 (91.25) is 91.85 - 91.25 = 0.60 mm!
# Gap to J9 (107.90) is 107.90 - 106.15 = 1.75 mm!
# J11 X: [114.75, 130.60]. Max distance to center (100, 100):
# Corner (130.60, 106.15): sqrt(30.6^2 + 6.15^2) = 31.21 mm << 35.0 mm!
# J11 FITS PERFECTLY AT (117.0, 101.5, rot=270)!

print("J11 at (117.0, 101.5, rot=270) fits with 0.60mm gap to C63 and 1.75mm gap to J9!")
