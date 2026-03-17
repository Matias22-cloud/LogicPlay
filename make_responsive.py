import os
import glob

base_dir = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

count = 0
for filepath in glob.glob(base_dir + '/**/*.html', recursive=True):
    # skip dashboard and landing since we manually configured them
    if filepath.endswith("index.html") and "dashboard_logicplay_hub\\index.html" in filepath:
        continue
    if filepath.endswith("landing.html"):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Replace hidden navbars with responsive wrapping flexboxes
    if 'class="hidden md:flex gap-8' in content:
        content = content.replace('class="hidden md:flex gap-8', 'class="flex flex-wrap lg:flex-nowrap gap-4 md:gap-8 justify-center')
        modified = True
        
    if 'class="hidden md:flex gap-6' in content:
        content = content.replace('class="hidden md:flex gap-6', 'class="flex flex-wrap lg:flex-nowrap gap-3 md:gap-6 justify-center')
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Made responsive navbar in: {os.path.basename(filepath)}")

print(f"Responsive fix applied to {count} files.")
