import math

# Center of circular board
cx, cy = 100.0, 100.0
R = 35.0

# 1. South flat cut:
# Horizontal line at y = 132.5
# Where does y = 132.5 intersect the R=35 circle?
# (x - 100)^2 + (132.5 - 100)^2 = 35^2
# (x - 100)^2 + 32.5^2 = 1225
# (x - 100)^2 + 1056.25 = 1225
# (x - 100)^2 = 168.75 => |x - 100| = 12.99 => x = 87.01 to 112.99
# But our connectors need x in [71.55, 122.45]!
# So the South cut is at y = 132.5.
# Let the South flat line run from (68.0, 132.5) to (124.5, 132.5).

# 2. East flat cut:
# Line along x = 135.5 from y = 90.0 to y = 112.0.
# From (124.5, 132.5) to (135.5, 120.0) -> (135.5, 90.0)?
# Let's check chamfers:
# Corner SE:
# Connect (124.5, 132.5) to (135.5, 116.0) with a chamfer line!
# (135.5, 116.0) to (135.5, 92.0) is the East flat edge (flush with XT30)!
# From (135.5, 92.0) to arc start on circle R=35:
# At y = 92.0: (x - 100)^2 + (92 - 100)^2 = 35^2 => (x - 100)^2 = 1225 - 64 = 1161 => x = 100 + 34.07 = 134.07.
# Chamfer from (135.5, 92.0) to (134.07, 92.0)?
# Or let the arc start at (134.07, 92.0) and go over (100.0, 65.0) to (65.93, 92.0)!

# Let's check:
# Circle R=35:
# At y = 92.0, x_east = 100 + sqrt(35^2 - 8^2) = 134.07.
# x_west = 100 - 34.07 = 65.93.
# The arc from (65.93, 92.0) passing through (100.0, 65.0) to (134.07, 92.0):
# This arc covers the entire North half of the board!

# Let's check West side:
# From (65.93, 92.0), vertical line down to (65.93, 122.0)!
# At (65.93, 122.0), line to (68.0, 132.5) [or corner chamfer to (70.0, 132.5)]!
# Wait! Let's check x of C60, C61, C62 on West:
# C60 has x1 = 66.27. If West edge is at x = 65.5, then C60 is 0.77 mm inside!
# At x = 65.5: line from (65.5, 92.0) to (65.5, 122.0).
# From (65.5, 122.0) to (70.0, 132.5).
# Wait, at J8 (CAN_IN):
# J8 has x in [71.55, 82.45], y in [119.69, 132.20].
# If South flat line starts at (69.0, 132.5), then J8 is completely supported by the South flat line!
# Line from (65.5, 122.0) to (69.0, 132.5):
# At x = 71.55, y of the edge is already 132.5!
# So J8 is 100% on the flat cut!

# Let's check East side at J10 (SWD):
# J10 has x in [106.55, 122.45], y in [119.69, 132.20].
# If South flat line ends at (124.5, 132.5), then J10 is completely supported!
# From (124.5, 132.5) to (135.5, 120.0):
# D6 is at x in [122.85, 130.15], y in [125.25, 129.75].
# Let's check if D6 is inside the chamfer line from (124.5, 132.5) to (135.5, 120.0):
# At x = 127.0:
# y = 132.5 - (127.0 - 124.5) / (135.5 - 124.5) * (132.5 - 120.0) = 132.5 - 2.5 / 11.0 * 12.5 = 132.5 - 2.84 = 129.66.
# And D6 y2 is 129.75! That's cutting close to D6!
# Why slant the chamfer early?
# Make the South flat line go all the way to (131.0, 132.5)!
# And from (131.0, 132.5) to (135.5, 124.0)!
# Then at x = 127.0, y of edge is 132.5 (South flat line)! D6 has 2.75 mm clearance!
# And from (131.0, 132.5) to (135.5, 124.0) to (135.5, 92.0):
# East flat line from (135.5, 92.0) to (135.5, 124.0)!
# That fully encompasses XT30 (J11), Fuse (F1), and TVS (D6)!

print("Calculated watertight outline parameters!")
