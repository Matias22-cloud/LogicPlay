import os
import glob

PWA_HEAD_BLOCK = """
    <!-- PWA Meta Tags & Service Worker -->
    <link rel="manifest" href="{rel_path}manifest.json">
    <meta name="theme-color" content="#2c0fbd">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <script>
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('{rel_path}service-worker.js')
                .then(registration => {{
                    console.log('ServiceWorker registration successful');
                }})
                .catch(err => {{
                    console.log('ServiceWorker registration failed: ', err);
                }});
            }});
        }}
    </script>
"""

PWA_BODY_BLOCK = """
    <script>
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            const installButtons = document.querySelectorAll('#install-button, #install-button-mobile, #install-button-landing');
            installButtons.forEach(btn => {{
                btn.style.display = 'flex'; // Make it visible if hidden
                btn.addEventListener('click', async () => {{
                    if (deferredPrompt) {{
                        deferredPrompt.prompt();
                        const {{ outcome }} = await deferredPrompt.userChoice;
                        console.log(`User response to the install prompt: ${{outcome}}`);
                        deferredPrompt = null;
                    }}
                }});
            }});
        }});
    </script>
"""

base_dir = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

count = 0
for filepath in glob.glob(base_dir + '/**/*.html', recursive=True):
    rel = os.path.relpath(base_dir, os.path.dirname(filepath))
    rel_path = "./" if rel == "." else rel.replace('\\', '/') + "/"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    if "rel=\"manifest\"" not in content:
        head_inject = PWA_HEAD_BLOCK.format(rel_path=rel_path)
        content = content.replace('</head>', head_inject + '\n</head>')
        modified = True
        
    if "beforeinstallprompt" not in content:
        content = content.replace('</body>', PWA_BODY_BLOCK.format() + '\n</body>')
        modified = True
        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")
        count += 1

print(f"PWA tags injected completely in {count} files.")
