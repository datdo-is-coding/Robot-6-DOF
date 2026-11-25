import math

# KiCad transforms: 
# For rotation theta in degrees (counter-clockwise in standard KiCad, or clockwise? Let's check from the file)
# In kicad_pcb:
# pad at local (px, py) rotated by theta:
# x_world = x0 + px*cos(theta) - py*sin(theta)
# y_world = y0 + px*sin(theta) + py*cos(theta)

def transform(x0, y0, theta_deg, lx, ly):
    rad = math.radians(theta_deg)
    # KiCad rotates clockwise in screen space (since Y is down):
    # or counter-clockwise in math space?
    # Let's check with an actual pad from the pcb!
    c = math.cos(rad)
    s = math.sin(rad)
    return x0 + lx*c - ly*s, y0 + lx*s + ly*c

# Let's check J11 in foc_v2.kicad_pcb
import re
with open('foc_v2.kicad_pcb', 'r') as f:
    text = f.read()

# find J11 block
b = text.split('(footprint "foc_v2:AMASS_XT30PW-M_Edge_NoSilk"')[1].split('(property "Reference" "J11"')[0]
print("J11 header:", b[:200])
