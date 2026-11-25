from inspect_j8_detail import get_fp

fp_h1 = get_fp('H1')
lines = fp_h1.splitlines()
for i, l in enumerate(lines):
    if 'F.CrtYd' in l:
        for k in range(max(0, i-5), i+2):
            print(lines[k])
