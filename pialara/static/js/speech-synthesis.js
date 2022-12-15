const syllabusText = document.querySelector('#syllabus-text');
const playButton = document.querySelector('#play-button');
const showSyllabusButton = document.querySelector('.show-syllabus-button');
const showSyllabusButtonText = document.querySelector('.show-syllabus-button-text');

const audio = new SpeechSynthesisUtterance();

audio.addEventListener('end', () => {
  playButton.classList.replace('btn-danger', 'btn-warning');
  playButton.innerHTML = `
    <span><i class="bi bi-ear me-2"></i></span>
    <span>Escuchar</span>`;
});

playButton.addEventListener('click', () => {
  audio.text = syllabusText.value || syllabusText.textContent;

  if (window.speechSynthesis.speaking) {
    playButton.classList.replace('btn-danger', 'btn-warning');
    playButton.innerHTML = `
      <span><i class="bi bi-ear me-2"></i></span>
      <span>Escuchar</span>`;
    window.speechSynthesis.cancel();
  } else {
    playButton.classList.replace('btn-warning', 'btn-danger');
    playButton.innerHTML = `
      <span><i class="bi bi-stop me-2"></i></span>
      <span>Parar</span>`;
    window.speechSynthesis.speak(audio);
  }
});

showSyllabusButton && showSyllabusButton.addEventListener('click', () => {
  syllabusText.classList.toggle('hide-syllabus-text');
  showSyllabusButtonText.textContent = syllabusText.classList.contains('hide-syllabus-text') ? 'Mostrar' : 'Ocultar';
});
