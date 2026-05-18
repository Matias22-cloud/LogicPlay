import os
import re

base = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

for root, d, files in os.walk(base):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Calculate depth relative to dashboard_logicplay_hub
            depth = len(os.path.relpath(path, base).split(os.sep))
            back = "../" * (depth - 1) if depth > 1 else "./"
            
            # Replace logo.svg absolute to relative dynamic
            content = re.sub(r'src=["\'].*?logo\.svg["\']', f'src="{back}logo.svg"', content)
            
            # Replace favicon to absolute dynamic 
            # LogicPlay.ico is inside c:\Users\Steven\Desktop\LogiPlayAPP (One level above dashboard_logicplay_hub)
            content = re.sub(r'<link[^>]*rel=["\']icon["\'][^>]*>', '', content)
            favicon_str = f'<link rel="icon" href="{back}../LogicPlay.ico" type="image/x-icon">'
            content = re.sub(r'<head\b([^>]*)>', f'<head\\1>\n    {favicon_str}', content)
            
            with open(path, 'w', encoding='utf-8') as out:
                out.write(content)

print("Icons normalized to dynamically generated relative paths.")
