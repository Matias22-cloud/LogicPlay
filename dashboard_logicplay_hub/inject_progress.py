import os
import re

base_path = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub"
dirs_to_check = ["Fisica_Todos los documentos", "Qumica_Todos los documentos", "Matemticas_Todos los documetos", "tipos_reacciones"]

script_template = """
    <!-- Progress Tracking Script Injected Automatically -->
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
        import { getFirestore, doc, getDoc, setDoc } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-firestore.js";

        const firebaseConfig = {
            apiKey: "AIzaSyBD3-ZnbczYZOuDm7e9OHLP6Xg68sdZ1so",
            authDomain: "logicplay-e775c.firebaseapp.com",
            projectId: "logicplay-e775c",
            storageBucket: "logicplay-e775c.firebasestorage.app",
            messagingSenderId: "11226997472",
            appId: "1:11226997472:web:836d7d87f4f6a01987e685"
        };
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);
        
        const uid = localStorage.getItem('logicplay_uid');
        const role = localStorage.getItem('logicplay_role');

        async function updateTopicProgress() {
            if (!uid || role === 'profesor') return;

            const topicId = "TOPIC_NAME";
            const progressValue = PROGRESS_VALUE;

            try {
                const userRef = doc(db, "users", uid);
                const docSnap = await getDoc(userRef);
                
                if (docSnap.exists()) {
                    let data = docSnap.data();
                    let currentProgressMap = data.progreso_temas || {};
                    let currentVal = currentProgressMap[topicId] || 0;
                    
                    if (progressValue > currentVal) {
                        currentProgressMap[topicId] = progressValue;
                        await setDoc(userRef, { progreso_temas: currentProgressMap }, { merge: true });
                        console.log(`Progreso actualizado a ${progressValue}% en el tema ${topicId}`);
                    }
                }
            } catch (err) {
                console.error("Error actualizando progreso", err);
            }
        }

        // Ejecutar si el dom ya cargo
        if(document.readyState === "complete" || document.readyState === "interactive") {
            setTimeout(updateTopicProgress, 1500);
        } else {
            document.addEventListener("DOMContentLoaded", () => setTimeout(updateTopicProgress, 1500));
        }
    </script>
"""

def inject():
    for root_dir in dirs_to_check:
        full_dir = os.path.join(base_path, root_dir)
        if not os.path.exists(full_dir):
            if root_dir == "tipos_reacciones":
                full_dir = os.path.join(base_path, root_dir)
            else:
                continue
                
        for root, dirs, files in os.walk(full_dir):
            # The topic name is the name of the folder inside the main category
            # Ensure it's not the root category itself
            if root == full_dir:
                continue
                
            topic_name = os.path.basename(root)
            
            # Check if this folder has code.html (selection dashboard), we don't inject here
            # We inject inside the actual content files: concepto, ejemplos, practica/laboratorio
            for file in files:
                if not file.endswith(".html"):
                    continue
                
                # Determine progress value
                val = 0
                f_lower = file.lower()
                if "concepto" in f_lower or "introduccion" in f_lower:
                    val = 33
                elif "ejemplo" in f_lower or "propiedades" in f_lower or "sarrus" in f_lower or "jordan" in f_lower:
                    # Treat properties, sarrus, jordan, etc without context as intermediate?
                    # Wait, sarrus/jordan are the only files in those maths folders. Let's make "code.html" or "laboratorio.html" or "practica.html" 100
                    val = 66
                elif "practica" in f_lower or "laboratorio" in f_lower or "code" in f_lower:
                    # Math specific
                    val = 100
                elif "funcioncuadratica" in f_lower:
                    # Let's map it based on numbers if it has any, otherwise just make them complete 33/66/100
                    pass
                
                # Default rules if missing
                if val == 0:
                    if "1" in f_lower: val = 33
                    elif "2" in f_lower: val = 66
                    else: val = 100 # Anything else reaches 100

                filepath = os.path.join(root, file)
                
                # Exclude the selection topics dashboard
                if topic_name.endswith("_selecci_n_de_temas") or topic_name.endswith("selecci_n_de_temas"):
                    continue
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check if it's already injected
                if "Progress Tracking Script Injected Automatically" in content:
                    continue
                    
                # Replace placeholders
                inject_str = script_template.replace("TOPIC_NAME", topic_name).replace("PROGRESS_VALUE", str(val))
                
                # Inject before </body>
                if "</body>" in content:
                    content = content.replace("</body>", inject_str + "\n</body>")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Injected into {filepath} (Val: {val})")

if __name__ == "__main__":
    inject()
    print("Done injecting.")
