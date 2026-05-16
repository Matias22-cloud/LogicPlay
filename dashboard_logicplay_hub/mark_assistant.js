import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import { getFirestore, doc, getDoc, collection, query, where, getDocs } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";
import { GoogleGenAI } from 'https://esm.run/@google/genai';

// --- CONFIGURACIÓN DE FIREBASE ---
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
const auth = getAuth(app);

// --- CONFIGURACIÓN DE GEMINI ---
const ai = new GoogleGenAI({
    apiKey: atob('QUl6YVN5RDM4S1VCbHNxV2xGejRBSXJyYU83Y0lyakFuMjBGd0pN'),
});

const geminiConfig = {
    systemInstruction: [{
        text: "Eres Mark, el amable y súper rápido asistente virtual universal de LogicPlay. Tu misión es ayudar al estudiante de Bachillerato en todo lo que necesite, ya sea navegación de la plataforma, explicación de conceptos de Ciencias o motivación. Debes dar respuestas cortas, precisas y sin mucho texto ya que tus respuestas son dictadas por voz. IMPORTANTE: No uses asteriscos, negritas ni formato especial complejo porque el motor de voz lo leerá literal. Habla directo y claro."
    }],
};
const model = 'gemini-1.5-flash';

// --- ELEMENTOS DE DOM ---
const widgetHTML = `
<!-- Botón Pestaña Cerrada -->
<div id="mark-widget-btn" class="fixed bottom-6 right-6 z-[60] bg-white border-2 border-primary text-primary px-4 py-2 font-bold text-sm shadow-xl rounded-xl flex items-center justify-center gap-2 cursor-pointer hover:-translate-y-1 hover:shadow-2xl transition-all select-none">
    <span class="text-xl">🤖</span>
    <span>Presiona Shift para hablar con Mark</span>
</div>

<!-- Panel de Chat -->
<div id="mark-chat-panel" class="fixed bottom-20 right-6 z-[60] w-80 md:w-96 bg-white border border-primary/20 rounded-2xl shadow-2xl flex flex-col hidden transform origin-bottom-right transition-all">
    <!-- Header -->
    <div class="bg-primary text-white p-4 rounded-t-2xl flex flex-col gap-1 items-start relative select-none">
        <h3 class="font-bold text-base flex items-center gap-2">🤖 Mark <span class="bg-blue-400 text-blue-900 text-[10px] uppercase font-black px-1.5 py-0.5 rounded ml-1">LogicPlay AI</span></h3>
        <p class="text-[11px] text-white/80 leading-snug">Mantén presionado <strong class="text-white">Shift</strong> para hablar. Presiona <strong class="text-white">Esc</strong> para cerrar.</p>
        <div id="mark-recording-badge" class="absolute top-4 right-4 flex items-center gap-1 bg-red-500 text-white text-[10px] font-bold px-2 py-1 rounded-full animate-pulse transition-opacity opacity-0">
            <span class="material-symbols-outlined text-[12px]">mic</span> Escuchando
        </div>
    </div>
    
    <!-- Mensajes -->
    <div id="mark-messages" class="h-80 overflow-y-auto p-4 flex flex-col gap-3 bg-slate-50/50 scrollbar-thin">
        <!-- Saludo inicial se inyectará aquí -->
    </div>

    <!-- Indicadores -->
    <div class="p-3 border-t border-slate-100 text-center flex flex-col justify-center items-center">
        <p id="mark-listening-status" class="text-xs text-slate-400 font-medium">Pulsa Shift ⬆ para hablar</p>
    </div>
</div>
`;

// Inyectar al body
document.body.insertAdjacentHTML('beforeend', widgetHTML);

const btnMark = document.getElementById('mark-widget-btn');
const panelMark = document.getElementById('mark-chat-panel');
const statusMark = document.getElementById('mark-listening-status');
const badgeRecording = document.getElementById('mark-recording-badge');
const messagesContainer = document.getElementById('mark-messages');

