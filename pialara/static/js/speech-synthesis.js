const syllabusText = document.querySelector('#syllabus-text');
const playButton = document.querySelector('#play-button');

const audio = new SpeechSynthesisUtterance();

audio.addEventListener('end', () => {
  playButton.classList.replace('btn-danger', 'btn-warning');
  playButton.innerHTML = `<span>
      <span><i class="bi bi-ear me-2"></i></span>
      <span>Escuchar frase</span>
    </span>`;
});

playButton.addEventListener('click', () => {
  audio.text = syllabusText.value || syllabusText.textContent;

  if (window.speechSynthesis.speaking) {
    playButton.classList.replace('btn-danger', 'btn-warning');
    playButton.innerHTML = `<span>
      <span><i class="bi bi-ear me-2"></i></span>
      <span>Escuchar frase</span>
    </span>`;
    window.speechSynthesis.cancel();
  } else {
    playButton.classList.replace('btn-warning', 'btn-danger');
    playButton.innerHTML = `<span>
      <span><i class="bi bi-stop me-2"></i></span>
      <span>Dejar de escuchar</span>
    </span>`;
    window.speechSynthesis.speak(audio);
  }
});
