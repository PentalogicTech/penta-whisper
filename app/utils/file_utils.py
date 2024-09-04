import os, requests
import datetime
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
from pydub import AudioSegment

costo_minuto_whisper = 0.006


# Recibe el link de audio, crea las carpetas y lo guarda
def save_audio_file(audio_link, current_date):

    # Evalua si es link valido 
    response = requests.get(audio_link)
    if response.status_code != 200:
        return 'No se pudo descargar el archivo de audio', 400
    
    # Obtener el nombre del archivo original
    filename = secure_filename(os.path.basename(audio_link))


    # Obtener el nombre del host o dominio de la URL
    url_parts = urlparse(audio_link)
    current_url = url_parts.netloc

    # Creacion de carpetas para los archivos
    log_folder = os.path.join('Logs')
    audio_folder = os.path.join('Data', current_date, current_url, 'Audios')
    text_folder = os.path.join('Data', current_date, current_url, 'Textos')
    
    os.makedirs(log_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)

    # Guarda el archivo de audio
    audio_path = os.path.join(audio_folder, filename)
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(response.content)
    

    return audio_path, filename, log_folder, text_folder, audio_folder, current_url

# Calculo de duracion del audio para monetizar
def calculo_costo_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    duration_seconds = len(audio) / 1000.0  # Convertir milisegundos a segundos
    
    costo_audio = (duration_seconds /60) * costo_minuto_whisper # Paso a minutos y calculo el costo
    
    return costo_audio


def convert_to_wav(audio_path, audio_folder, filename):
    audio = AudioSegment.from_file(audio_path)
    audio_convertido = os.path.join(audio_folder, os.path.splitext(filename)[0] + ".mp3")
    audio.export(audio_convertido, format="mp3")

    return audio_convertido

def guardado_txt (filename, text_folder, transcripto):
    text_filename = f'{os.path.splitext(filename)[0]}.txt'
    text_path = os.path.join(text_folder, text_filename)
    with open(text_path, 'w') as output_file:
        output_file.write(transcripto["text"])

    return text_filename

def save_logs(log_folder, current_date, current_url, text_filename):
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    log_filename = f'{os.path.join(log_folder,current_date)}.txt'
    with open(log_filename, 'a') as log_file:
        log_file.write(f'{current_time} -- ')
        log_file.write(f'{current_url} -- ')
        log_file.write(f'{text_filename}\n')