let isPanelOpen = false;
let isGreetingDone = false;
let isRecording = false;
let isProcessing = false;

// --- SPEECH RECOGNITION (Walkie Talkie) ---
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
}

// --- TEXT TO SPEECH ---
const synth = window.speechSynthesis;

function speak(text) {
    if (synth.speaking) synth.cancel();

    // Limpiamos formato markdown simple de Gemini para lectura de voz limpia
    const cleanText = text.replace(/\*\*/g, '').replace(/\*/g, '');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'es-ES';
    utterance.rate = 1.05;

    // Intentar buscar voz femenina o agradable de Google
    const voices = synth.getVoices();
    const esVoice = voices.find(v => v.lang.includes('es') && v.name.includes('Google')) || voices.find(v => v.lang.includes('es'));
    if (esVoice) utterance.voice = esVoice;

    synth.speak(utterance);
}

// --- UI HELPERS ---
function addMessageHTML(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `flex gap-2 w-full ${isUser ? 'justify-end' : ''} mb-2`;

    const bubbleClass = isUser
        ? 'bg-[#E3E8FC] text-slate-800 p-3 rounded-2xl rounded-tr-none text-sm shadow-sm max-w-[85%] border border-primary/10 font-medium'
        : 'bg-white border border-slate-100 p-3 rounded-2xl rounded-tl-none text-sm text-slate-700 shadow-sm max-w-[85%] font-medium';

    let contentHTML = '';

    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');

    if (!isUser) {
        contentHTML = `
            <div class="size-7 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-sm shadow-inner">🤖</div>
            <div class="${bubbleClass}">${formattedText}</div>
        `;
    } else {
        contentHTML = `<div class="${bubbleClass}">${formattedText}</div>`;
    }

    msgDiv.innerHTML = contentHTML;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return msgDiv;
}

// --- LOGICA PRINCIPAL ---
async function fetchUserContext() {
    const uid = localStorage.getItem('logicplay_uid');
    const role = localStorage.getItem('logicplay_role') || 'estudiante';
    const rawName = localStorage.getItem('logicplay_user_name') || 'Estudiante';
    const firstName = rawName.split(' ')[0];

    let totalStreak = 0;
    let notifsCount = 0;

    if (uid && role === 'estudiante') {
        try {
            // Racha
            const userRef = doc(db, "users", uid);
            const userSnap = await getDoc(userRef);
            if (userSnap.exists()) {
                const data = userSnap.data();
                // Racha General o Máxima
                totalStreak = data.streak || Math.max(data.racha_fisica || 0, data.racha_quimica || 0, data.racha_matematicas || 0);
            }

            // Notificaciones no leídas
            const notifQuery = query(collection(db, "notificaciones")); // Idealmente donde id_usuario == uid u otra lógica para estudiante
            const notifSnap = await getDocs(notifQuery);
            notifSnap.forEach(doc => {
                if (!doc.data().leido) notifsCount++;
            });
        } catch (e) {
            console.error("Mark couldn't fetch data", e);
        }
    }

    return { firstName, totalStreak, notifsCount };
}

async function doInitialGreeting() {
    if (isGreetingDone) return;
    isGreetingDone = true;

    // Loading status
    const loader = addMessageHTML("Un momento...", false);

    const context = await fetchUserContext();

    let greetingText = `¡Hola ${context.firstName}! Soy Mark, tu asistente de LogicPlay. `;
    if (context.totalStreak > 0) {
        greetingText += `Llevas ${context.totalStreak} días de racha, ¡no la pierdas! `;
    }
    if (context.notifsCount > 0) {
        greetingText += `Tienes ${context.notifsCount} notificaciones nuevas. `;
    }
    greetingText += "¿En qué te puedo ayudar hoy?";

    // Reemplazar loader
    loader.innerHTML = `<div class="size-7 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-sm shadow-inner">🤖</div>
    <div class="bg-white border border-slate-100 p-3 rounded-2xl rounded-tl-none text-sm text-slate-700 shadow-sm max-w-[85%] font-medium">${greetingText}</div>`;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    speak(greetingText);
}

