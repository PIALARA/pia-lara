import os, uuid
from flask import (
    Blueprint, render_template, request, current_app
)
# from gradio_client import Client, file

bp = Blueprint('lara', __name__)
rutaAudio = "audio_files/"

@bp.route('/lara')
def login():
    return render_template('lara/lara.html')


# @bp.route('/lara/save_record', methods=['POST'])
# def save_record():
#     print("Guardando audio")
#     audio_file = request.files['audio_data']
#     if not os.path.isdir('audio_files'):
#         os.makedirs('audio_files')

#     name_audio = str(uuid.uuid4()) + '.wav'
#     audio_file.save(os.path.join('audio_files', name_audio))

#     GRADIO_URL = current_app.config['GRADIO_URL']

#     client = Client(GRADIO_URL, ssl_verify=False)
#     transcription = client.predict(
#             audio=file(rutaAudio + name_audio),
#             modelo="base",
#             api_name="/predict"
#     )

#     return {'status': 'ok', 'text': transcription}
