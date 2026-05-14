import os
import re

base_path = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"

katex_snippet = """
    <!-- KaTeX for Math Rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js" 
        onload="renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '\\\\(', right: '\\\\)', display: false}]});"></script>
"""

instruction_addition = """\nCuando escribas fórmulas matemáticas, fórmulas de física o química, escríbelas en formato LaTeX usando doble backslash así: \\\\( fórmula \\\\) para fórmulas inline y $$ fórmula $$ para bloques. Por ejemplo: la velocidad es \\\\(v = \\\\frac{d}{t}\\\\) y la fuerza es \\\\(F = ma\\\\). """

def process_files():
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if not file.endswith(".html"):
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            modified = False

            # 1. Update gemini-3-flash-preview to gemini-1.5-flash
            if "gemini-3-flash-preview" in content:
                content = content.replace("gemini-3-flash-preview", "gemini-1.5-flash")
                modified = True

            # 2. Add System Instruction about LaTeX if GenAI is present
            if "GoogleGenAI" in content or "@google/genai" in content:
                if "fórmulas matemáticas, fórmulas de física" not in content:
                    # Look for systemInstruction text blocks
                    # E.g. 'text: "Eres un tutor...' or `text: 'Eres un tutor...` or `text: \`Eres un tutor...`
                    # The instruction_addition uses \\\\( to output \\( in JS template literals. 
                    # Let's insert it before the closing quote or backtick.
                    # We can use regex to find the system instruction block
                    def inject_instr(match):
                        q = match.group(1) # quote char
                        text = match.group(2)
                        return f'text: {q}{text}{instruction_addition}{q}'
                        
                    new_content, num = re.subn(r'text:\s*([\'"`])(.*?(?:tutor|experto).*?)(?=\1)', inject_instr, content, flags=re.DOTALL | re.IGNORECASE)
                    if num > 0:
                        content = new_content
                        modified = True
                    else:
                        # Fallback if specific words aren't found
                        new_content, num = re.subn(r'(systemInstruction:\s*\[\s*\{\s*parts:\s*\[\s*\{\s*text:\s*([\'"`]))(.*?)(?=\2)', r'\1\3' + instruction_addition, content, flags=re.DOTALL)
                        if num > 0:
                            content = new_content
                            modified = True

            # 3. Add KaTeX scripts
            # We want to add it to any file that has math replacements or AI, or just all files except maybe the simplest ones?
            # Safe to add to all html files with </head>.
            if "katex.min.css" not in content and "</head>" in content.lower():
                content = re.sub(r'</head>', katex_snippet + '\n</head>', content, flags=re.IGNORECASE)
                modified = True

            # 4. Replace common plain text math with KaTeX inline math
            # m/s² -> \( \text{m/s}^2 \)
            # don't do it inside HTML attributes (like id="x2Input" or class="...")
            # We will use simple replacements only outside of < > but that is hard in pure string replace.
            # However x² is rarely an attribute.
            
            # Helper to replace only outside tags safely? Too complex for python regex simply.
            # But x² is only used in text.
            orig_content = content
            content = content.replace("x²", r"\(x^2\)")
            content = content.replace("m/s²", r"\(\text{m/s}^2\)")
            content = content.replace("x³", r"\(x^3\)")
            content = content.replace("x₂", r"\(x_2\)")
            content = content.replace("x₁", r"\(x_1\)")
            
            # Special case for "2/2^2" and similar? The user mentioned them so we should just do generic ones safely
            # Since those are just text, no generic regex mapping unless specific. 
            
            if content != orig_content:
                modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Modified: {filepath}")

if __name__ == "__main__":
    process_files()
    print("All files processed.")
