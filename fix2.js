const fs = require('fs');
const path = require('path');

const files = [
    'dashboard_logicplay_hub/dashboard_fisica.html',
    'dashboard_logicplay_hub/dashboard_matematicas.html',
    'dashboard_logicplay_hub/dashboard_quimica.html',
    'dashboard_logicplay_hub/index.html'
];

let count = 0;

files.forEach(f => {
    const file = path.join(__dirname, f);
    if (!fs.existsSync(file)) return;

    let content = fs.readFileSync(file, 'utf8');

    const regex = /const firebaseConfig = {[\s\S]*?};\s*(?:const|let|var)\s+app\s*=\s*initializeApp\(firebaseConfig(?:,\s*['\"][^'\"]+['\"])?\);[\s\S]*?(?:const|let|var)\s+(?:db|firestoreDB)\s*=\s*getFirestore\([a-zA-Z0-9_]*\);(?:[\s\S]*?(?:const|let|var)\s+auth\s*=\s*getAuth\([a-zA-Z0-9_]*\);)?/g;

    let first = true;
    const finalContent = content.replace(regex, (match) => {
        if (first) {
            first = false;
            return match;
        } else {
            let res = 'const db = getFirestore();';
            if (match.includes('getAuth')) {
                res += '\n        const auth = getAuth();';
            }
            return res;
        }
    });

    if (content !== finalContent) {
        fs.writeFileSync(file, finalContent, 'utf8');
        console.log('Fixed:', file);
        count++;
    } else {
        console.log('Failed to fix manually:', file);
    }
});

console.log('Total files fixed in step 3:', count);
