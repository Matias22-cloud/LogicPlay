import os

target_file = r"c:\Users\Steven\Desktop\LogiPlayAPP\dashboard_logicplay_hub\Fisica_Todos los documentos\f_sica_mru\practica.html"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# REPLACEMENT 1: Challenge text
old_challenge = """El dron de entregas de "Los Pollos Hermanos" debe recorrer una distancia de <span
                                class="font-bold text-slate-900 dark:text-white border-b-2 border-primary/30 px-1">100.0
                                m</span> de forma rectilínea uniforme para entregar un pedido al cliente. Debe llegar en
                            exactamente <span
                                class="font-bold text-slate-900 dark:text-white border-b-2 border-primary/30 px-1">5.0
                                s</span>. ¿Qué velocidad (v) debes configurar en el panel para lograr una entrega
                            perfecta?"""

new_challenge = """Bienvenido al **Simulador MRU 3D**. El dron de entregas de "Los Pollos Hermanos" tiene la misión de soltar un paquete en exactamente <span class="font-bold text-primary border-b-2 border-primary/30 px-1">5.0 s</span>.
<br><br>Ajusta el slider de <b>Distancia (d)</b> para definir dónde dejar el paquete y el slider de <b>Velocidad (v)</b> para garantizar que se cumpla el objetivo de los 5 segundos de vuelo. ¡Gana 100 puntos de física si la ecuación es perfecta!"""

content = content.replace(old_challenge, new_challenge)

# REPLACEMENT 2: Parameters Panel
# Find the panel block from '<div class="lg:col-span-2 glass-panel p-6 rounded-3xl">' to the end of the feedback message.
# Instead of strict string index, we can use start/end locators

start_panel = content.find('<div class="lg:col-span-2 glass-panel p-6 rounded-3xl">')
end_panel = content.find('<div class="glass-panel p-6 rounded-3xl bg-primary/5 border-primary/20 flex flex-col gap-3">')

if start_panel != -1 and end_panel != -1:
    new_panel = """<div class="lg:col-span-2 glass-panel p-6 rounded-3xl">
                        <div class="flex items-center justify-between mb-6">
                            <h4 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Panel Interactivo 3D</h4>
                            <span class="text-[10px] px-2 py-1 bg-primary/20 text-primary rounded-md font-bold">MRU \\( v = d/t \\)</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-6">
                            <!-- Distancia Slider -->
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">straighten</span> Distancia (d)</span>
                                    <span class="text-slate-900 dark:text-white text-base"><span id="val_d_display">100</span> m</span>
                                </label>
                                <input id="slider_d" type="range" min="20" max="250" step="5" value="100" class="w-full h-2 bg-slate-200 dark:bg-slate-700 appearance-none rounded-full cursor-pointer accent-primary">
                            </div>
                            <!-- Velocidad Slider -->
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">speed</span> Velocidad (v)</span>
                                    <span class="text-slate-900 dark:text-white text-base"><span id="val_v_display">20</span> m/s</span>
                                </label>
                                <input id="slider_v" type="range" min="5" max="50" step="1" value="20" class="w-full h-2 bg-slate-200 dark:bg-slate-700 appearance-none rounded-full cursor-pointer accent-accent">
                            </div>
                        </div>
                        <!-- HUD KaTeX Fórmulas -->
                        <div class="bg-slate-50 dark:bg-slate-800/50 rounded-2xl p-4 flex flex-col items-center justify-center border border-slate-200 dark:border-slate-700 shadow-inner">
                            <span class="text-[10px] font-bold text-slate-400 mb-2 uppercase tracking-widest">Ecuación Calculada en Tiempo Real</span>
                            <div id="katex-formula" class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white my-1">
                                <!-- KaTeX renders here -->
                            </div>
                            <div class="mt-2 text-sm text-slate-500 font-medium tracking-wide">
                                Tiempo Teórico Prometido = <span id="val_t_display" class="font-bold text-accent">5.0</span> s
                            </div>
                        </div>
                        <div id="feedback_msg" class="mt-6 flex items-center justify-center gap-2 text-slate-500 bg-slate-100 dark:bg-slate-800 p-3 rounded-lg border border-slate-200 dark:border-slate-700 transition-all opacity-0">
                             <span class="material-symbols-outlined text-sm">info</span>
                             <span class="text-xs font-bold uppercase tracking-wider" id="feedback_text">Esperando Misión...</span>
                        </div>
                    </div>\n                    """
    content = content[:start_panel] + new_panel + content[end_panel:]

