#!/usr/bin/env python3
"""Build 3D Planos Inclinados simulator."""
import re, os

FILE = os.path.join("Fisica_Todos los documentos", "f_sica_planos_inclinados", "practica.html")

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ── NEW BODY CONTENT ─────────────────────────────────────────────
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
                        <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 dark:white tracking-tight">Planos Inclinados</h1>
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
                    <div class="absolute top-0 right-0 p-4 opacity-5"><span class="material-symbols-outlined text-9xl">terrain</span></div>
                    <div class="flex items-center gap-3 mb-4"><span class="material-symbols-outlined text-primary fill-1">assignment</span><h3 class="text-xl font-bold text-slate-800 dark:text-slate-200">Simulador 3D: Plano Inclinado</h3></div>
                    <div class="relative z-10">
                        <p class="text-lg text-slate-600 dark:text-slate-400 leading-relaxed font-light">
                            Ajusta la <b>masa</b> y el <b>angulo</b> del plano inclinado. La caja se deslizara por el plano y deberas calcular la componente <b>Px</b> (paralela al plano). Ingresa el valor correcto de Px para ganar <span class="font-bold text-primary">100 puntos</span>.
                        </p>
                    </div>
                </section>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 glass-panel p-6 rounded-3xl">
                        <div class="flex items-center justify-between mb-6">
                            <h4 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Panel Interactivo 3D</h4>
                            <span class="text-[10px] px-2 py-1 bg-primary/20 text-primary rounded-md font-bold">Px = m·g·sen(θ)</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-6">
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">fitness_center</span> Masa (m)</span>
                                    <span class="text-slate-900 dark:text-white text-base"><span id="val_m_display">30</span> kg</span>
                                </label>
                                <input id="slider_m" type="range" min="5" max="100" step="5" value="30" class="w-full h-2 bg-slate-200 dark:bg-slate-700 appearance-none rounded-full cursor-pointer accent-primary">
                            </div>
                            <div class="flex flex-col gap-3 group">
                                <label class="flex items-center justify-between text-xs font-bold text-slate-500 group-hover:text-primary transition-colors">
                                    <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm">rotate_right</span> Angulo (θ)</span>
                                    <span class="text-slate-900 dark:text-white text-base"><span id="val_a_display">30</span>°</span>
                                </label>
                                <input id="slider_a" type="range" min="10" max="60" step="5" value="30" class="w-full h-2 bg-slate-200 dark:bg-slate-700 appearance-none rounded-full cursor-pointer accent-accent">
                            </div>
                        </div>
                        <div class="bg-slate-50 dark:bg-slate-800/50 rounded-2xl p-4 flex flex-col items-center justify-center border border-slate-200 dark:border-slate-700 shadow-inner">
                            <span class="text-[10px] font-bold text-slate-400 mb-2 uppercase tracking-widest">Ecuacion en Tiempo Real</span>
                            <div id="katex-formula" class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white my-1"></div>
                        </div>
                        <div class="mt-4 flex items-center gap-4">
                            <div class="flex-1 relative flex items-center rounded-xl overflow-hidden bg-white dark:bg-slate-800/80 border-2 border-primary/40 focus-within:border-primary shadow-sm">
                                <input id="input_px" class="w-full bg-transparent border-none text-sm font-bold px-3 py-2.5 focus:ring-0 text-primary" placeholder="Ingresa Px..." type="number" step="0.1">
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
                        <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed italic">"Primero calcula el peso P = m × g, luego la componente paralela <strong>Px = P × sen(θ)</strong>. Recuerda que sen(30°) = 0.5."</p>
                    </div>
                </div>

                <section class="relative group mt-2">
                    <div class="absolute -inset-1 bg-gradient-to-r from-primary to-accent rounded-[2.5rem] blur opacity-20 group-hover:opacity-30 transition duration-1000"></div>
                    <div class="relative glass-panel rounded-[2rem] overflow-hidden bg-slate-900 aspect-[21/9] min-h-[300px] flex items-center justify-center p-0">
                        <div id="threejs-container" class="w-full h-full absolute inset-0 cursor-crosshair"></div>
                        <div class="absolute top-6 left-6 flex gap-4 z-30 pointer-events-none">
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-primary/80">Peso (P)</span>
                                <span id="hud_p" class="text-xl font-mono font-bold text-white">294.3<span class="text-xs ml-1 text-slate-400">N</span></span>
                            </div>
                            <div class="glass-panel bg-black/50 border-white/10 px-4 py-2 rounded-xl backdrop-blur-md">
                                <span class="block text-[10px] uppercase font-bold text-accent/80">Px (paralela)</span>
                                <span id="hud_px" class="text-xl font-mono font-bold text-white">147.2<span class="text-xs ml-1 text-slate-400">N</span></span>
                            </div>
                        </div>
                        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 z-30 flex gap-4">
                            <button id="btn_simular" class="group relative flex items-center justify-center px-10 py-3 bg-primary text-white font-bold rounded-2xl shadow-2xl hover:scale-105 active:scale-95 transition-all outline-none border border-white/20">
                                <div class="absolute -inset-1 bg-primary blur opacity-40 group-hover:opacity-70 transition"></div>
                                <span class="relative flex items-center gap-2 shadow-sm text-lg"><span class="material-symbols-outlined text-2xl">south_east</span> SOLTAR CAJA</span>
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
        window.savePointsFisica = async function(pts) { const uid = localStorage.getItem('logicplay_uid'); if(uid) { try { await updateDoc(doc(db, "users", uid), { points: increment(pts), puntos_fisica: increment(pts), racha_fisica: increment(1), streak: increment(1) }); console.log("Puntos guardados!"); } catch(e) { console.error(e); } } };
    </script>

    <!-- Three.js 3D Plano Inclinado Simulator -->
    <script type="module">
        import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js';

        let scene, camera, renderer, box, rampMesh, targetFlag;
        let simRunning = false, animId, boxPos = 0, missionWon = false;

        const sliderM = document.getElementById('slider_m');
        const sliderA = document.getElementById('slider_a');
        const valM = document.getElementById('val_m_display');
        const valA = document.getElementById('val_a_display');
        const formulaEl = document.getElementById('katex-formula');
        const hudP = document.getElementById('hud_p');
        const hudPx = document.getElementById('hud_px');
        const btnSim = document.getElementById('btn_simular');
        const btnReset = document.getElementById('btn_reset_ext');
        const btnCheck = document.getElementById('btn_check');
        const inputPx = document.getElementById('input_px');
        const fbMsg = document.getElementById('feedback_msg');
        const fbText = document.getElementById('feedback_text');

        const G = 9.81;

        function getParams() {
            const m = parseFloat(sliderM.value);
            const a = parseFloat(sliderA.value);
            const aRad = a * Math.PI / 180;
            const P = m * G;
            const Px = P * Math.sin(aRad);
            const Py = P * Math.cos(aRad);
            return { m, a, aRad, P, Px, Py };
        }

        function updateHUD() {
            const { m, a, P, Px } = getParams();
            valM.innerText = m;
            valA.innerText = a;
            hudP.innerHTML = P.toFixed(1) + '<span class="text-xs ml-1 text-slate-400">N</span>';
            hudPx.innerHTML = Px.toFixed(1) + '<span class="text-xs ml-1 text-slate-400">N</span>';
            if (window.katex) {
                katex.render(`P_x = m \\cdot g \\cdot \\sin(\\theta) = ${m} \\times ${G} \\times \\sin(${a}°) = ${Px.toFixed(1)}\\,\\text{N}`, formulaEl, { throwOnError: false, displayMode: true });
            }
            updateRamp();
        }

        sliderM.addEventListener('input', updateHUD);
        sliderA.addEventListener('input', updateHUD);

        function init3D() {
            const container = document.getElementById('threejs-container');
            const w = container.clientWidth, h = container.clientHeight;
            scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x0f172a, 0.012);
            camera = new THREE.PerspectiveCamera(55, w / h, 0.1, 500);
            camera.position.set(8, 6, 10);
            camera.lookAt(0, 2, -2);
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(w, h);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            scene.add(new THREE.AmbientLight(0xffffff, 0.4));
            const dir = new THREE.DirectionalLight(0xffffff, 1);
            dir.position.set(20, 40, 20); dir.castShadow = true;
            dir.shadow.mapSize.set(1024, 1024);
            scene.add(dir);

            // Floor
            const floor = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 }));
            floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true;
            scene.add(floor);
            scene.add(new THREE.GridHelper(20, 20, 0x4f46e5, 0x334155));

            // Ramp
            const rampGeo = new THREE.BoxGeometry(4, 0.3, 10);
            const rampMat = new THREE.MeshStandardMaterial({ color: 0x6366f1, metalness: 0.2, roughness: 0.5 });
            rampMesh = new THREE.Mesh(rampGeo, rampMat);
            rampMesh.castShadow = true; rampMesh.receiveShadow = true;
            scene.add(rampMesh);

            // Box
            const boxGeo = new THREE.BoxGeometry(1.2, 1.2, 1.2);
            const boxMat = new THREE.MeshStandardMaterial({ color: 0xf43f5e, metalness: 0.3, roughness: 0.3 });
            box = new THREE.Mesh(boxGeo, boxMat);
            box.castShadow = true;
            scene.add(box);

            // Target flag at bottom
            const poleGeo = new THREE.CylinderGeometry(0.05, 0.05, 2);
            const poleMat = new THREE.MeshStandardMaterial({ color: 0x22c55e });
            targetFlag = new THREE.Group();
            const pole = new THREE.Mesh(poleGeo, poleMat);
            pole.position.y = 1;
            targetFlag.add(pole);
            const flagGeo = new THREE.PlaneGeometry(0.8, 0.5);
            const flagMat = new THREE.MeshStandardMaterial({ color: 0x22c55e, side: THREE.DoubleSide });
            const flag = new THREE.Mesh(flagGeo, flagMat);
            flag.position.set(0.4, 1.8, 0);
            targetFlag.add(flag);
            scene.add(targetFlag);

            updateRamp();
            renderLoop();
        }

        function updateRamp() {
            const { aRad } = getParams();
            const rampLen = 10;
            rampMesh.rotation.x = -aRad;
            rampMesh.position.set(0, Math.sin(aRad) * rampLen / 2 + 0.15, -Math.cos(aRad) * rampLen / 2);

            // Reset box to top
            if (!simRunning) {
                boxPos = 0;
                const topX = 0;
                const topY = Math.sin(aRad) * (rampLen / 2 - 1) + 0.15 + 0.75;
                const topZ = -Math.cos(aRad) * (rampLen / 2 - 1);
                box.position.set(topX, topY, topZ);
                box.rotation.x = -aRad;
            }

            // Target at bottom of ramp
            targetFlag.position.set(0, 0, Math.cos(aRad) * rampLen / 2 + 0.5);
        }

        function renderLoop() {
            animId = requestAnimationFrame(renderLoop);
            if (simRunning) {
                const { aRad, m } = getParams();
                const acc = G * Math.sin(aRad); // acceleration along ramp
                const rampLen = 8; // travel length
                boxPos += acc * 0.008; // scaled time step
                if (boxPos >= rampLen) {
                    boxPos = rampLen;
                    simRunning = false;
                }
                const startOffset = 4;
                const along = startOffset - boxPos;
                box.position.y = Math.sin(aRad) * along + 0.15 + 0.75;
                box.position.z = -Math.cos(aRad) * along;
                box.rotation.x = -aRad;
            }
            // Gentle camera bob
            camera.position.y = 6 + Math.sin(Date.now() * 0.001) * 0.15;
            renderer.render(scene, camera);
        }

        btnSim.addEventListener('click', () => {
            if (simRunning) return;
            simRunning = true;
            boxPos = 0;
        });

        btnReset.addEventListener('click', () => {
            simRunning = false;
            boxPos = 0;
            missionWon = false;
            fbMsg.style.opacity = '0';
            updateRamp();
        });

        btnCheck.addEventListener('click', () => {
            const { Px } = getParams();
            const userVal = parseFloat(inputPx.value);
            fbMsg.style.opacity = '1';
            if (isNaN(userVal) || userVal <= 0) {
                fbText.textContent = 'Ingresa un valor valido de Px.';
                fbMsg.className = 'mt-4 flex items-center justify-center gap-2 text-red-600 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg border border-red-200 dark:border-red-800 transition-all';
                return;
            }
            if (Math.abs(userVal - Px) < 2) {
                fbText.textContent = '¡Correcto! Px = ' + Px.toFixed(1) + ' N. +100 puntos!';
                fbMsg.className = 'mt-4 flex items-center justify-center gap-2 text-green-600 bg-green-50 dark:bg-green-900/20 p-3 rounded-lg border border-green-200 dark:border-green-800 transition-all';
                if (!missionWon) { missionWon = true; if (window.savePointsFisica) window.savePointsFisica(100); }
            } else {
                fbText.textContent = 'Incorrecto. Recuerda: Px = m × g × sen(θ). Intenta de nuevo.';
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
        setTimeout(updateHUD, 300);
    </script>
'''

# ── Replace from <body> to just before the Faraday chat ──
# Keep the <head> tag and everything from Faraday chat onwards
head_end = html.find('</head>')
head_section = html[:head_end + len('</head>')]

# Find the Faraday chat container and everything after it
faraday_start = html.find('<div id="faraday-chat-container"')
if faraday_start == -1:
    # Try alternate
    faraday_start = html.find('faraday-chat-container')
    faraday_start = html.rfind('<div', 0, faraday_start)

tail_section = html[faraday_start:]

new_html = head_section + '\n\n' + NEW_BODY + '\n\n    ' + tail_section

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"✅ Planos Inclinados 3D simulator built successfully in {FILE}")