function openPanel() {
    if (isPanelOpen) return;
    isPanelOpen = true;
    panelMark.classList.remove('hidden');
    // Forzar redibujado de botones
    setTimeout(() => {
        doInitialGreeting();
    }, 150);
}

function closePanel() {
    if (!isPanelOpen) return;
    isPanelOpen = false;
    panelMark.classList.add('hidden');
    if (synth.speaking) synth.cancel();
}

// Toggle on click just in case
btnMark.addEventListener('click', () => {
    if (isPanelOpen) closePanel();
    else openPanel();
});


// --- WALKIE TALKIE LOGIC ---
let finalTranscript = '';

if (recognition) {
    recognition.onstart = () => {
        isRecording = true;
        badgeRecording.classList.remove('opacity-0');
        statusMark.textContent = "Te estoy escuchando...";
        synth.cancel(); // Stop talking if we start speaking
    };
    recognition.onresult = (e) => {
        finalTranscript = e.results[0][0].transcript;
    };
    recognition.onerror = (e) => {
        console.error('Speech recognition error', e.error);
        if (e.error !== "aborted") {
            statusMark.textContent = "Hubo un error al escucharte. Intenta de nuevo.";
        }
    };
    recognition.onend = () => {
        isRecording = false;
        badgeRecording.classList.add('opacity-0');
        statusMark.textContent = "Procesando...";

        if (finalTranscript.trim() && isPanelOpen) {
            processUserQuery(finalTranscript);
        } else {
            statusMark.textContent = "Pulsa Shift ⬆ para hablar";
        }
        finalTranscript = ''; // reset
    };
} else {
    statusMark.innerHTML = '<span class="text-red-500">Tu navegador no soporta micrófono vía Web Speech API.</span>';
}

async function processUserQuery(text) {
    if (isProcessing) return;
    isProcessing = true;
    addMessageHTML(text, true);

    // Loading indicator
    const loader = addMessageHTML("Pensando...", false);

    try {
        const response = await ai.models.generateContent({
            model,
            config: geminiConfig,
            contents: [{ role: 'user', parts: [{ text }] }],
        });

        const reply = response.text;

        loader.innerHTML = `<div class="size-7 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-sm shadow-inner">🤖</div>
        <div class="bg-white border border-slate-100 p-3 rounded-2xl rounded-tl-none text-sm text-slate-700 shadow-sm max-w-[85%] font-medium">${reply.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')}</div>`;
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        speak(reply);
    } catch (err) {
        console.error("Mark Gemini Error", err);
        loader.innerHTML = `<div class="size-7 shrink-0 rounded-full bg-primary/10 flex items-center justify-center text-sm shadow-inner">🤖</div>
        <div class="bg-red-50 border border-red-200 text-red-600 p-3 rounded-2xl rounded-tl-none text-sm shadow-sm max-w-[85%] font-medium">Mmm, parece que hubo un fallo de sistema. ¿Me repites?</div>`;
    } finally {
        isProcessing = false;
        if (!isRecording) statusMark.textContent = "Pulsa Shift ⬆ para hablar";
    }
}

// --- GLOBAL KEYBOARD LISTENERS ---
document.addEventListener('keydown', (e) => {
    // Escape to close
    if (e.key === 'Escape' && isPanelOpen) {
        closePanel();
        return;
    }

    // Shift to hold talk
    // No trigger if focus is on form inputs (like faraday-input or search, etc.)
    if (e.key === 'Shift') {
        const activeTag = document.activeElement.tagName;
        if (activeTag === 'INPUT' || activeTag === 'TEXTAREA') return;

        openPanel(); // Ensure it's open
        if (recognition && !isRecording) {
            try {
                recognition.start();
            } catch (err) {
                // If it's already started, ignore
            }
        }
    }
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'Shift') {
        if (recognition && isRecording) {
            recognition.stop();
        }
    }
});
