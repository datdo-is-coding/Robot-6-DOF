with open("communication.kicad_sch", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("J8 symbol instance:")
for j in range(5800, 5845):
    print(lines[j].rstrip())

print("\nJ8 pins section:")
for j in range(5845, 5885):
    print(lines[j].rstrip())
