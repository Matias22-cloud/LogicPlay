#!/usr/bin/env python3
"""Build 3D Equilibrio de Fuerzas simulator - balance/tension forces."""
import os

FILE = os.path.join("Fisica_Todos los documentos", "f_sica_equilibrio_de_fuerzas", "practica.html")
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
                        <span class="text-primary font-bold text-sm tracking-widest uppercase mb-2 block">Modulo 02: Estatica</span>
                        <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 dark:white tracking-tight">Equilibrio de Fuerzas</h1>
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
                    <div class="absolute top-0 right-0 p-4 opacity-5"><span class="material-symbols-outlined text-9xl">balance</span></div>
                    <div class="flex items-center gap-3 mb-4"><span class="material-symbols-outlined text-primary fill-1">assignment</span><h3 class="text-xl font-bold text-slate-800 dark:text-slate-200">Simulador 3D: Equilibrio de Fuerzas</h3></div>
                    <div class="relative z-10">
                        <p class="text-lg text-slate-600 dark:text-slate-400 leading-relaxed font-light">
                            Una caja esta sobre una superficie horizontal. Ajusta la <b>masa</b> y la <b>fuerza aplicada</b>. La caja se movera solo si la fuerza supera la friccion maxima. Calcula el <b>coeficiente de friccion estatico (μs = F/N)</b> para ganar <span class="font-bold text-primary">100 puntos</span>.
                        </p>
                    </div>
                </section>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 glass-panel p-6 rounded-3xl">
                        <div class="flex items-center justify-between mb-6">
                            <h4 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Panel Interactivo 3D</h4>
                            <span class="text-[10px] px-2 py-1 bg-primary/20 text-primary rounded-md font-bold">μs = F / N</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-6">
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">fitness_center</span> Masa (m)</span>
                                    <span class="text-slate-900 dark:text-white text-base"><span id="val_m_display">10</span> kg</span>
                                </label>
                                <input id="slider_m" type="range" min="5" max="50" step="1" value="10" class="w-full h-2 bg-slate-200 dark:bg-slate-700 appearance-none rounded-full cursor-pointer accent-primary">
                            </div>
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">east</span> Fuerza Aplicada (F)</span>
                                    <span class="text-slate-900 dark:text-white text-base"><span id="val_f_display">10</span> N</span>
                                </label>
                                <input id="slider_f" type="range" min="1" max="200" step="1" value="10" class="w-full h-2 bg-slate-200 dark:bg-slate-700 appearance-none rounded-full cursor-pointer accent-accent">
                            </div>
                        </div>
                        <div class="bg-slate-50 dark:bg-slate-800/50 rounded-2xl p-4 flex flex-col items-center justify-center border border-slate-200 dark:border-slate-700 shadow-inner">
                            <span class="text-[10px] font-bold text-slate-400 mb-2 uppercase tracking-widest">Ecuacion en Tiempo Real</span>
                            <div id="katex-formula" class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white my-1"></div>
                        </div>
                        <div class="mt-4 flex items-center gap-4">
                            <div class="flex-1 relative flex items-center rounded-xl overflow-hidden bg-white dark:bg-slate-800/80 border-2 border-primary/40 focus-within:border-primary shadow-sm">
                                <input id="input_mu" class="w-full bg-transparent border-none text-sm font-bold px-3 py-2.5 focus:ring-0 text-primary" placeholder="Ingresa μs..." type="number" step="0.01">
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
                        <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed italic">"En equilibrio la sumatoria de fuerzas es cero. La Normal (N) es igual al Peso (m×g) en superficie horizontal. El coeficiente de friccion estatico es <strong>μs = F / N</strong>."</p>
                    </div>
                </div>

                <section class="relative group mt-2">
                    <div class="absolute -inset-1 bg-gradient-to-r from-primary to-accent rounded-[2.5rem] blur opacity-20 group-hover:opacity-30 transition duration-1000"></div>
                    <div class="relative glass-panel rounded-[2rem] overflow-hidden bg-slate-900 aspect-[21/9] min-h-[300px] flex items-center justify-center p-0">
                        <div id="threejs-container" class="w-full h-full absolute inset-0 cursor-crosshair"></div>
                        <div class="absolute top-6 left-6 flex gap-4 z-30 pointer-events-none">
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-primary/80">Normal (N)</span>
                                <span id="hud_n" class="text-xl font-mono font-bold text-white">98.1<span class="text-xs ml-1 text-slate-400">N</span></span>
                            </div>
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-accent/80">Estado</span>
                                <span id="hud_state" class="text-xl font-mono font-bold text-white">Reposo</span>
                            </div>
                        </div>
                        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 z-30">
                            <button id="btn_simular" class="group relative flex items-center justify-center px-10 py-3 bg-primary text-white font-bold rounded-2xl shadow-2xl hover:scale-105 active:scale-95 transition-all outline-none border border-white/20">
                                <div class="absolute -inset-1 bg-primary blur opacity-40 group-hover:opacity-70 transition"></div>
                                <span class="relative flex items-center gap-2 shadow-sm text-lg"><span class="material-symbols-outlined text-2xl">east</span> APLICAR FUERZA</span>
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
        let scene, camera, renderer, crate, arrowF, arrowN, arrowW;
        let simRunning = false, crateVelX = 0, missionWon = false;
        const G = 9.81, MU_THRESHOLD = 0.3;

        const sliderM = document.getElementById('slider_m');
        const sliderF = document.getElementById('slider_f');
        const valM = document.getElementById('val_m_display');
        const valF = document.getElementById('val_f_display');
        const formulaEl = document.getElementById('katex-formula');
        const hudN = document.getElementById('hud_n');
        const hudState = document.getElementById('hud_state');
        const btnSim = document.getElementById('btn_simular');
        const btnReset = document.getElementById('btn_reset_ext');
        const btnCheck = document.getElementById('btn_check');
        const inputMu = document.getElementById('input_mu');
        const fbMsg = document.getElementById('feedback_msg');
        const fbText = document.getElementById('feedback_text');

        function getParams() {
            const m = parseFloat(sliderM.value);
            const F = parseFloat(sliderF.value);
            const N = m * G;
            const mu = F / N;
            return { m, F, N, mu };
        }

        function updateHUD() {
            const { m, F, N, mu } = getParams();
            valM.innerText = m; valF.innerText = F;
            hudN.innerHTML = N.toFixed(1) + '<span class="text-xs ml-1 text-slate-400">N</span>';
            if (window.katex) {
                katex.render(`\\mu_s = \\frac{F}{N} = \\frac{${F}}{${N.toFixed(1)}} = ${mu.toFixed(3)}`, formulaEl, { throwOnError: false, displayMode: true });
            }
            // Update arrow length
            if (arrowF) {
                const scale = F / 50;
                arrowF.scale.set(scale, 1, 1);
            }
        }

        sliderM.addEventListener('input', updateHUD);
        sliderF.addEventListener('input', updateHUD);

        function init3D() {
            const container = document.getElementById('threejs-container');
            const w = container.clientWidth, h = container.clientHeight;
            scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x0f172a, 0.01);
            camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 500);
            camera.position.set(0, 5, 12);
            camera.lookAt(0, 1, 0);
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(w, h); renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.5));
            const dir = new THREE.DirectionalLight(0xffffff, 1);
            dir.position.set(15, 30, 15); dir.castShadow = true;
            scene.add(dir);

            // Floor
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 }));
            floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true;
            scene.add(floor);
            scene.add(new THREE.GridHelper(20, 20, 0x4f46e5, 0x334155));

            // Crate
            const crateGeo = new THREE.BoxGeometry(2, 2, 2);
            const crateMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.2, roughness: 0.5 });
            crate = new THREE.Mesh(crateGeo, crateMat);
            crate.position.set(0, 1, 0); crate.castShadow = true;
            scene.add(crate);

            // Force arrow (red, horizontal)
            const arrowGeo = new THREE.ConeGeometry(0.3, 1, 8);
            const arrowMat = new THREE.MeshStandardMaterial({ color: 0xf43f5e });
            arrowF = new THREE.Group();
            const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 3), arrowMat);
            shaft.rotation.z = -Math.PI / 2; shaft.position.x = 1.5;
            arrowF.add(shaft);
            const tip = new THREE.Mesh(arrowGeo, arrowMat);
            tip.rotation.z = -Math.PI / 2; tip.position.x = 3.2;
            arrowF.add(tip);
            arrowF.position.set(-3, 1, 0);
            scene.add(arrowF);

            // Weight arrow (blue, vertical down)
            const wGroup = new THREE.Group();
            const wShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2), new THREE.MeshStandardMaterial({ color: 0x3b82f6 }));
            wShaft.position.y = -1;
            wGroup.add(wShaft);
            const wTip = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.6, 8), new THREE.MeshStandardMaterial({ color: 0x3b82f6 }));
            wTip.position.y = -2.2; wTip.rotation.x = Math.PI;
            wGroup.add(wTip);
            wGroup.position.set(0, 2, 0);
            arrowW = wGroup;
            scene.add(wGroup);

            // Normal arrow (green, vertical up)
            const nGroup = new THREE.Group();
            const nShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2), new THREE.MeshStandardMaterial({ color: 0x22c55e }));
            nShaft.position.y = 1;
            nGroup.add(nShaft);
            const nTip = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.6, 8), new THREE.MeshStandardMaterial({ color: 0x22c55e }));
            nTip.position.y = 2.2;
            nGroup.add(nTip);
            nGroup.position.set(0, 2, 0);
            arrowN = nGroup;
            scene.add(nGroup);

            updateHUD();
            renderLoop();
        }

        function resetSim() {
            simRunning = false; crateVelX = 0;
            crate.position.set(0, 1, 0);
            arrowF.position.x = -3;
            hudState.textContent = 'Reposo';
            fbMsg.style.opacity = '0';
            missionWon = false;
        }

        function renderLoop() {
            requestAnimationFrame(renderLoop);
            if (simRunning) {
                const { m, F, N, mu } = getParams();
                const frictionMax = MU_THRESHOLD * N;
                if (F > frictionMax) {
                    const acc = (F - frictionMax) / m;
                    crateVelX += acc * 0.003;
                    crate.position.x += crateVelX * 0.05;
                    arrowF.position.x = crate.position.x - 3;
                    arrowW.position.x = crate.position.x;
                    arrowN.position.x = crate.position.x;
                    hudState.textContent = 'Movimiento';
                    hudState.style.color = '#f43f5e';
                    if (crate.position.x > 8) { simRunning = false; }
                } else {
                    hudState.textContent = 'Equilibrio ✓';
                    hudState.style.color = '#22c55e';
                    simRunning = false;
                }
            }
            camera.position.y = 5 + Math.sin(Date.now() * 0.001) * 0.08;
            renderer.render(scene, camera);
        }

        btnSim.addEventListener('click', () => { if (!simRunning) { resetSim(); simRunning = true; } });
        btnReset.addEventListener('click', resetSim);

        btnCheck.addEventListener('click', () => {
            const { mu } = getParams();
            const userVal = parseFloat(inputMu.value);
            fbMsg.style.opacity = '1';
            if (isNaN(userVal) || userVal < 0) {
                fbText.textContent = 'Ingresa un valor valido de μs.';
                fbMsg.className = 'mt-4 flex items-center justify-center gap-2 text-red-600 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-200 dark:border-red-800 transition-all';
                return;
            }
            if (Math.abs(userVal - mu) < 0.02) {
                fbText.textContent = '¡Correcto! μs = ' + mu.toFixed(3) + '. +100 puntos!';
                fbMsg.className = 'mt-4 flex items-center justify-center gap-2 text-green-600 bg-green-50 dark:bg-green-900/20 p-3 rounded-lg border border-green-200 dark:border-green-800 transition-all';
                if (!missionWon) { missionWon = true; if (window.savePointsFisica) window.savePointsFisica(100); }
            } else {
                fbText.textContent = 'Incorrecto. Recuerda: μs = F / N = F / (m×g).';
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
print(f"✅ Equilibrio de Fuerzas 3D simulator built successfully in {FILE}")
