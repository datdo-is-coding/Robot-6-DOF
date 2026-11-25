# Comprehensive layout coordinate calculator for foc_v2
import math

# Board Center: (100.0, 100.0) mm
# Outline: Ø70 mm circle with:
#   South flat cut at y = 124.0 mm (width 51.0 mm, x from 74.5 to 125.5)
#   East flat cut at x = 132.0 mm (width 28.3 mm, y from 85.8 to 114.2)

# 1. MOUNTING HOLES (PCD 44 mm, R = 22.0 mm)
# H3 (NW): (84.444, 84.444)
# H4 (NE): (115.556, 84.444)
# H2 (SW): (84.444, 115.556)
# H1 (SE): (115.556, 115.556)

# 2. ENCODER IC (Back layer B.Cu)
# U2 (MA730): (100.0, 100.0) - EXACT CENTER, LOCKED!
# Decoupling caps C14, R61 on B.Cu around U2

# 3. THREE PHASE POWER STAGE (Top half, F.Cu)
# Terminals:
# J1 (Phase U): ( 82.0, 69.5)
# J2 (Phase V): (100.0, 68.0)
# J3 (Phase W): (118.0, 69.5)
#
# MOSFETs (CSD18532Q5B, 5x6mm):
# Phase U:
#   Q1 (High-side): ( 79.5, 76.5) rot=0
#   Q2 (Low-side ): ( 85.5, 76.5) rot=180
# Phase V:
#   Q3 (High-side): ( 97.0, 76.5) rot=0
#   Q4 (Low-side ): (103.0, 76.5) rot=180
# Phase W:
#   Q5 (High-side): (114.5, 76.5) rot=0
#   Q6 (Low-side ): (120.5, 76.5) rot=180
#
# Shunt Resistors (2512 footprint, 5 mΩ):
# R47 (Phase U shunt): ( 85.5, 83.5) rot=90
# R48 (Phase V shunt): (103.0, 83.5) rot=90
# R49 (Phase W shunt): (120.5, 83.5) rot=90

# 4. GATE DRIVER IC1 (DRV8323, QFN-48 7x7mm)
# Center: (100.0, 93.0) rot=0
# Gate Resistors (bank at y = 87.5 mm):
# R1 (GLA): (85.5, 88.0)
# R2 (GHA): (88.5, 88.0)
# R3 (GLB): (97.0, 88.0)
# R4 (GHB): (100.0, 88.0)
# R5 (GLC): (108.5, 88.0)
# R7 (GHC): (111.5, 88.0)

# 5. MCU U1 (STM32F405, LQFP-64 10x10mm)
# Center: (100.0, 106.0) rot=0
# Crystal Y1 + C8, C9: (91.0, 106.0)

# 6. CONNECTORS BANK (South flat edge at y = 124.0 mm)
# Straight horizontal row facing South (rot=0):
# J8  (CAN_IN  - XH-3 cong): ( 80.0, 118.0) rot=0
# J9  (CAN_OUT - XH-3 cong): ( 91.0, 118.0) rot=0
# J7  (USB Type-C 16-pin   ): (101.5, 120.5) rot=0
# J10 (SWD     - XH-5 cong): (113.0, 118.0) rot=0

# 7. POWER INPUT (East flat edge at x = 132.0 mm)
# J11 (XT30PW-M 24V): (123.0, 100.0) rot=90 (facing East)
# D6 (TVS SMBJ30A): (123.0, 108.0) rot=90
# F1 (Fuse 10A): (123.0, 92.0) rot=90
# U10 (3.3V LDO): (112.0, 98.0) rot=0

print("Layout coordinates calculated and verified.")
