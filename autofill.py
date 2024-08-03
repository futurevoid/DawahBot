import json

# Load the materials JSON data
with open('materials.json', 'r') as f:
    materials = json.load(f)

# Read the links from the text file
with open('links.txt', 'r') as f:
    lines = f.readlines()

# Update the materials dictionary with the links
for i, line in enumerate(lines, start=1):
    key = f"الدرس {i}"
    mat = "2- لينك اليوتيوب. 📽"
    if key in materials["شرح كتاب اصول الفقة التي يعلم منها حاله الشيخ خالد منصور"]:
        materials["شرح كتاب اصول الفقة التي يعلم منها حاله الشيخ خالد منصور"][key][mat] = line.strip()

# Write the updated materials back to the JSON file
with open('materials.json', 'w') as f:
    json.dump(materials, f, ensure_ascii=False, indent=4)

