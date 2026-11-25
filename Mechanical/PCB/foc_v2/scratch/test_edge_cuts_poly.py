import math
import sys
sys.path.append('scratch')
from verify_exact_boxes import boxes

CX, CY = 100.0, 100.0
R = 35.0

# Shape of board:
# Base is circle of radius R=35.0, BUT bounded by:
# y <= 132.5 (South cut)
# x >= 66.5  (West cut)
# x <= 135.0 (East cut)
# And North is y >= 65.0 (circle top).

def is_inside_board(x, y):
    if y > 132.5: return False
    if x < 66.5: return False
    if x > 135.0: return False
    # check circle:
    # If a point is within the flat cut extensions:
    # Notice: South cut is y <= 132.5. At South corners (x in [80, 120]), dy = 32.5.
    # Radius to (100, 100):
    d = math.hypot(x - CX, y - CY)
    if d <= 35.0:
        return True
    # If d > 35.0, is it in the allowable flat cut tab?
    # South flat tab: y between 120.0 and 132.5, x between 82.0 and 118.0
    if 120.0 <= y <= 132.5 and 82.0 <= x <= 118.0:
        return True
    # West flat tab: x between 66.5 and 75.0, y between 90.0 and 110.0
    if 66.5 <= x <= 75.0 and 90.0 <= y <= 110.0:
        return True
    # East flat tab: x between 125.0 and 135.0, y between 88.0 and 115.0
    if 125.0 <= x <= 135.0 and 88.0 <= y <= 115.0:
        return True
    return False

outside_pts = []
for k, b in boxes.items():
    if k in ['C_BULK1', 'C63']:
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            px = b['x'] + 5.0 * math.cos(rad)
            py = b['y'] + 5.0 * math.sin(rad)
            if not is_inside_board(px, py):
                outside_pts.append(f"{k} cylinder point ({px:.2f}, {py:.2f}) outside")
        continue
    for px, py in [(b['x1'], b['y1']), (b['x1'], b['y2']), (b['x2'], b['y1']), (b['x2'], b['y2'])]:
        if not is_inside_board(px, py):
            outside_pts.append(f"{k} point ({px:.2f}, {py:.2f}) outside")

print(f"Total points outside: {len(outside_pts)}")
for p in outside_pts:
    print(" ", p)
