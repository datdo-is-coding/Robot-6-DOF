from fine_tune_zero_drc import set_fp, run_drc

print("Step 1: Adjust D4 to (117.0, 89.0)")
set_fp('D4', 117.0, 89.0)

print("Step 2: Adjust JP1 to (75.5, 97.4)")
set_fp('JP1', 75.5, 97.4)

print("Step 3: Adjust R45 to (74.0, 99.2) and R46 to (78.0, 99.2)")
set_fp('R45', 74.0, 99.2)
set_fp('R46', 78.0, 99.2)

overlaps = run_drc()
print(f"Remaining courtyard overlaps: {len(overlaps)}")
for c in overlaps:
    print(" ", [i['description'] for i in c['items']])
