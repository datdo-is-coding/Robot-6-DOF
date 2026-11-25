from inspect_j8_detail import get_fp

fp_j7 = get_fp('J7')
print("=== J7 Footprint Full ===")
for l in fp_j7.splitlines():
    if 'fp_line' in l or 'fp_rect' in l or 'pad' in l:
        print(l)
