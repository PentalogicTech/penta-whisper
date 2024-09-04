import openai
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

API_KEY = os.getenv("API_KEY")
ORGANIZATION = os.getenv("ORGANIZATION")
costo_token = os.getenv("COSTO_GPT")

openai.api_key = API_KEY
openai.organization = ORGANIZATION
openai.Model.list()

def transcribe_audio(audio_convertido):
    media_file = open(audio_convertido, "rb")

    transcripto = openai.Audio.transcribe(    
        model="whisper-1",
        file=media_file,
    )

    return transcripto

    
def fix_text(transcripto):
    corregido = openai.ChatCompletion.create(
        model="gpt-4o", 
        temperature=0,
        max_tokens=2000,        
        messages=[
            {"role": "system","content": os.getenv("PROMPT")},
            {"role":"user","content":transcripto["text"]}
        ]
    )

    costo_gpt = corregido['usage']['total_tokens'] * 0.000005
    return corregido, costo_gpt

    