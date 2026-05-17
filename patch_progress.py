import os
import json
import re

base_path = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

# Fix Manifest
manifest_path = os.path.join(base_path, "manifest.json")
try:
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "icons" in data and len(data["icons"]) > 0:
        data["icons"][0]["src"] = "/LogicPlay.ico"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
except Exception as e:
    print(f"Manifest error: {e}")

# Fix Progress Bars in 'concepto.html'
for root, dirs, files in os.walk(base_path):
    for filename in files:
        if filename.endswith("concepto.html"):
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace completado: 33% with 0%
            new_content = re.sub(r'COMPLETADO:\s*33%', 'COMPLETADO: 0%', content)
            new_content = re.sub(r'>33%<', '>0%<', new_content)
            new_content = re.sub(r'width:\s*33%', 'width: 0%', new_content)

            # Extra ensure text gets updated just in case
            new_content = new_content.replace('33%', '0%')
            new_content = new_content.replace('0%0%', '0%')

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Patched {filepath}")

# Optional: Clean up mark array script logic
index_path = os.path.join(base_path, "mark_assistant.js")
if os.path.exists(index_path):
    os.remove(index_path)
    print("Deleted mark_assistant.js")

