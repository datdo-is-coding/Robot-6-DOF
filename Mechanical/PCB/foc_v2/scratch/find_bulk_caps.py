import math

H4 = (115.55635, 84.44365)
H3 = (84.44365, 84.44365)

# For C63 (D=10.5mm, R=5.25mm):
print("Searching for C63 positions...")
for x in range(116, 126):
    for y in range(75, 95):
        cx, cy = float(x), float(y)
        # distance to board center + 5.25 <= 35.0
        d_board = math.hypot(cx - 100, cy - 100) + 5.25
        if d_board > 35.0:
            continue
        # distance to H4 >= 3.0 + 5.25 = 8.25
        d_h4 = math.hypot(cx - H4[0], cy - H4[1])
        if d_h4 < 8.25:
            continue
        print(f"  Valid C63 at ({cx}, {cy}): board_d={d_board:.2f}, h4_d={d_h4:.2f}")

print("\nSearching for C_BULK1 positions...")
for x in range(70, 85):
    for y in range(75, 95):
        cx, cy = float(x), float(y)
        d_board = math.hypot(cx - 100, cy - 100) + 5.25
        if d_board > 35.0:
            continue
        d_h3 = math.hypot(cx - H3[0], cy - H3[1])
        if d_h3 < 8.25:
            continue
        print(f"  Valid C_BULK1 at ({cx}, {cy}): board_d={d_board:.2f}, h3_d={d_h3:.2f}")
