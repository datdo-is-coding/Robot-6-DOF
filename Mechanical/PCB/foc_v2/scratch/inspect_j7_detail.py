from inspect_j8_detail import get_fp

fp_j7 = get_fp('J7')
print("=== J7 PADS AND LINES ===")
for line in fp_j7.splitlines():
    if 'pad' in line or 'CrtYd' in line or 'fp_rect' in line:
        print(line)
