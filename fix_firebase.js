const fs = require('fs');
const path = require('path');

function findFiles(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        file = path.join(dir, file);
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory() && !file.includes('node_modules') && !file.includes('.git')) {
            results = results.concat(findFiles(file));
        } else if (file.endsWith('.html')) {
            results.push(file);
        }
    });
    return results;
}

const files = findFiles(path.join(__dirname, 'dashboard_logicplay_hub'));
let count = 0;

const regex = /const firebaseConfig = {[\s\S]*?};\s*const app = initializeApp\(firebaseConfig\);\s*const db = getFirestore\(app\);/g;

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    const matches = content.match(regex);
    if (matches && matches.length > 1) {
        // Keep the first one, replace subsequent ones with just getting the default db
        let first = true;
        const newContent = content.replace(regex, (match) => {
            if (first) {
                first = false;
                return match;
            } else {
                return 'const db = getFirestore();';
            }
        });
        
        fs.writeFileSync(file, newContent, 'utf8');
        console.log('Fixed:', file);
        count++;
    }
});

console.log('Total files fixed:', count);
