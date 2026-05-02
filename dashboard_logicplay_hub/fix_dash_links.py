import os
import glob

base_dir = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

files_to_check = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

for file_path in files_to_check:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    # For subdirectories like `Fisica_Todos los documentos/f_sica_mru/practica.html`
    new_content = new_content.replace(
        'href="../../dashboard_logicplay_clasificaci_n_anonimizada/code.html"',
        'href="../../index.html"'
    )
    # For single level subdirectories like `cursos/index.html`
    new_content = new_content.replace(
        'href="../dashboard_logicplay_clasificaci_n_anonimizada/code.html"',
        'href="../index.html"'
    )
    # For files in the same directory (though they should just link to index.html directly)
    new_content = new_content.replace(
        'href="dashboard_logicplay_clasificaci_n_anonimizada/code.html"',
        'href="index.html"'
    )
    
    # Just in case there are single quotes:
    new_content = new_content.replace(
        "href='../../dashboard_logicplay_clasificaci_n_anonimizada/code.html'",
        "href='../../index.html'"
    )
    new_content = new_content.replace(
        "href='../dashboard_logicplay_clasificaci_n_anonimizada/code.html'",
        "href='../index.html'"
    )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed Dashboard links in: {file_path}")
