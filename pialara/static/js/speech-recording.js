const recordButton = document.querySelector('#record-button');
const recordedAudio = document.querySelector('#recorded-audio');
const sendAudio = document.querySelector('#send-button');

let audioChunks = [];
let generalBlob = '';

navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  handlerFunction(stream);
});

function handlerFunction(stream) {
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.addEventListener('dataavailable', e => {
    audioChunks.push(e.data);
    if (mediaRecorder.state === 'inactive') {
      let blob = new Blob(audioChunks, { type: 'audio/mpeg-3' });
      console.log(blob);
      // sendData(blob);
      const url = URL.createObjectURL(blob);
      recordedAudio.controls = true;
      recordedAudio.src = url;
      generalBlob = blob
    }
  });
}

recordButton.addEventListener('click', e => {
  if (mediaRecorder.state === 'inactive') {
    console.log('Recording are started..');
    recordButton.classList.replace('btn-success', 'btn-danger');
    recordButton.innerHTML = '<i class="bi bi-stop me-2"></i>Parar de grabar';
    recordedAudio.controls = false;
    audioChunks = [];
    mediaRecorder.start();
  } else if (mediaRecorder.state === 'recording') {
    console.log('Recording are stopped.');
    recordButton.classList.replace('btn-danger', 'btn-success');
    recordButton.innerHTML = '<i class="bi bi-mic me-2"></i>Volver a grabar';
    mediaRecorder.stop();
  }
});

sendAudio.addEventListener('click', e => {
  var form = new FormData();
  form.append('file', generalBlob);
  form.append('title', 'data.mp3');
  //Chrome inspector shows that the post data includes a file and a title.
  $.ajax({
      type: 'POST',
      url: '/audios/save-record',
      data: form,
      cache: false,
      processData: false,
      contentType: false
  }).done(function(data) {
      window.location.href = "create";
  });
});