# REPLACEMENT 3: Canvas area
start_canvas = content.find('<!-- Canvas Container -->')
end_canvas = content.find('</section>')

new_canvas_area = """<!-- Canvas Container -->
                        <div id="threejs-container" class="w-full h-full absolute inset-0 cursor-crosshair"></div>

                        <!-- HUD -->
                        <div class="absolute top-6 left-6 flex gap-4 z-30 pointer-events-none">
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-primary/80">Recorrido d(t)</span>
                                <span id="hud_d" class="text-xl font-mono font-bold text-white shadow-sm">0.0<span class="text-xs ml-1 text-slate-400">m</span></span>
                            </div>
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-accent/80">Cronómetro (t)</span>
                                <span id="hud_t" class="text-xl font-mono font-bold text-white shadow-sm">0.0<span class="text-xs ml-1 text-slate-400">s</span></span>
                            </div>
                        </div>

                        <!-- Botón Simular -->
                        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 z-30 flex gap-4" id="botones_simulacion">
                            <button id="btn_simular" class="group relative flex items-center justify-center px-10 py-3 bg-primary text-white font-bold rounded-2xl shadow-2xl hover:scale-105 active:scale-95 transition-all outline-none border border-white/20">
                                <div class="absolute -inset-1 bg-primary blur opacity-40 group-hover:opacity-70 transition"></div>
                                <span class="relative flex items-center gap-2 shadow-sm text-lg">
                                    <span class="material-symbols-outlined text-2xl">rocket_launch</span> LANZAR DRON 3D
                                </span>
                            </button>
                        </div>

                        <div class="absolute top-6 right-6 z-30">
                            <button id="btn_reset_ext" class="size-10 rounded-xl bg-white/10 hover:bg-white/20 backdrop-blur border border-white/20 flex items-center justify-center text-white transition-all shadow-lg outline-none">
                                <span class="material-symbols-outlined text-xl">refresh</span>
                            </button>
                        </div>
                    </div>
                """
if start_canvas != -1 and end_canvas != -1:
    content = content[:start_canvas] + new_canvas_area + content[end_canvas:]


# REPLACEMENT 4: Script logic
# Old script starts at `<script>\n        let simulacionId = null;` up to just before `<script>\n        let deferredPrompt;` or `<!-- Faraday Chatbot UI -->`

start_script = content.find('<script>\n        let simulacionId = null;')
end_script = content.find('<!-- Faraday Chatbot UI -->')

