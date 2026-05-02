import os
import glob

base_dir = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

targets = [
    "Fisica_Todos los documentos",
    "Qumica_Todos los documentos",
    "Matemticas_Todos los documetos"
]

files_to_check = []
for t in targets:
    search_path = os.path.join(base_dir, t, '**', '*.html')
    files_to_check.extend(glob.glob(search_path, recursive=True))

for file_path in files_to_check:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    # Fix dashboard link
    new_content = new_content.replace(
        'href="../dashboard_logicplay_clasificaci_n_anonimizada/code.html"',
        'href="../../dashboard_logicplay_clasificaci_n_anonimizada/code.html"'
    )
    # Fix manifest and service worker
    new_content = new_content.replace(
        'href="../manifest.json"',
        'href="../../manifest.json"'
    )
    new_content = new_content.replace(
        "register('../service-worker.js')",
        "register('../../service-worker.js')"
    )
    
    # Fix practica link
    new_content = new_content.replace(
        'href="../f_sica_pr_ctica_interactiva/code.html"',
        'href="../f_sica_pr_ctica_interactiva_3/code.html"'
    )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {file_path}")
