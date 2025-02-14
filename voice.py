from TTS.api import TTS
from pydub import AudioSegment
import os

def initialize_tts():
    #tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=True)
    tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True, gpu=True)
    return tts


def create_audio(text : str, counter : int, tts : TTS):
     #Metni sese dönüştür
    tts.tts_to_file(
        text, 
        file_path=f"audios/{counter}.wav", 
        speed=1.0, 
        pitch=0.8, 
        volume=1.2
        )
    # WAV dosyasını yükle
    audio = AudioSegment.from_wav(f"audios/{counter}.wav")

    #hızını arttır
    audio = audio.speedup(playback_speed=1.1)
    # MP3 formatında kaydet
    audio.export(f"audios/{counter}.mp3", format="mp3")
    os.remove(f"audios/{counter}.wav")
    

