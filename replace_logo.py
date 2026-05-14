import os
import re

workspace = r"c:\Users\Steven\Desktop\LogiPlayAPP"

# The SVG pattern to match
svg_pattern = re.compile(r'<svg[^>]*viewbox="0 0 48 48"[^>]*>.*?d="M24 0\.757355.*?<\/svg>', re.IGNORECASE | re.DOTALL)

def replace_in_files():
    total_replaced = 0
    for root, dirs, files in os.walk(workspace):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                # Calculate relative path to root workspace to reference logo.svg
                rel_dir = os.path.relpath(workspace, root)
                logo_path = "logo.svg" if rel_dir == "." else f"{rel_dir}/logo.svg".replace('\\', '/')
                
                img_tag = f'<img src="{logo_path}" alt="LogicPlay Logo" style="width: 32px; height: 32px;" />'
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                new_content, count = svg_pattern.subn(img_tag, content)
                
                if count > 0:
                    print(f"Replaced {count} occurrences in {file_path}")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    total_replaced += count
                    
    print(f"Total replacements: {total_replaced}")

if __name__ == "__main__":
    replace_in_files()
