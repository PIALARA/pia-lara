import os, uuid
from flask import (
    Blueprint, render_template, request, current_app
)
from gradio_client import Client, file

bp = Blueprint('lara', __name__)

@bp.route('/lara')
def login():
    return render_template('lara/lara.html')

@bp.route('/lara/save_record', methods=['POST'])
def save_record():

    audio_file = request.files['audio_data']
    print(audio_file)

    name_audio = str(uuid.uuid4()) + '.wav'
    RUTA_AUDIO = current_app.config['AUDIO_PATH']
    print(RUTA_AUDIO)
    audio_file.save(os.path.join(RUTA_AUDIO, name_audio))

    GRADIO_URL = current_app.config['GRADIO_URL']

    client = Client(GRADIO_URL, ssl_verify=False)
    transcription = client.predict(
            audio=file(RUTA_AUDIO + "/" + name_audio),
            modelo="base",
            api_name="/predict"
    )

    return {'status': 'ok', 'text': transcription}

