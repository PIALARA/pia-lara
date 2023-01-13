const recordButton = document.querySelector('.record-button');
const recordedAudio = document.querySelector('#recorded-audio');
const spinner = document.querySelector('#spinner');
const canvas = document.querySelector('.visualizer');
const $sendButton = $("#send-button");

let audioChunks = [];
let generalBlob = '';
const canvasCtx = canvas.getContext('2d');
let audioCtx;
let duration;

navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {
    handlerFunction(stream);
    visualize(stream);
});

function handlerFunction(stream) {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.addEventListener('dataavailable', e => {
        audioChunks.push(e.data);
        if (mediaRecorder.state === 'inactive') {
            let blob = new Blob(audioChunks, {type: 'audio/mpeg-3'});
            const url = URL.createObjectURL(blob);
            recordedAudio.controls = true;
            recordedAudio.src = url;
            generalBlob = blob;
        }
    });
}

recordButton.addEventListener('click', () => {
    if (mediaRecorder.state === 'inactive') {
        console.log('Recording started.');
        $sendButton.hide();
        recordButton.classList.add('recording');
        canvas.style.display = 'block';
        recordedAudio.controls = false;
        audioChunks = [];
        mediaRecorder.start();
        duration = new Date();
    } else if (mediaRecorder.state === 'recording') {
        canvas.style.display = 'none';
        console.log('Recording stopped.');
        recordButton.classList.remove('recording');
        $sendButton.show();
        mediaRecorder.stop();
        duration = parseInt((new Date() - duration) / 1000);
    }
});

$sendButton.on('click', () => {
    spinner.removeAttribute('hidden');

    var form = new FormData();
    form.append('file', generalBlob);
    $sendButton
        .attr('disabled', true)
        .text('espere...');
    form.append('duration', duration);
    //Chrome inspector shows that the post data includes a file and a title.
    $.ajax({
        type: 'POST',
        url: '/audios/save-record',
        data: form,
        cache: false,
        processData: false,
        contentType: false,
    }).done(function (data) {
        $sendButton
            .hide()
            .attr('disabled', false)
            .text('espere...');

        recordedAudio.controls = false;
        swal({
            title: data.message || '',
            icon: data.status === 'ok' ? 'success' : 'error',
            buttons: {
                audio: {
                    text: 'Grabar otro audio',
                    value: 'grabar'
                },
            },
        }).then(value => {
            if (value === "grabar")
                window.location.reload()
        })
    }).fail(e => {
        swal({
            title: 'Error',
            icon: 'error',
            text: 'Ha habido un error al subir el audio. Por favor, reinicie el navegador y reinténtlo de nuevo.',
        })

    });

})

function visualize(stream) {
    if (!audioCtx) {
        audioCtx = new AudioContext();
    }

    const source = audioCtx.createMediaStreamSource(stream);

    const analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    source.connect(analyser);
    //analyser.connect(audioCtx.destination);

    draw();

    function draw() {
        const WIDTH = canvas.width;
        const HEIGHT = canvas.height;

        requestAnimationFrame(draw);

        analyser.getByteTimeDomainData(dataArray);

        canvasCtx.fillStyle = 'rgb(255, 255, 255)';
        canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = 'rgb(249, 81, 96, 255)';

        canvasCtx.beginPath();

        let sliceWidth = (WIDTH * 1.0) / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            let v = dataArray[i] / 128.0;
            let y = (v * HEIGHT) / 2;

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
}
