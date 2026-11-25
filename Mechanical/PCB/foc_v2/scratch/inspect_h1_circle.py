from inspect_j8_detail import get_fp

fp_h1 = get_fp('H1')
lines = fp_h1.splitlines()
for i, l in enumerate(lines):
    if 'fp_circle' in l:
        print('\n'.join(lines[i:i+6]))
        print('---')
