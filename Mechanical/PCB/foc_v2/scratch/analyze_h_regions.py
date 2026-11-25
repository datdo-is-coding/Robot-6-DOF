import math

# Let's test if we can arrange J8, J9, J7, J10 to completely avoid H2 (84.44, 115.56) and H1 (115.56, 115.56)
# Connectors:
# J8: 3-pin XH, pads at x, x+2.5, x+5.0. Body [x-2.5, x+7.5]
# J9: 3-pin XH, pads at x, x+2.5, x+5.0. Body [x-2.5, x+7.5]
# J7: USB-C, pads [x-4.3, x+4.3], body [x-4.5, x+4.5], depth [-3.7, +3.8]
# J10: 5-pin XH, pads at x, x+2.5, x+5.0, x+7.5, x+10.0. Body [x-2.5, x+12.5]

# Let's check what X coordinates are available:
# H2 is at 84.44. Keepout is radius 3.0 => [81.44, 87.44]
# H1 is at 115.56. Keepout is radius 3.0 => [112.56, 118.56]

# Look at the regions:
# Region Left: X < 81.44
# Region Center: 87.44 < X < 112.56 (width = 25.12 mm)
# Region Right: X > 118.56

print("Region Center width:", 112.56 - 87.44)
