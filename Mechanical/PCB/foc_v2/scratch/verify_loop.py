import math

segments = [
    ("line", (69.0, 132.5), (131.0, 132.5)),
    ("line", (131.0, 132.5), (135.5, 125.0)),
    ("line", (135.5, 125.0), (135.5, 92.0)),
    ("line", (135.5, 92.0), (134.0712, 92.0)),
    # Arc: start=(134.0712, 92.0), mid=(100.0, 65.0), end=(65.9288, 92.0)
    # Let's check R from center (100, 100):
    # (134.0712 - 100)^2 + (92.0 - 100)^2 = 34.0712^2 + 64 = 1160.85 + 64 = 1224.85 ~= 35^2 (1225)
    ("arc", (134.0712, 92.0), (100.0, 65.0), (65.9288, 92.0)),
    ("line", (65.9288, 92.0), (65.5, 92.0)),
    ("line", (65.5, 92.0), (65.5, 125.0)),
    ("line", (65.5, 125.0), (69.0, 132.5)),
]

print("Verifying watertight loop:")
for i in range(len(segments)):
    curr = segments[i]
    next_s = segments[(i + 1) % len(segments)]
    p_end = curr[3] if curr[0] == "arc" else curr[2]
    p_start = next_s[1]
    dist = math.hypot(p_end[0] - p_start[0], p_end[1] - p_start[1])
    print(f"Segment {i} end {p_end} -> Segment {(i+1)%len(segments)} start {p_start} : gap = {dist:.6f} mm")
    assert dist < 1e-4, f"Gap detected at segment {i}!"

print("Watertight verification PASSED 100%!")
