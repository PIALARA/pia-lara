const recordButton = document.getElementById('recordButton');
const sendButton = document.getElementById('sendRecording');
const modelSelect = document.getElementById('modelSelect');
const statusDisplay = document.getElementById('status');
const transcriptionDisplay = document.getElementById('transcription');
const spinner = document.getElementById('spinner');
const canvas = document.getElementById('canvas');
const canvasCtx = canvas.getContext('2d');

let mediaRecorder;
let audioChunks = [];
let audioBlob;
let isRecording = false;
let audioContext;
let analyser;
let dataArray;
let bufferLength;

function showStatus(message, type = 'info') {
    statusDisplay.textContent = message;
    statusDisplay.className = `alert alert-${type} w-50 text-center`;
    statusDisplay.style.display = 'block';
}

function drawVisualizer() {
    if (!isRecording) return;
    requestAnimationFrame(drawVisualizer);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

    canvasCtx.lineWidth = 2;

    // Create gradient for blurred edges
    let gradient = canvasCtx.createLinearGradient(0, 0, canvas.width, 0);
    gradient.addColorStop(0, 'rgba(60, 130, 146, 0)');
    gradient.addColorStop(0.1, 'rgba(60, 130, 146, 1)');
    gradient.addColorStop(0.9, 'rgba(60, 130, 146, 1)');
    gradient.addColorStop(1, 'rgba(60, 130, 146, 0)');

    canvasCtx.strokeStyle = gradient;

    canvasCtx.beginPath();

    let sliceWidth = canvas.width / bufferLength;
    let x = 0;

    for (let i = 0; i < bufferLength; i++) {
        let v = dataArray[i] / 128.0;
        let y = (v * canvas.height) / 2;

        if (i === 0) {
            canvasCtx.moveTo(x, y);
        } else {
            canvasCtx.lineTo(x, y);
        }

        x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();
}

recordButton.addEventListener('click', () => {
    const messageElement = document.getElementById('response-message');
    const transcripcion = document.getElementById('transcription');
    transcripcion.textContent = '';
    messageElement.textContent = '';
    if (!isRecording) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioContext.createAnalyser();
                analyser.fftSize = 2048;
                bufferLength = analyser.frequencyBinCount;
                dataArray = new Uint8Array(bufferLength);

                const source = audioContext.createMediaStreamSource(stream);
                source.connect(analyser);

                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                showStatus("Grabando...", 'info');
                recordButton.textContent = "Detener Grabación";
                recordButton.classList.remove('btn-custom');
                recordButton.classList.add('btn-danger');
                isRecording = true;

                drawVisualizer();

                // Deshabilitar el botón "Enviar" al comenzar una nueva grabación
                sendButton.disabled = true;

                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener('stop', () => {
                    audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    audioChunks = [];
                    showStatus("Selecciona un modelo de la lista", 'warning');
                    sendButton.disabled = false;
                    audioContext.close();
                });
            });
    } else {
        mediaRecorder.stop();
        recordButton.textContent = "Comenzar Grabación";
        recordButton.classList.remove('btn-danger');
        recordButton.classList.add('btn-custom');
        isRecording = false;
    }
});

sendButton.addEventListener('click', () => {
    const selectedModel = modelSelect.value;
    if (!selectedModel) {
        showStatus("Por favor, selecciona un modelo antes de enviar.", 'danger');
        return;
    }
    
    transcriptionDisplay.textContent = ""; 
    spinner.style.display = "block"; 

    const formData = new FormData();
    formData.append('audio_data', audioBlob, 'recording.wav');
    formData.append('model', selectedModel);

    fetch('/lara/save_record', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        spinner.style.display = "none"; 
        if (data.error) {
            showStatus(`Error: ${data.error}`, 'danger');
        } else {
            transcriptionDisplay.textContent = data.text;
            showStatus("Transcripción completada", 'success');
        }
        enableButtons()
    })

    .catch(error => {
        spinner.style.display = "none";
        showStatus(`Error: ${error}`, 'danger');
    });

    showStatus("Grabación enviada para transcripción", 'info');
   
});

function enableButtons() {
    document.getElementById('happyBtn').removeAttribute('disabled');
    document.getElementById('neutralBtn').removeAttribute('disabled');
    document.getElementById('sadBtn').removeAttribute('disabled');
}

function disabledButtons(){
    document.getElementById('happyBtn').setAttribute('disabled', 'disabled');
    document.getElementById('neutralBtn').setAttribute('disabled', 'disabled');
    document.getElementById('sadBtn').setAttribute('disabled', 'disabled');

}

function submitFeedback(emotion) {
    const messageElement = document.getElementById('response-message');
    
    switch(emotion) {
        case 'happy':
            messageElement.textContent = '¡Gracias por tu feedback positivo!';
            messageElement.style.color = 'green';
            disabledButtons()
            sendSurvey("Bien")
            break;
        case 'neutral':
            messageElement.textContent = 'Gracias por tu feedback.';
            messageElement.style.color = 'orange';
            disabledButtons()
            sendSurvey("Normal")
            break;
        case 'sad':
            messageElement.textContent = 'Lamentamos que tu experiencia no haya sido buena.';
            messageElement.style.color = 'red';
            disabledButtons()
            sendSurvey("Mal")
            break;
        default:
            messageElement.textContent = '';
            break;
    }
}


function sendSurvey(emotion){

    fetch('/lara/send_survey', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ emotion: emotion }) // Envía la emoción seleccionada al servidor
    })
    .then(response => response.json())
    .then(data => {
        // Aquí puedes manejar la respuesta del servidor si es necesario
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}