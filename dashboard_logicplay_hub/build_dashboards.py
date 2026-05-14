import os
import re

root_dir = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"
index_path = os.path.join(root_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

subjects = [
    {
        "id": "fisica",
        "name": "Física",
        "icon": "science",
        "points_field": "puntos_fisica",
        "streak_field": "racha_fisica",
        "hero_title": "Laboratorio de Física",
        "hero_desc": "Domina el movimiento, las fuerzas y la energía. Resuelve problemas y compite en el ranking de Física.",
        "course_link": "Fisica_Todos los documentos/f_sica_selecci_n_de_temas/code.html",
        "hero_img": "psychology"
    },
    {
        "id": "quimica",
        "name": "Química",
        "icon": "biotech",
        "points_field": "puntos_quimica",
        "streak_field": "racha_quimica",
        "hero_title": "Laboratorio de Química",
        "hero_desc": "Mezcla elementos, balancea reacciones y descubre la composición del mundo. ¡Compite en el ranking de Química!",
        "course_link": "Qumica_Todos los documentos/quimica_selecci_n_de_temas/code.html",
        "hero_img": "science"
    },
    {
        "id": "matematicas",
        "name": "Matemáticas",
        "icon": "functions",
        "points_field": "puntos_matematicas",
        "streak_field": "racha_matematicas",
        "hero_title": "Centro de Cálculo",
        "hero_desc": "Resuelve integrales, optimiza funciones y domina el cálculo. ¡Usa tu mente matemática y encabeza el ranking!",
        "course_link": "Matemticas_Todos los documetos/matematica_selecci_n_de_temas.html",
        "hero_img": "functions"
    }
]

# Update index.html links to point to the dashboards
new_index_content = content
new_index_content = new_index_content.replace('href="Fisica_Todos%20los%20documentos/f_sica_selecci_n_de_temas/code.html"', 'href="dashboard_fisica.html"')
new_index_content = new_index_content.replace('href="Qumica_Todos%20los%20documentos/quimica_selecci_n_de_temas/code.html"', 'href="dashboard_quimica.html"')
new_index_content = new_index_content.replace('href="Matemticas_Todos%20los%20documetos/matematica_selecci_n_de_temas.html"', 'href="dashboard_matematicas.html"')

# We will save the updated index.html later! 
# Let's generate the dashboards using the modified index.html, so they already link correctly to each other.
base_dashboard = new_index_content

for s in subjects:
    dash = base_dashboard
    
    # 1. Navbar highlighting
    # De-highlight dashboard
    dash = dash.replace(
        '<a\n                    class="text-primary font-semibold hover:text-primary transition-colors flex items-center gap-2"\n                    href="#"><span class="material-symbols-outlined text-[20px]">dashboard</span> Dashboard</a>',
        '<a\n                    class="text-slate-500 dark:text-slate-400 hover:text-primary transition-colors flex items-center gap-2"\n                    href="index.html"><span class="material-symbols-outlined text-[20px]">dashboard</span> Dashboard</a>'
    )
    
    # Highlight specific subject
    # It currently is: <a class="text-slate-500 dark:text-slate-400 hover:text-primary transition-colors flex items-center gap-2" href="dashboard_SUBJECT.html"> <span class="material-symbols-outlined text-[20px]">ICON</span> Name </a>
    # We replace it with active classes
    dash = re.sub(
        r'<a class="[^"]+"(\s*)href="dashboard_' + s['id'] + r'\.html">(\s*)<span class="material-symbols-outlined text-\[20px\]">' + s['icon'] + r'</span> ' + s['name'] + r'(\s*)</a>',
        r'<a class="text-primary font-semibold bg-primary/10 px-3 py-1.5 rounded-lg hover:text-primary transition-colors flex items-center gap-2"\1href="dashboard_' + s['id'] + r'.html">\2<span class="material-symbols-outlined text-[20px]">' + s['icon'] + r'</span> ' + s['name'] + r'\3</a>',
        dash
    )
    
    # 2. Hero Section
    dash = re.sub(r'<h2 class="text-4xl md:text-5xl font-black mb-4 leading-tight">Reto Semanal: Desafío de\s*Lógica</h2>',
                  f'<h2 class="text-4xl md:text-5xl font-black mb-4 leading-tight">{s["hero_title"]}</h2>', dash)
    dash = re.sub(r'<p class="text-lg text-white/80 mb-8">Resuelve los 5 acertijos avanzados de esta semana y\s*gana un multiplicador de puntos x2 durante el fin de semana.</p>',
                  f'<p class="text-lg text-white/80 mb-8">{s["hero_desc"]}</p>', dash)
    dash = dash.replace("rotate-12\">psychology</span>", f"rotate-12\">{s['hero_img']}</span>")
    
    # Update button to point to course link (f_sica_selecci_n_de_temas...)
    dash = dash.replace("onclick=\"window.location.href='reto_semanal/teoria.html'\"", f"onclick=\"window.location.href='{s['course_link']}'\"")
    dash = dash.replace("Participar ahora", "Ir a Materia")

    # Update the "Cursos" link to point to the correct course
    # Actually, keep "Cursos" and "Retos" linking to their places, or maybe Cursos goes to the course.
    # The user says: "El dashboard principal que ya existe se mantiene igual pero muestra el total general. Los tres dashboards nuevos por materia muestran solo los puntos y racha de esa materia."
    
    # 3. Firebase fields update
    # In Javascript section, change data.points to data.puntos_fisica
    dash = dash.replace(
        "domStreak.textContent = `${data.streak || 0} Días`;",
        f"domStreak.textContent = `${{data.{s['streak_field']} || 0}} Días`;"
    )
    dash = dash.replace(
        "domPoints.textContent = `${data.points || 0} XP`;",
        f"domPoints.textContent = `${{data.{s['points_field']} || 0}} XP`;",
        1 # Only the one displaying total points for the material
    )
    
    # Leaderboard title
    dash = dash.replace(
        '<span class="text-xs font-bold text-slate-400">Global</span>',
        f'<span class="text-xs font-bold text-primary px-2 py-1 bg-primary/10 rounded-full">{s["name"]}</span>'
    )
    
    # Firebase ranking queries
    # orderBy("points", "desc") -> orderBy("puntos_fisica", "desc")
    dash = dash.replace(
        'orderBy("points", "desc")',
        f'orderBy("{s["points_field"]}", "desc")'
    )
    
    # Points displayed in ranking
    dash = dash.replace(
        '<p class="text-xs text-slate-500">${data.points || 0} XP</p>',
        f'<p class="text-xs text-slate-500">${{data.{s["points_field"]} || 0}} XP</p>'
    )
    
    with open(os.path.join(root_dir, f"dashboard_{s['id']}.html"), "w", encoding="utf-8") as out:
        out.write(dash)
        
with open(index_path, "w", encoding="utf-8") as idx:
    # ensure index dashboard button points to #
    base = new_index_content.replace(
        '<a\n                    class="text-primary font-semibold hover:text-primary transition-colors flex items-center gap-2"\n                    href="#">',
        '<a\n                    class="text-primary font-semibold hover:text-primary transition-colors flex items-center gap-2"\n                    href="#">'
    )
    idx.write(base)
    
print("Dashboards created successfully!")
