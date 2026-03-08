document.addEventListener('DOMContentLoaded', () => {
    const fraseText = document.querySelector('#frase-sugerida-text');
    const playButton = document.querySelector('#frase-play-button');

    if (!fraseText || !playButton) return;

    const audio = new SpeechSynthesisUtterance();

    // Desbloquear síntesis en iOS
    document.addEventListener('click', () => {
        if (!window.speechSynthesis.speaking && !window.speechSynthesis.pending) {
            const unlock = new SpeechSynthesisUtterance('');
            window.speechSynthesis.speak(unlock);
            window.speechSynthesis.cancel();
        }
    }, { once: true });

    window.speechSynthesis.onvoiceschanged = () => {
        const voices = window.speechSynthesis.getVoices();
        const spanishVoices = voices.filter(voice => /es/i.test(voice.lang));
        audio.voice = spanishVoices[0];
        audio.lang = spanishVoices[0]?.lang || 'es-ES';
    };

    // Forzar carga en Safari
    if (speechSynthesis.getVoices().length > 0) {
        window.speechSynthesis.onvoiceschanged();
    }

    audio.addEventListener('end', () => {
        playButton.classList.replace('btn-danger', 'btn-warning');
        playButton.innerHTML = `<span><i class="bi bi-ear me-2"></i></span><span>Escuchar</span>`;
    });

    playButton.addEventListener('click', () => {
        audio.text = fraseText.textContent;
        if (window.speechSynthesis.speaking) {
            playButton.classList.replace('btn-danger', 'btn-warning');
            playButton.innerHTML = `<span><i class="bi bi-ear me-2"></i></span><span>Escuchar</span>`;
            window.speechSynthesis.cancel();
        } else {
            playButton.classList.replace('btn-warning', 'btn-danger');
            playButton.innerHTML = `<span><i class="bi bi-stop me-2"></i></span><span>Parar</span>`;
            window.speechSynthesis.speak(audio);
        }
    });
});