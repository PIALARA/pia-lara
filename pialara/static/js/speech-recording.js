const recordButton = document.querySelector('#record-button');
const recordedAudio = document.querySelector('#recorded-audio');
const sendAudio = document.querySelector('#send-button');
const spinner = document.querySelector('#spinner');
const canvas = document.querySelector('.visualizer');
const mainSection = document.querySelector('.main-controls');
const tag = document.querySelector('.tag').innerText;

let audioChunks = [];
let generalBlob = '';
const canvasCtx = canvas.getContext("2d");
let audioCtx;

navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  handlerFunction(stream);
  visualize(stream);
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
      sendAudio.removeAttribute("hidden");

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
  spinner.removeAttribute("hidden");
  sendAudio.setAttribute("disabled","disabled")
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
      swal({
        title: "Audio guardado correctamente!",
        icon: "success",
        buttons: {
          audio: "Grabar otro audio!",
        },
      }).then((value) => {
        switch (value) {
          case "audio":
            window.location.href = tag;
            break;
          default:
            window.location.href = tag;
        }
      });
  });
});

function visualize(stream) {
  if(!audioCtx) {
    audioCtx = new AudioContext();
  }

  const source = audioCtx.createMediaStreamSource(stream);

  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  source.connect(analyser);
  //analyser.connect(audioCtx.destination);

  draw()

  function draw() {
    const WIDTH = canvas.width
    const HEIGHT = canvas.height;

    requestAnimationFrame(draw);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    canvasCtx.beginPath();

    let sliceWidth = WIDTH * 1.0 / bufferLength;
    let x = 0;


    for(let i = 0; i < bufferLength; i++) {

      let v = dataArray[i] / 128.0;
      let y = v * HEIGHT/2;

      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height/2);
    canvasCtx.stroke();

  }
}