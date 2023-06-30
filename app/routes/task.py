
from app.utils.openai_utils import transcribe_audio, fix_text
from app.utils.file_utils import save_logs, guardado_txt, save_audio_file, convert_to_wav
import os, datetime
from app.celery import celery
from flask import Blueprint

task_bp = Blueprint('task_bp', __name__)

@celery.task()
def process_audio(audio_link):
    try:

        current_date = datetime.datetime.now().strftime('%Y-%m-%d') 


        audio_path, filename, log_folder, text_folder, audio_folder, current_url = save_audio_file(audio_link, current_date)
        audio_convertido = convert_to_wav (audio_path, audio_folder, filename)
        audio_transcripto = transcribe_audio (audio_convertido)
        text_filename = guardado_txt(filename, text_folder, audio_transcripto)
        audio_final = fix_text (audio_transcripto)

        save_logs(log_folder, current_date, current_url, text_filename)

        os.remove(audio_convertido)
        return audio_final['choices'][0]['message']
    
    except Exception as e:
        process_audio.retry(exc=e)


