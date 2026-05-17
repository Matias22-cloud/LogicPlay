import re
import os

files = [
    'dashboard_logicplay_hub/index.html',
    'dashboard_logicplay_hub/dashboard_fisica.html',
    'dashboard_logicplay_hub/dashboard_quimica.html',
    'dashboard_logicplay_hub/dashboard_matematicas.html'
]

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Mark Assistant
    content = re.sub(r'<!-- Mark Assistant -->\s*<script type="module" src="mark_assistant\.js"></script>', '', content)

    # 2. Fix Header Avatar displayName logic
    content = re.sub(
        r'if \(data\.photoURL\) \{\s*domHeaderAvatar\.innerHTML = `<img alt="\$\{data\.name\}"[^>]*>`[^}]*\} else \{\s*domHeaderAvatar\.innerHTML = `<div[^>]*>\$\{data\.name\.charAt\(0\)\.toUpperCase\(\)\}<\/div>`;\s*\}',
        r'''const displayName = data.nombre || data.name || 'Estudiante';
                        if (data.photoURL) {
                            domHeaderAvatar.innerHTML = `<img alt="${displayName}" class="w-full h-full object-cover" src="${data.photoURL}" />`;
                        } else {
                            domHeaderAvatar.innerHTML = `<div class="w-full h-full flex items-center justify-center bg-primary text-white font-bold text-lg">${displayName.charAt(0).toUpperCase()}</div>`;
                        }''',
        content
    )

    # 3. Fix loadRanking displayName
    content = re.sub(
        r'let avatarHtml = \'\';\s*if \(data\.photoURL\) \{\s*avatarHtml = `<img alt="\$\{data\.name\}"[^>]*>`[^}]*\} else \{\s*avatarHtml = `<div[^>]*>\$\{data\.name\.charAt\(0\)\.toUpperCase\(\)\}<\/div>`;\s*\}',
        r'''let avatarHtml = '';
                    let displayName = data.nombre || data.name || 'Estudiante';
                    if (data.photoURL) {
                        avatarHtml = `<img alt="${displayName}" class="w-full h-full object-cover" src="${data.photoURL}" />`;
                    } else {
                        avatarHtml = `<div class="w-full h-full flex items-center justify-center bg-indigo-500 text-white font-bold text-base">${displayName.charAt(0).toUpperCase()}</div>`;
                    }''',
        content
    )

    content = re.sub(
        r'<p class="text-sm font-bold \$\{isMe \? \'text-primary\' : \'\'\}">\$\{data\.name\} \$\{isMe \? \'\(Tú\)\' : \'\'\}<\/p>',
        r'<p class="text-sm font-bold ${isMe ? \'text-primary\' : \'\'}">${displayName} ${isMe ? \'(Tú)\' : \'\'}</p>',
        content
    )

    # 4. Fix registerActivity (XP + Streak)
    streak_logic_old = r'''let updates = \{ points: \(data\.points \|\| 0\) \+ 10 \}; // 10 points per generic activity

                    if \(data\.lastActivity !== today\) \{
                        const yesterday = new Date\(\);
                        yesterday\.setDate\(yesterday\.getDate\(\) - 1\);
                        const yesterdayStr = yesterday\.getFullYear\(\) \+ "-" \+ \(yesterday\.getMonth\(\) \+ 1\) \+ "-" \+ yesterday\.getDate\(\);

                        if \(data\.lastActivity === yesterdayStr\) \{
                            updates\.streak = \(data\.streak \|\| 0\) \+ 1;
                        \} else \{
                            updates\.streak = 1;
                        \}
                        updates\.lastActivity = today;
                    \}

                    await updateDoc\(userRef, updates\);'''

    streak_logic_new = r'''let updates = {};

                    if (data.lastActivity !== today && data.lastActivity) {
                        const lastActDate = new Date(data.lastActivity);
                        const currDate = new Date(today);
                        const diffTime = Math.abs(currDate - lastActDate);
                        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
                        
                        if (diffDays <= 2) {
                            updates.streak = (data.streak || 0) + 1;
                        } else {
                            updates.streak = 1;
                        }
                        updates.lastActivity = today;
                    } else if (!data.lastActivity) {
                        updates.streak = 1;
                        updates.lastActivity = today;
                    }

                    if (Object.keys(updates).length > 0) {
                        await updateDoc(userRef, updates);
                    }'''

    content = re.sub(streak_logic_old, streak_logic_new, content)

    # 5. PWA Icon in Head
    if '<link rel="icon" type="image/x-icon" href="/logicplay.ico">' in content:
        content = content.replace('<link rel="icon" type="image/x-icon" href="/logicplay.ico">', '<link rel="icon" href="/LogicPlay.ico">')
    
    if '<link rel="icon" type="image/x-icon" href="/LogicPlay.ico">' not in content and '<link rel="icon" href="/LogicPlay.ico">' not in content:
         # add to head if not present
         content = content.replace('</head>', '    <link rel="icon" type="image/x-icon" href="/LogicPlay.ico">\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in files:
    full_path = os.path.join(r"c:\Users\Steven\Desktop\LogiPlayAPP", f)
    patch_file(full_path)
