#!/usr/bin/env python3
"""Build 3D Peso y Masa simulator - planetary weight comparison."""
import os

FILE = os.path.join("Fisica_Todos los documentos", "f_sica_peso_y_masa", "practica.html")
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

NEW_BODY = r'''<body class="bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-slate-100 antialiased">
    <div class="relative flex h-auto min-h-screen w-full flex-col overflow-x-hidden">
        <header class="sticky top-0 z-50 glass-panel border-b px-4 sm:px-6 md:px-20 py-4">
            <div class="flex items-center justify-between max-w-7xl mx-auto w-full gap-2">
                <div class="flex items-center gap-2 sm:gap-4 text-primary min-w-0">
                    <div class="size-10 shrink-0 flex items-center justify-center bg-primary/10 rounded-xl"><span class="material-symbols-outlined text-primary text-2xl font-bold">science</span></div>
                    <div class="min-w-0"><h2 class="text-slate-900 dark:text-slate-100 text-xs sm:text-sm md:text-base font-bold leading-tight truncate">Fisica Practica Interactiva</h2></div>
                </div>
                <div class="flex items-center gap-2 sm:gap-4 shrink-0">
                    <nav class="flex items-center gap-2 sm:gap-4 text-sm font-semibold text-slate-500"><a class="hover:text-primary transition-colors text-xs sm:text-sm whitespace-nowrap" href="../../index.html">Dashboard</a></nav>
                    <button class="flex items-center justify-center rounded-xl h-9 w-9 sm:h-10 sm:w-10 bg-slate-100 dark:bg-slate-800 hover:bg-primary/10 transition-all group"><span class="material-symbols-outlined text-slate-600 dark:text-slate-400 group-hover:text-primary">person</span></button>
                </div>
            </div>
        </header>
        <main class="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
            <div class="mb-10">
                <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
                    <div>
                        <span class="text-primary font-bold text-sm tracking-widest uppercase mb-2 block">Modulo 03: Dinamica</span>
                        <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 dark:white tracking-tight">Peso y Masa</h1>
                    </div>
                </div>
                <div class="flex items-center gap-1 border-b border-slate-200 dark:border-slate-800">
                    <a class="nav-tab nav-tab-inactive" href="concepto.html">1. Concepto</a>
                    <a class="nav-tab nav-tab-inactive" href="ejemplos.html">2. Ejemplos</a>
                    <a class="nav-tab nav-tab-active" href="#">3. Practica</a>
                </div>
            </div>
            <div class="grid grid-cols-1 gap-8 fade-in">
                <section class="glass-panel p-6 md:p-8 rounded-3xl border-l-[6px] border-l-primary relative overflow-hidden">
                    <div class="absolute top-0 right-0 p-4 opacity-5"><span class="material-symbols-outlined text-9xl">rocket_launch</span></div>
                    <div class="flex items-center gap-3 mb-4"><span class="material-symbols-outlined text-primary fill-1">assignment</span><h3 class="text-xl font-bold text-slate-800 dark:text-slate-200">Simulador 3D: Peso en Diferentes Planetas</h3></div>
                    <div class="relative z-10">
                        <p class="text-lg text-slate-600 dark:text-slate-400 leading-relaxed font-light">
                            Ajusta la <b>masa</b> del astronauta y selecciona un <b>planeta</b>. El objeto caera con la gravedad local. Calcula el <b>Peso (P = m × g)</b> en ese planeta para ganar <span class="font-bold text-primary">100 puntos</span>.
                        </p>
                    </div>
                </section>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 glass-panel p-6 rounded-3xl">
                        <div class="flex items-center justify-between mb-6">
                            <h4 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Panel Interactivo 3D</h4>
                            <span class="text-[10px] px-2 py-1 bg-primary/20 text-primary rounded-md font-bold">P = m · g</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-6">
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">fitness_center</span> Masa (m)</span>
                                    <span class="text-slate-900 dark:text-white text-base"><span id="val_m_display">80</span> kg</span>
                                </label>
                                <input id="slider_m" type="range" min="10" max="200" step="5" value="80" class="w-full h-2 bg-slate-200 dark:bg-slate-700 appearance-none rounded-full cursor-pointer accent-primary">
                            </div>
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">public</span> Planeta</span>
                                    <span class="text-slate-900 dark:text-white text-base" id="val_planet_display">Marte</span>
                                </label>
                                <select id="select_planet" class="w-full h-10 bg-slate-100 dark:bg-slate-800 border-2 border-primary/30 rounded-xl px-3 text-sm font-bold text-primary focus:ring-primary cursor-pointer">
                                    <option value="3.72" data-name="Marte" data-color="#c0392b" selected>Marte (g = 3.72)</option>
                                    <option value="9.81" data-name="Tierra" data-color="#2980b9">Tierra (g = 9.81)</option>
                                    <option value="1.62" data-name="Luna" data-color="#7f8c8d">Luna (g = 1.62)</option>
                                    <option value="24.79" data-name="Jupiter" data-color="#d35400">Jupiter (g = 24.79)</option>
                                    <option value="8.87" data-name="Venus" data-color="#e67e22">Venus (g = 8.87)</option>
                                </select>
                            </div>
                        </div>
                        <div class="bg-slate-50 dark:bg-slate-800/50 rounded-2xl p-4 flex flex-col items-center justify-center border border-slate-200 dark:border-slate-700 shadow-inner">
                            <span class="text-[10px] font-bold text-slate-400 mb-2 uppercase tracking-widest">Ecuacion en Tiempo Real</span>
                            <div id="katex-formula" class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white my-1"></div>
                        </div>
                        <div class="mt-4 flex items-center gap-4">
                            <div class="flex-1 relative flex items-center rounded-xl overflow-hidden bg-white dark:bg-slate-800/80 border-2 border-primary/40 focus-within:border-primary shadow-sm">
                                <input id="input_p" class="w-full bg-transparent border-none text-sm font-bold px-3 py-2.5 focus:ring-0 text-primary" placeholder="Ingresa el Peso P..." type="number" step="0.1">
                                <span class="text-[10px] font-bold text-slate-400 pr-3">N</span>
                            </div>
                            <button id="btn_check" class="px-6 py-2.5 bg-primary text-white font-bold rounded-xl shadow-lg hover:scale-105 active:scale-95 transition-all text-sm">VERIFICAR</button>
                        </div>
                        <div id="feedback_msg" class="mt-4 flex items-center justify-center gap-2 text-slate-500 bg-slate-100 dark:bg-slate-800 p-3 rounded-lg border border-slate-200 dark:border-slate-700 transition-all opacity-0">
                             <span class="material-symbols-outlined text-sm">info</span>
                             <span class="text-xs font-bold uppercase tracking-wider" id="feedback_text">Esperando...</span>
                        </div>
                    </div>
                    <div class="glass-panel p-6 rounded-3xl bg-primary/5 border-primary/20 flex flex-col gap-3">
                        <div class="flex items-center gap-2 text-primary"><span class="material-symbols-outlined fill-1">lightbulb</span><h4 class="font-bold text-sm uppercase tracking-wider">Consejo Pedagogico</h4></div>
                        <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed italic">"El peso depende de la gravedad del planeta. Usa <strong>P = m × g</strong> donde m es constante y g cambia segun el planeta. En Marte g es menor, asi que el peso tambien sera menor."</p>
                    </div>
                </div>

                <section class="relative group mt-2">
                    <div class="absolute -inset-1 bg-gradient-to-r from-primary to-accent rounded-[2.5rem] blur opacity-20 group-hover:opacity-30 transition duration-1000"></div>
                    <div class="relative glass-panel rounded-[2rem] overflow-hidden bg-slate-900 aspect-[21/9] min-h-[300px] flex items-center justify-center p-0">
                        <div id="threejs-container" class="w-full h-full absolute inset-0 cursor-crosshair"></div>
                        <div class="absolute top-6 left-6 flex gap-4 z-30 pointer-events-none">
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-primary/80" id="hud_planet_name">Marte</span>
                                <span id="hud_g" class="text-xl font-mono font-bold text-white">3.72<span class="text-xs ml-1 text-slate-400">m/s²</span></span>
                            </div>
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-accent/80">Peso Calculado</span>
                                <span id="hud_p" class="text-xl font-mono font-bold text-white">297.6<span class="text-xs ml-1 text-slate-400">N</span></span>
                            </div>
                        </div>
                        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 z-30">
                            <button id="btn_simular" class="group relative flex items-center justify-center px-10 py-3 bg-primary text-white font-bold rounded-2xl shadow-2xl hover:scale-105 active:scale-95 transition-all outline-none border border-white/20">
                                <div class="absolute -inset-1 bg-primary blur opacity-40 group-hover:opacity-70 transition"></div>
                                <span class="relative flex items-center gap-2 shadow-sm text-lg"><span class="material-symbols-outlined text-2xl">download</span> SOLTAR OBJETO</span>
                            </button>
                        </div>
                        <div class="absolute top-6 right-6 z-30">
                            <button id="btn_reset_ext" class="size-10 rounded-xl bg-white/10 hover:bg-white/20 backdrop-blur border border-white/20 flex items-center justify-center text-white transition-all shadow-lg outline-none">
                                <span class="material-symbols-outlined text-xl">refresh</span>
                            </button>
                        </div>
                    </div>
                </section>
            </div>
            <footer class="mt-20 py-8 border-t border-slate-200 dark:border-slate-800 flex justify-between items-center gap-4"><div class="flex items-center gap-4 text-slate-400 text-sm"><span>&copy; 2024 Fisica Interactiva</span></div><div class="flex gap-4"><div class="flex items-center gap-2 px-3 py-1 bg-slate-100 dark:bg-slate-800 rounded-full text-[10px] font-bold text-slate-500"><span class="size-2 bg-green-500 rounded-full"></span> ENGINE V2.4 ONLINE</div></div></footer>
        </main>
    </div>

    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
        import { getFirestore, doc, updateDoc, increment } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-firestore.js";
        const firebaseConfig = { apiKey: "AIzaSyBD3-ZnbczYZOuDm7e9OHLP6Xg68sdZ1so", authDomain: "logicplay-e775c.firebaseapp.com", projectId: "logicplay-e775c", storageBucket: "logicplay-e775c.firebasestorage.app", messagingSenderId: "11226997472", appId: "1:11226997472:web:836d7d87f4f6a01987e685" };
        const app = initializeApp(firebaseConfig); const db = getFirestore(app);
        window.savePointsFisica = async function(pts) { const uid = localStorage.getItem('logicplay_uid'); if(uid) { try { await updateDoc(doc(db, "users", uid), { points: increment(pts), puntos_fisica: increment(pts), racha_fisica: increment(1), streak: increment(1) }); } catch(e) { console.error(e); } } };
    </script>

    <script type="module">
        import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js';
        let scene, camera, renderer, sphere, ground;
        let simRunning = false, sphereVelY = 0, missionWon = false;

        const PLANETS = { 'Marte': 0xc0392b, 'Tierra': 0x2980b9, 'Luna': 0x7f8c8d, 'Jupiter': 0xd35400, 'Venus': 0xe67e22 };

        const sliderM = document.getElementById('slider_m');
        const selectP = document.getElementById('select_planet');
        const valM = document.getElementById('val_m_display');
        const valPlanet = document.getElementById('val_planet_display');
        const formulaEl = document.getElementById('katex-formula');
        const hudG = document.getElementById('hud_g');
        const hudP = document.getElementById('hud_p');
        const hudName = document.getElementById('hud_planet_name');
        const btnSim = document.getElementById('btn_simular');
        const btnReset = document.getElementById('btn_reset_ext');
        const btnCheck = document.getElementById('btn_check');
        const inputP = document.getElementById('input_p');
        const fbMsg = document.getElementById('feedback_msg');
        const fbText = document.getElementById('feedback_text');

        function getParams() {
            const m = parseFloat(sliderM.value);
            const g = parseFloat(selectP.value);
            const name = selectP.options[selectP.selectedIndex].dataset.name;
            return { m, g, P: m * g, name };
        }

        function updateHUD() {
            const { m, g, P, name } = getParams();
            valM.innerText = m;
            valPlanet.innerText = name;
            hudName.innerText = name;
            hudG.innerHTML = g + '<span class="text-xs ml-1 text-slate-400">m/s²</span>';
            hudP.innerHTML = P.toFixed(1) + '<span class="text-xs ml-1 text-slate-400">N</span>';
            if (window.katex) {
                katex.render(`P = m \\cdot g = ${m} \\times ${g} = ${P.toFixed(1)}\\,\\text{N}`, formulaEl, { throwOnError: false, displayMode: true });
            }
            // Update sphere scale based on mass
            if (sphere) {
                const s = 0.5 + (m / 200) * 1.5;
                sphere.scale.set(s, s, s);
            }
            // Update ground color based on planet
            if (ground) {
                const color = PLANETS[name] || 0x1e293b;
                ground.material.color.setHex(color);
            }
        }

        sliderM.addEventListener('input', updateHUD);
        selectP.addEventListener('change', () => { updateHUD(); resetSim(); });

        function init3D() {
            const container = document.getElementById('threejs-container');
            const w = container.clientWidth, h = container.clientHeight;
            scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x0f172a, 0.015);
            camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 500);
            camera.position.set(0, 5, 10);
            camera.lookAt(0, 3, 0);
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(w, h); renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.5));
            const dir = new THREE.DirectionalLight(0xffffff, 1);
            dir.position.set(15, 30, 15); dir.castShadow = true;
            scene.add(dir);

            // Ground
            ground = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), new THREE.MeshStandardMaterial({ color: 0xc0392b, roughness: 0.8 }));
            ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true;
            scene.add(ground);
            scene.add(new THREE.GridHelper(20, 20, 0xffffff, 0x555555));

            // Sphere (astronaut object)
            sphere = new THREE.Mesh(
                new THREE.SphereGeometry(1, 32, 32),
                new THREE.MeshStandardMaterial({ color: 0x4f46e5, metalness: 0.4, roughness: 0.2 })
            );
            sphere.position.y = 8; sphere.castShadow = true;
            scene.add(sphere);

            // Scale platform
            const platGeo = new THREE.BoxGeometry(3, 0.3, 3);
            const platMat = new THREE.MeshStandardMaterial({ color: 0x22c55e, metalness: 0.5 });
            const platform = new THREE.Mesh(platGeo, platMat);
            platform.position.y = 0.15; platform.receiveShadow = true;
            scene.add(platform);

            updateHUD();
            renderLoop();
        }

        function resetSim() {
            simRunning = false; sphereVelY = 0;
            sphere.position.y = 8;
            fbMsg.style.opacity = '0';
            missionWon = false;
        }

        function renderLoop() {
            requestAnimationFrame(renderLoop);
            if (simRunning && sphere.position.y > 1.2) {
                const { g } = getParams();
                sphereVelY += g * 0.002;
                sphere.position.y -= sphereVelY * 0.05;
                if (sphere.position.y <= 1.2) {
                    sphere.position.y = 1.2;
                    simRunning = false;
                }
            }
            camera.position.y = 5 + Math.sin(Date.now() * 0.001) * 0.1;
            renderer.render(scene, camera);
        }

        btnSim.addEventListener('click', () => { if (!simRunning) { simRunning = true; sphereVelY = 0; sphere.position.y = 8; } });
        btnReset.addEventListener('click', resetSim);

        btnCheck.addEventListener('click', () => {
            const { P } = getParams();
            const userVal = parseFloat(inputP.value);
            fbMsg.style.opacity = '1';
            if (isNaN(userVal) || userVal <= 0) {
                fbText.textContent = 'Ingresa un valor valido.';
                fbMsg.className = 'mt-4 flex items-center justify-center gap-2 text-red-600 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-200 dark:border-red-800 transition-all';
                return;
            }
            if (Math.abs(userVal - P) < 2) {
                fbText.textContent = '¡Correcto! P = ' + P.toFixed(1) + ' N. +100 puntos!';
                fbMsg.className = 'mt-4 flex items-center justify-center gap-2 text-green-600 bg-green-50 dark:bg-green-900/20 p-3 rounded-lg border border-green-200 dark:border-green-800 transition-all';
                if (!missionWon) { missionWon = true; if (window.savePointsFisica) window.savePointsFisica(100); }
            } else {
                fbText.textContent = 'Incorrecto. Recuerda: P = m × g.';
                fbMsg.className = 'mt-4 flex items-center justify-center gap-2 text-accent bg-accent/5 p-3 rounded-lg border border-accent/20 transition-all';
            }
        });

        window.addEventListener('resize', () => {
            const c = document.getElementById('threejs-container');
            camera.aspect = c.clientWidth / c.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(c.clientWidth, c.clientHeight);
        });

        init3D();
    </script>
'''

head_end = html.find('</head>')
head_section = html[:head_end + len('</head>')]
faraday_start = html.find('<div id="faraday-chat-container"')
tail_section = html[faraday_start:]
new_html = head_section + '\n\n' + NEW_BODY + '\n\n    ' + tail_section

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f"✅ Peso y Masa 3D simulator built successfully in {FILE}")
