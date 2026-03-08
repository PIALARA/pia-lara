/**
 * Centraliza la lógica de carga de frases aleatorias por ubicación
 * y la síntesis de voz asociada a las frases sugeridas.
 */

function cargarFraseAleatoria(location) {
    fetch(`/syllabus/frase-aleatoria?location=${encodeURIComponent(location)}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) return;
            
            // Actualización de texto
            const fraseText = document.getElementById('frase-sugerida-text');
            if (fraseText) fraseText.textContent = data.texto;
            
            // Actualización de etiquetas
            const tagsEl = document.getElementById('frase-sugerida-tags');
            if (tagsEl) tagsEl.textContent = 'Etiquetas: ' + (Array.isArray(data.tags) ? data.tags.join(', ') : data.tags);
            
            // Actualización de badge momento del día
            const badgeMomento = document.getElementById('momento-dia-badge');
            if (badgeMomento) {
                badgeMomento.textContent = data.momento_dia.charAt(0).toUpperCase() + data.momento_dia.slice(1);
            }
        })
        .catch(err => console.error('Error al cargar frase:', err));
}

// Lógica para el botón de escuchar (merging de frase-sugerida.js)
document.addEventListener('DOMContentLoaded', () => {
    const playButton = document.querySelector('#frase-play-button');
    const fraseText = document.querySelector('#frase-sugerida-text');

    if (!playButton || !fraseText) return;

    const synth = window.speechSynthesis;
    let utterance = new SpeechSynthesisUtterance();

    // Desbloquear síntesis en móviles
    document.addEventListener('click', () => {
        if (!synth.speaking && !synth.pending) {
            const unlock = new SpeechSynthesisUtterance('');
            synth.speak(unlock);
            synth.cancel();
        }
    }, { once: true });

    function loadVoice() {
        const voices = synth.getVoices();
        const spanishVoice = voices.find(v => /es-ES/i.test(v.lang)) || voices.find(v => /es/i.test(v.lang));
        if (spanishVoice) {
            utterance.voice = spanishVoice;
            utterance.lang = spanishVoice.lang;
        }
    }

    if (synth.onvoiceschanged !== undefined) {
        synth.onvoiceschanged = loadVoice;
    }
    loadVoice();

    utterance.onend = () => {
        playButton.classList.replace('btn-danger', 'btn-warning');
        playButton.innerHTML = `<span><i class="bi bi-ear me-2"></i></span><span>Escuchar</span>`;
    };

    playButton.addEventListener('click', () => {
        if (synth.speaking) {
            synth.cancel();
            // El evento onend se encargará de resetear el botón
        } else {
            utterance.text = fraseText.textContent;
            playButton.classList.replace('btn-warning', 'btn-danger');
            playButton.innerHTML = `<span><i class="bi bi-stop me-2"></i></span><span>Parar</span>`;
            synth.speak(utterance);
        }
    });
});