if start_script != -1 and end_script != -1:
    threejs_script = """<!-- Three.js 3D Physics Simulator -->
    <script type="module">
        import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js';

        // Variables
        let scene, camera, renderer;
        let car, road, targetBox, markPoint;
        let simRunning = false;
        let timeElapsed = 0;
        let vehiclePos = 0;
        let requestID;

        // UI Elements
        const sliderD = document.getElementById('slider_d');
        const sliderV = document.getElementById('slider_v');
        const valDText = document.getElementById('val_d_display');
        const valVText = document.getElementById('val_v_display');
        const valTText = document.getElementById('val_t_display');
        const formulaContainer = document.getElementById('katex-formula');
        const btnSimular = document.getElementById('btn_simular');
        const btnReset = document.getElementById('btn_reset_ext');
        const hudD = document.getElementById('hud_d');
        const hudT = document.getElementById('hud_t');
        const fbMsg = document.getElementById('feedback_msg');
        const fbText = document.getElementById('feedback_text');

        const TARGET_TIME = 5.0;

        function updateMathHUD() {
            const d = parseFloat(sliderD.value);
            const v = parseFloat(sliderV.value);
            valDText.innerText = d;
            valVText.innerText = v;
            
            const t = d / v;
            valTText.innerText = t.toFixed(2);
            
            if(window.katex) {
                const latex = `v = \\\\frac{d}{t} \\\\implies ${v} = \\\\frac{${d}}{${t.toFixed(2)}}`;
                katex.render(latex, formulaContainer, { throwOnError: false, displayMode: true });
            }
            
            if (targetBox) {
                targetBox.position.z = -d;
            }
        }
        
        sliderD.addEventListener('input', updateMathHUD);
        sliderV.addEventListener('input', updateMathHUD);

        function init3D() {
            const container = document.getElementById('threejs-container');
            const width = container.clientWidth;
            const height = container.clientHeight;

            scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x0f172a, 0.008); // Dark fog matching slate-900 background
            
            camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
            camera.position.set(0, 5, 8); // Start slightly behind Z=0

            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(width, height);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Lighting
            const ambient = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambient);
            
            const dirLight = new THREE.DirectionalLight(0xffffff, 1);
            dirLight.position.set(50, 100, 50);
            dirLight.castShadow = true;
            dirLight.shadow.mapSize.width = 1024;
            dirLight.shadow.mapSize.height = 1024;
            dirLight.shadow.camera.near = 0.5;
            dirLight.shadow.camera.far = 500;
            scene.add(dirLight);

            // Road Strip
            const roadGeometry = new THREE.PlaneGeometry(8, 600);
            const roadMaterial = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 });
            road = new THREE.Mesh(roadGeometry, roadMaterial);
            road.rotation.x = -Math.PI / 2;
            road.position.z = -250;
            road.receiveShadow = true;
            scene.add(road);
            
            // Grid helper across road
            const grid = new THREE.GridHelper(20, 20, 0x4f46e5, 0x334155);
            grid.position.y = 0.01;
            scene.add(grid);

            // Create Drone Object
            const droneGroup = new THREE.Group();
            
            const bodyGeo = new THREE.BoxGeometry(2, 0.8, 4);
            const bodyMat = new THREE.MeshStandardMaterial({ color: 0x4f46e5, metalness: 0.3, roughness: 0.2 });
            const body = new THREE.Mesh(bodyGeo, bodyMat);
            body.castShadow = true;
            
            const cockpitGeo = new THREE.BoxGeometry(1.4, 0.5, 1.5);
            const cockpitMat = new THREE.MeshStandardMaterial({ color: 0x0ea5e9, opacity: 0.8, transparent: true });
            const cockpit = new THREE.Mesh(cockpitGeo, cockpitMat);
            cockpit.position.set(0, 0.6, 0.5);
            
            // Simple propellers or wings
            const wingGeo = new THREE.BoxGeometry(6, 0.1, 1);
            const wingMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8 });
            const wing = new THREE.Mesh(wingGeo, wingMat);
            wing.position.set(0, 0, -1);
            
            droneGroup.add(body);
            droneGroup.add(cockpit);
            droneGroup.add(wing);
            droneGroup.position.set(0, 1, 0); // initial start Z=0
            
            car = droneGroup;
            scene.add(car);
            
            // Target Box / Delivery point
            const targetGeo = new THREE.BoxGeometry(4, 0.2, 4);
            const targetMat = new THREE.MeshStandardMaterial({ color: 0x22c55e, emissive: 0x16a34a, emissiveIntensity: 0.8 });
            targetBox = new THREE.Mesh(targetGeo, targetMat);
            targetBox.position.set(0, 0.1, -100);
            targetBox.receiveShadow = true;
            scene.add(targetBox);

            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
            
            updateMathHUD();
            renderFrame();
        }

        function renderFrame() {
            requestID = requestAnimationFrame(renderFrame);
            renderer.render(scene, camera);
            
            if(!simRunning) {
                // Subtle hover effect
                car.position.y = 1 + Math.sin(Date.now() * 0.003) * 0.1;
                camera.position.x = Math.sin(Date.now() * 0.0005) * 3;
                camera.lookAt(car.position.x, car.position.y, car.position.z - 20);
            }
        }

        function startSimulation() {
            if(simRunning) return;
            
            const v = parseFloat(sliderV.value);
            const targetD = parseFloat(sliderD.value);
            
            simRunning = true;
            timeElapsed = 0;
            vehiclePos = 0;
            btnSimular.style.display = 'none';
            btnSimular.parentElement.classList.add('opacity-0', 'pointer-events-none');
            sliderD.disabled = true;
            sliderV.disabled = true;
            fbMsg.style.opacity = '0';
            
            // Re-center camera behind car
            camera.position.x = 0;
            camera.position.y = 4;
            
            let lastTime = performance.now();

            const loop = (timestamp) => {
                if(!simRunning) return;
                
                const dt = (timestamp - lastTime) / 1000;
                lastTime = timestamp;
                
                // Safety limit dt to prevent huge jumps if tab was inactive
                if (dt < 0.5) {
                    timeElapsed += dt;
                    vehiclePos = v * timeElapsed;
                }
                
                car.position.z = -vehiclePos;
                
                // Camera follows vehicle
                camera.position.z = car.position.z + 8;
                camera.lookAt(0, 1, car.position.z - 20);
                
                // Update HUD
                hudD.innerHTML = vehiclePos.toFixed(1) + '<span class="text-xs ml-1 text-slate-400">m</span>';
                hudT.innerHTML = timeElapsed.toFixed(1) + '<span class="text-xs ml-1 text-slate-400">s</span>';
                
                if(vehiclePos >= targetD) {
                    vehiclePos = targetD;
                    car.position.z = -vehiclePos;
                    endSimulation(v, targetD, timeElapsed);
                    return; 
                }
                
                if(timeElapsed >= TARGET_TIME + 2.0) {
                     endSimulation(v, targetD, timeElapsed);
                     return;
                }
                
                requestID = requestAnimationFrame(loop);
            };
            requestID = requestAnimationFrame((ts) => {
                lastTime = ts; 
                loop(ts);
            });
        }

        function endSimulation(v, d, t) {
            simRunning = false;
            
            const diff = Math.abs(t - TARGET_TIME);
            fbMsg.style.opacity = '1';
            
            // Dramatic camera zoom
            camera.position.set(4, 2, car.position.z + 5);
            camera.lookAt(car.position.x, car.position.y, car.position.z);
            
            if(diff <= 0.1 && Math.abs(d - vehiclePos) <= 0.1) {
                fbMsg.className = "mt-6 flex items-center justify-center gap-2 text-white bg-green-500 p-4 rounded-xl shadow-xl transition-all font-bold text-sm tracking-wide";
                fbText.innerText = "¡MISIÓN PERFECTA! Tiempo exacto. +100 PUNTOS DE FÍSICA.";
                if(window.savePointsFisica) window.savePointsFisica(100);
            } else if (t > TARGET_TIME) {
                fbMsg.className = "mt-6 flex items-center justify-center gap-2 text-accent bg-accent/10 p-4 rounded-xl border border-accent/30 transition-all font-bold text-sm text-center";
                fbText.innerText = "¡UY! LLEGASTE TARDE. (Más de 5s). ¡Aumenta tu velocidad para recorrer la misma distancia en menos tiempo!";
            } else {
                fbMsg.className = "mt-6 flex items-center justify-center gap-2 text-primary bg-primary/10 p-4 rounded-xl border border-primary/30 transition-all font-bold text-sm text-center";
                fbText.innerText = "¡MÁS DESPACIO! Llegaste muy rápido (Antes de los 5s). Baja tu velocidad.";
            }
        }
        
        btnSimular.addEventListener('click', startSimulation);

        btnReset.addEventListener('click', () => {
             simRunning = false;
             timeElapsed = 0;
             vehiclePos = 0;
             car.position.z = 0;
             car.position.y = 1;
             
             // Reset UI state
             btnSimular.style.display = 'flex';
             btnSimular.parentElement.classList.remove('opacity-0', 'pointer-events-none');
             sliderD.disabled = false;
             sliderV.disabled = false;
             fbMsg.style.opacity = '0';
             
             hudD.innerHTML = '0.0<span class="text-xs ml-1 text-slate-400">m</span>';
             hudT.innerHTML = '0.0<span class="text-xs ml-1 text-slate-400">s</span>';
        });

        // Initialize at the end to ensure DOM is ready
        setTimeout(() => {
            init3D();
        }, 100);

    </script>
    """
    content = content[:start_script] + threejs_script + content[end_script:]

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Build 3D process completed successfully.")
