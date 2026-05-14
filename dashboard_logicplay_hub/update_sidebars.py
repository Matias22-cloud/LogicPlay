import os
import re

root_dir = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

files_to_fix = [
    r"Fisica_Todos los documentos\f_sica_selecci_n_de_temas\code.html",
    r"Qumica_Todos los documentos\quimica_selecci_n_de_temas\code.html",
    r"Matemticas_Todos los documetos\matematica_selecci_n_de_temas.html"
]

for file_rel in files_to_fix:
    fpath = os.path.join(root_dir, file_rel)
    if not os.path.exists(fpath): continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    # Replace relative links with correct ones to dashboards 
    
    # Física
    new_content = re.sub(r'href="[^"]*f_sica_selecci_n_de_temas/code\.html"', 'href="../../dashboard_fisica.html"', new_content)
    
    # Química
    new_content = re.sub(r'href="[^"]*quimica_selecci_n_de_temas/code\.html"', 'href="../../dashboard_quimica.html"', new_content)
    
    # Matemáticas
    new_content = re.sub(r'href="[^"]*matematica_selecci_n_de_temas\.html"', 'href="../../dashboard_matematicas.html"', new_content)
    
    # If the link was "#" because it was the active page in the sidebar, let's keep it as "#" if it has class containing bg-primary text-white
    # Wait, the active link in the sidebar is just `href="#"`. So the regex above only catches non-active links. This is fine, since active link is already "#".
    # BUT we want the sidebar to link to the Dashboards, not other theme selection pages!

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_rel}")
