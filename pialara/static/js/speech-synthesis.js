const syllabusText = document.querySelector('#syllabus-text');
const playButton = document.querySelector('#play-button');

const audio = new SpeechSynthesisUtterance();
audio.text = syllabusText.textContent;

audio.addEventListener('end', () => {
  playButton.classList.replace('btn-danger', 'btn-warning');
  playButton.innerHTML = '<i class="bi bi-ear me-2"></i>Escuchar frase';
});

playButton.addEventListener('click', () => {
  if (window.speechSynthesis.speaking) {
    playButton.classList.replace('btn-danger', 'btn-warning');
    playButton.innerHTML = '<i class="bi bi-ear me-2"></i>Escuchar frase';
    window.speechSynthesis.cancel();
  } else {
    playButton.classList.replace('btn-warning', 'btn-danger');
    playButton.innerHTML = '<i class="bi bi-stop me-2"></i>Dejar de escuchar';
    window.speechSynthesis.speak(audio);
  }
});
