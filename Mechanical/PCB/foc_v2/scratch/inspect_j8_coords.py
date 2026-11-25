from inspect_j8_detail import get_fp

for ref in ['J8', 'J10']:
    fp = get_fp(ref)
    lines = fp.splitlines()
    for i, l in enumerate(lines):
        if 'CrtYd' in l:
            # print previous 6 lines
            for k in range(max(0, i-6), i+2):
                print(lines[k])
        if '(pad ' in l:
            print(lines[l.find('(pad '):][:80])
            for k in range(i, min(len(lines), i+3)):
                print(' ', lines[k].strip())
