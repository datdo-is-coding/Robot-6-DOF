with open("scratch/apply_final_clean_layout.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    'f\'\\t\\t(property "Description" ""\\n\',',
    'f\'\\t\\t(property "Description" "{extra_props.get("Description", "")}"\\n\','
)
text = text.replace(
    'extra_props={"LCSC Part #": "C293630", "KLC_S3.3": "", "KLC_S4.1": "", "Availability": "", "Price": "", "SNAPEDA_PN": ""}',
    'extra_props={"LCSC Part #": "C293630", "KLC_S3.3": "", "KLC_S4.1": "", "Availability": "", "Price": "", "SNAPEDA_PN": "", "Description": "Generic connectable mounting pin connector, single row, 01x03, script generated (kicad-library-utils/schlib/autogen/connector/)"}'
)

with open("scratch/apply_final_clean_layout.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated Description property in apply_final_clean_layout.py")
