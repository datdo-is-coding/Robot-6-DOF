import math

# Let's test connector placement along X when front face is at Y = 124.2:
# Flat cut at Y = 124.5 mm (from 75.0 to 125.0)
# Connectors:
# J7: y_orig = 124.2 - 3.79 = 120.41. Width: [-4.47, 4.47] (crtyd [-5.32, 5.32])
# J8: y_orig = 124.2 - 9.20 = 115.00. Width: [-2.45, 7.45] (crtyd [-2.95, 7.95])
# J9: y_orig = 124.2 - 9.20 = 115.00. Width: [-2.45, 7.45] (crtyd [-2.95, 7.95])
# J10: y_orig = 124.2 - 9.20 = 115.00. Width: [-2.45, 12.45] (crtyd [-2.95, 12.95])

# Mounting holes:
# H2 = (84.444, 115.556), H1 = (115.556, 115.556)
# Note: At y_orig = 115.00, pads are at Y = 115.00.
# |115.00 - 115.556| = 0.556 mm.
# Pad radius ~ 0.85 mm. Hole radius = 1.35 mm.
# Clearance required = 0.2 mm.
# So dist >= 2.40 mm.
# dx >= sqrt(2.40^2 - 0.556^2) = sqrt(5.76 - 0.31) = 2.33 mm.
# So pads cannot be within 2.33 mm in X of 84.444 or 115.556.
# That means no pad at X in [82.11 .. 86.77] or [113.23 .. 117.89].

# Now: Where were J8, J9, J7, J10 placed previously?
# J8: at X = 74.5 -> pads at 74.5, 77.0, 79.5.
#     79.5 is 4.94 mm away from 84.444! (CLEAN! > 2.33 mm!)
# J9: at X = 86.0 -> pads at 86.0, 88.5, 91.0.
#     86.0 is only 1.56 mm from 84.444! (COLLISION with H2!)
#     If J9 is moved to X = 87.5:
#     pads at 87.5, 90.0, 92.5.
#     87.5 - 84.444 = 3.06 mm > 2.33 mm! (CLEAN!)
# J7: at X = 100.0 -> pads in [95.68, 104.32]. (CLEAN!)
# J10: at X = 109.5 -> pads at 109.5, 112.0, 114.5, 117.0, 119.5.
#     Wait! J10 pad 3 is at 114.5, pad 4 is at 117.0!
#     H1 is at 115.556!
#     So J10 pad 3 and pad 4 sit right on top of H1!
#     THAT'S WHY J10 COLLIDED WITH H1!

print("Analysis complete.")
