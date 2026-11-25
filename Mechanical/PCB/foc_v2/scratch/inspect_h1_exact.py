from inspect_j8_detail import get_fp

fp_h1 = get_fp('H1')
print("=== H1 Footprint ===")
for l in fp_h1.splitlines():
    if 'pad' in l or 'CrtYd' in l or 'fp_circle' in l or 'fp_line' in l or 'fp_rect' in l:
        print(l)
