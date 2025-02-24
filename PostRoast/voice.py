import asyncio
import edge_tts
import os
import google.generativeai as genai
import json
import reddit as rd

filtered_stories = rd.fetch_and_filter()

def load_api_key():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config['genai_api_key']

def isGender():
    api_key = load_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    counter = 1
    genders = []
    for story in filtered_stories:
        if counter > 5:
            break
        response = model.generate_content(f"What is the this writer gender : {story['selftext']}  just write male female or unisex do not write anything else")
        gender = response.text.strip().lower()
        genders.append(gender)
        counter += 1
    return genders

async def create_audio(text: str, counter: int, gender: str):
    mp3_file_path = f"audios/{counter}.mp3"
    try:
        # Cinsiyete göre ses modelini seç
        if gender == "female":
            voice_model = "en-US-JennyNeural"
        else:
            voice_model = "en-US-GuyNeural"

        # Metni sese dönüştür ve MP3 dosyası olarak kaydet
        communicate = edge_tts.Communicate(text, voice_model)
        await communicate.save(mp3_file_path)

        # Dosyanın başarıyla oluşturulup oluşturulmadığını kontrol et
        if not os.path.exists(mp3_file_path):
            raise FileNotFoundError(f"File {mp3_file_path} was not created.")

        print(f"Audio saved as {mp3_file_path}")
    except Exception as e:
        print(f"An error occurred while creating audio: {e}")