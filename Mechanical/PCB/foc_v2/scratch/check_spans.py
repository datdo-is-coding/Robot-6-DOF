# We have 4 connectors:
# J8 (w=9.9)
# J9 (w=9.9)
# J7 (w=8.94)
# J10 (w=14.9)

# We have available X spans on the board:
# Left span: [76.35, 81.44] -> width = 81.44 - 76.35 = 5.09 mm!
# Center span: [87.44, 112.56] -> width = 112.56 - 87.44 = 25.12 mm!
# Right span: [118.56, 123.65] -> width = 123.65 - 118.56 = 5.09 mm!

# Look at the widths:
# The left span is ONLY 5.09 mm wide!
# The right span is ONLY 5.09 mm wide!
# The center span is 25.12 mm wide!
# Total available width outside keepouts = 5.09 + 25.12 + 5.09 = 35.30 mm!
# But total connector width is 43.64 mm!
# 43.64 > 35.30 mm!
print("Left span width:", 81.44 - 76.35)
print("Center span width:", 112.56 - 87.44)
print("Right span width:", 123.65 - 118.56)
print("Can 4 connectors fit strictly outside the X-intervals of H2 and H1 at that Y?")
print("NO, because the smallest connector is 8.94 mm wide, but Left and Right spans are only 5.09 mm wide!")
