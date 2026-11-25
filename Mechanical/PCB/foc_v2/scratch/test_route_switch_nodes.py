import re
import uuid
import subprocess

# Let's inspect the exact coordinates of pads for Phase U, V, W
# Phase U:
# Q1: fp (80.0, 77.5) rot 180.
#   Pad 1: rel(-2.9, -1.905) -> (82.90, 79.405)
#   Pad 2: rel(-2.9, -0.635) -> (82.90, 78.135)
#   Pad 3: rel(-2.9, 0.635)  -> (82.90, 76.865)
#   Pad 4: rel(-2.9, 1.905)  -> (82.90, 75.595) [Gate]
#   Pad 5: rel(1.05, 0)      -> (78.95, 77.50)  [Drain = VS]
# Q2: fp (87.5, 77.5) rot 180.
#   Pad 1: rel(-2.9, -1.905) -> (90.40, 79.405) [SPA]
#   Pad 2: rel(-2.9, -0.635) -> (90.40, 78.135) [SPA]
#   Pad 3: rel(-2.9, 0.635)  -> (90.40, 76.865) [SPA]
#   Pad 4: rel(-2.9, 1.905)  -> (90.40, 75.595) [Gate]
#   Pad 5: rel(1.05, 0)      -> (86.45, 77.50)  [Drain = SHA]
# J1: fp (84.5, 71.6) -> Pad 1 at (84.5, 71.6) [SHA]

# Let's check clearance:
# Q1 pads 1..3 (x=82.90, y=76.865..79.405) to Q2 pad 5 (x=86.45, y=77.50)
# A bus bar connecting Q1 pads 1..3: vertical track at x=82.90 from y=76.865 to 79.405, width 0.6 mm
# Connect from (82.90, 77.50) to Q2 pad 5 at (86.45, 77.50), width 1.5 mm!
# And connect from (84.50, 77.50) to J1 at (84.50, 71.60), width 1.5 mm!

print("Calculated Switch Node U coordinates successfully.")
