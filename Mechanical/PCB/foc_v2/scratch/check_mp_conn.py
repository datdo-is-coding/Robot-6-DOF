with open('communication.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for uuid "e001bb9f-9bd1-410c-bd18-d15c4d66e6df"
print("e001bb9f count:", text.count("e001bb9f"))
