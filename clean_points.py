import os
import re

base_path = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

subjects_config = {
    "Fisica_Todos los documentos": {"func": "savePointsFisica", "points_prop": "puntos_fisica"},
    "Qumica_Todos los documentos": {"func": "savePointsQuimica", "points_prop": "puntos_quimica"},
    "Matemticas_Todos los documetos": {"func": "savePointsMatematicas", "points_prop": "puntos_matematicas"},
}

for root_dir, info in subjects_config.items():
    subject_path = os.path.join(base_path, root_dir)
    if not os.path.exists(subject_path):
        continue

    func_name = info["func"]
    pts_prop = info["points_prop"]

    for root, dirs, files in os.walk(subject_path):
        for f in files:
            if not f.endswith(".html"):
                continue

            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()

            changed = False
            
            # Change savePoints*(100) -> savePoints*(10)
            pattern_call = rf"window\.{func_name}\(100\)"
            if re.search(pattern_call, content):
                content = re.sub(pattern_call, f"window.{func_name}(10)", content)
                changed = True
                
            # Replace the problematic object with the clean one
            # The problematic structure depends heavily on line breaks that may vary (often minified or expanded)
            # Use regex to identify any updateDoc payload that modifies points and streak directly in these files.
            
            # Case 1 (Single Line): { points: increment(pts), puntos_fisica: increment(pts), racha_fisica: increment(1), streak: increment(1) }
            # Case 2 (Multi Line)
            # Let's cleanly replace the properties being incremented inside the { ... } object of the updateDoc call that follows `window.savePoints*`
            
            # Since the structure is consistent:
            pattern_assign = re.compile(
                r'\{[^}]*points:\s*increment\(pts\)[^}]*\}'
            )
            
            if re.search(pattern_assign, content):
                new_payload = f"{{ {pts_prop}: increment(pts) }}"
                content = re.sub(pattern_assign, new_payload, content)
                changed = True

            if changed:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Patched savePoints in {f}")

print("Cleaned XP tracking!")
