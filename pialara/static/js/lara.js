const startButton = document.getElementById('startRecording');
const stopButton = document.getElementById('stopRecording');
const statusDisplay = document.getElementById('status');
const transcriptionDisplay = document.getElementById('transcription');

let mediaRecorder;
let audioChunks = [];

startButton.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            statusDisplay.textContent = "Grabando...";

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio_data', audioBlob, 'recording.wav');

                fetch('/lara/save_record', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        transcriptionDisplay.textContent = `Error: ${data.error}`;
                    } else {
                        transcriptionDisplay.textContent = data.text;
                    }
                })
                .catch(error => {
                    transcriptionDisplay.textContent = `Error: ${error}`;
                });

                audioChunks = [];
                statusDisplay.textContent = "Grabación detenida";
            });

            startButton.disabled = true;
            stopButton.disabled = false;
        });
});

stopButton.addEventListener('click', () => {
    mediaRecorder.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
});
