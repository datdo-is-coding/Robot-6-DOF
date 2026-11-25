from inspect_j8_detail import get_fp
import re

fp_j7 = get_fp('J7')
print("=== J7 Courtyard and Pads ===")
for m in re.finditer(r'\(fp_line\s+\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\).*?\(layer\s+"F\.CrtYd"\)', fp_j7, re.DOTALL):
    print(f"Line: ({m.group(1)}, {m.group(2)}) -> ({m.group(3)}, {m.group(4)})")
for m in re.finditer(r'\(pad\s+"([^"]*)"\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)', fp_j7):
    print(f"Pad {m.group(1)} at ({m.group(2)}, {m.group(3)})")
