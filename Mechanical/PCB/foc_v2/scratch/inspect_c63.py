from inspect_j8_detail import get_fp

fp_c63 = get_fp('C63')
print("=== C63 Footprint ===")
for l in fp_c63.splitlines()[:15]:
    print(l)
