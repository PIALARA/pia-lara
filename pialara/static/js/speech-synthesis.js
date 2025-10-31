document.addEventListener('DOMContentLoaded', () => {

const syllabusText = document.querySelector('#syllabus-text');
const playButton = document.querySelector('#play-button');
const showSyllabusButton = document.querySelector('.show-syllabus-button');
const showSyllabusButtonText = document.querySelector('.show-syllabus-button-text');

//botones audio
const speedButtonsContainer = document.querySelector('.speed-buttons');
const speedButtons = document.querySelectorAll('.speed-button');
//botones audio fin

const audio = new SpeechSynthesisUtterance();
// 🔹 Desbloquea el contexto de audio en iPhone al primer toque
document.addEventListener('click', () => {
  if (!window.speechSynthesis.speaking && !window.speechSynthesis.pending) {
    const unlock = new SpeechSynthesisUtterance('');
    window.speechSynthesis.speak(unlock);
    window.speechSynthesis.cancel();
  }
}, { once: true });




// Este evento se lanza cuando las voces han cargado correctemente
window.speechSynthesis.onvoiceschanged = () => {

  // Recogemos las voces
  const voices = window.speechSynthesis.getVoices();

  // Filtramos y obtenemos solo las voces en español
  const spanishVoices = voices.filter(voice => /es/i.test(voice.lang));

  // Se va a seleccionar la primera voz del array de voces por defecto
  audio.voice = spanishVoices[0];
  audio.lang = spanishVoices[0]?.lang || 'es-ES'; // 🔹 Necesario para Safari


  // Añadimos las voces como opciones al selector
  let html = "";

  for (const key in spanishVoices) {
    html += '<option value="' + key + '">' + spanishVoices[key].name + '</option>';
  }

  // Recogemos elemento select
  const elemVoiceSelect = document.querySelector('.voice-select');

  elemVoiceSelect.innerHTML = html;

  // Evento que se lanza cuando el selector cambia
  elemVoiceSelect.addEventListener('change', (e) => {
    // Obtenemos el value de la opción seleccionada, que a su vez es el índice del array de voces de la voz seleccionada
    // y la sustituimos por la voz actual.
    voiceIndex = e.target.value;
    audio.voice = spanishVoices[voiceIndex];
  });
};
//Selector de voz fin

// 🔹 Forzar carga de voces en Safari/iOS si ya están disponibles
if (speechSynthesis.getVoices().length > 0) {
  window.speechSynthesis.onvoiceschanged();
}



audio.addEventListener('end', () => {
  playButton.classList.replace('btn-danger', 'btn-warning');
  playButton.innerHTML = `
    <span><i class="bi bi-ear me-2"></i></span>
    <span>Escuchar</span>`;
});

console.log('Entro sistesis1:',playButton);
//botones audio  //Se inserta el if sino da error la primera vez que entra aqui (warning)
if(playButton != null)
{
  playButton.addEventListener('click', () => {
    audio.text = syllabusText.value || syllabusText.textContent;
    console.log('Entro sistesis:2');
    if (window.speechSynthesis.speaking) {
      playButton.classList.replace('btn-danger', 'btn-warning');
      playButton.innerHTML = `
        <span><i class="bi bi-ear me-2"></i></span>
        <span>Escuchar</span>`;
      console.log('Entro paro mitad:');
      window.speechSynthesis.cancel();
    } else {
      playButton.classList.replace('btn-warning', 'btn-danger');
      playButton.innerHTML = `
        <span><i class="bi bi-stop me-2"></i></span>
        <span>Parar</span>`;
      window.speechSynthesis.speak(audio);
       
      console.log('Entro escucho final:');
      
    }
    //botones audio //ajustes botones cuando le doy a escuchar
    speedButtonsContainer.style.display = 'flex';
    speedButtons.forEach(button => {
      button.addEventListener('click', () => {
          const speedFactor = parseFloat(button.dataset.speed); // Obtener la velocidad desde el atributo 'data-speed'
          audio.rate = speedFactor;
        });
    })
    //fin botones audio
  });
}
console.log('Entro sistesis3:');
showSyllabusButton && showSyllabusButton.addEventListener('click', () => {
  console.log('Entro sistesis4:');
  syllabusText.classList.toggle('hide-syllabus-text');
  showSyllabusButtonText.textContent = syllabusText.classList.contains('hide-syllabus-text') ? 'Mostrar' : 'Ocultar';
});
})