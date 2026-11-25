from inspect_j8_detail import get_fp
import re

components = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'J1', 'J2', 'J3', 'C_BUS1', 'C_BUS2', 'C_BUS3', 'C_BULK1', 'IC1', 'U1', 'J11']

for c in components:
    fp = get_fp(c)
    if fp:
        m_at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', fp)
        x = float(m_at.group(1)) if m_at else 0
        y = float(m_at.group(2)) if m_at else 0
        rot = float(m_at.group(3)) if m_at and m_at.group(3) else 0
        print(f"{c:8s}: at ({x:6.2f}, {y:6.2f}) rot={rot:5.1f}")
