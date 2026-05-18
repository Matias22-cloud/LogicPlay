import os
import re

base_dir = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

# 1. Obtener HTML real de perfil y notificaciones
with open(os.path.join(base_dir, "dashboard_fisica.html"), 'r', encoding='utf-8') as f:
    dash_content = f.read()

start_str = '<!-- Notification Bell & Panel -->'
end_str = '<!-- Mobile Menu Button -->'
idx_start = dash_content.find(start_str)
idx_end = dash_content.find(end_str)

if idx_start == -1 or idx_end == -1:
    print("No se encontró el bloque de notificaciones en el dashboard matriz.")
    exit(1)

real_profile_html = dash_content[idx_start:idx_end]

subjects_config = [
    ("Fisica_Todos los documentos", "f_sica_selecci_n_de_temas/code.html"),
    ("Qumica_Todos los documentos", "quimica_selecci_n_de_temas/code.html"),
    ("Matemticas_Todos los documetos", "matematica_selecci_n_de_temas.html")
]

# Patterns for identifying the dummy buttons inside the shrinkage div:
# <div class="flex items-center gap-2 sm:gap-4 shrink-0"> ... </div>
import glob

files_modified = 0

for subj_folder, biblio_rel in subjects_config:
    subj_path = os.path.join(base_dir, subj_folder)
    if not os.path.isdir(subj_path):
        continue
    
    # Traverse all subdirectories to find HTML modules
    for root, dirs, files in os.walk(subj_path):
        for file in files:
            if not file.endswith(".html") or file == "code.html" or file == "matematica_selecci_n_de_temas.html": 
                # Ignore the library itself
                continue
            
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # The library URL must leap back over the current submodule folder
            biblioteca_path = f"../{biblio_rel}"
            
            # We want to replace from <button ...>Biblioteca</button> to <span class="material-symbols-outlined">person</span></button>
            # OR we can just inject into <div class="flex items-center gap-2 sm:gap-4 shrink-0">
            
            # Regex to find the <div class="flex items-center gap-2 sm:gap-4 shrink-0"> chunk and replace inner contents
            # Actually, standardizing is dangerous. Let's just catch the dummy Biblioteca button and dummy user button
            # Usually:
            # <button class="[^"]*">Biblioteca</button>\s*<button class="[^"]*">\s*<span class="material-symbols-outlined">person</span>\s*</button>
            
            pattern_dummy = r'<button[^>]*>\s*Biblioteca\s*</button>\s*<button[^>]*>\s*<span class="material-symbols-outlined">person</span>\s*</button>'
            
            replacement = f'''<a href="{biblioteca_path}" class="hidden sm:block px-4 py-2 text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-primary transition-colors">
                        Biblioteca
                    </a>
                    {real_profile_html}'''
            
            new_content, count = re.subn(pattern_dummy, replacement, content, flags=re.DOTALL)
            
            if count > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_modified += 1
                print(f"Updated {filepath}")
            else:
                # Sometimes the buttons might be slightly different.
                # Let's try another generic approach if the first fails:
                # replacing the whole shrink-0 div contents if we know Dashboard is there.
                pass

print(f"Total files updated: {files_modified}")
