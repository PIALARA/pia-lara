const recordButton = document.querySelector('#record-button');
const recordStopButton = document.querySelector('#record-stop-button');
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
    if (mediaRecorder.state == 'inactive') {
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
  console.log('Recording are started..');
  recordButton.disabled = true;
  recordStopButton.disabled = false;

  audioChunks = [];
  mediaRecorder.start();
});

recordStopButton.addEventListener('click', e => {
  console.log('Recording are stopped.');
  recordButton.disabled = false;
  recordStopButton.disabled = true;

  mediaRecorder.stop();
});

sendAudio.addEventListener('click', e => {
  var form = new FormData();
  form.append('file', generalBlob, URL.createObjectURL(generalBlob));
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