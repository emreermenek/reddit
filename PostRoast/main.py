import os
import reddit as rd
import video as vid
import subtitle as sub
import upload as up
from mutagen.mp3 import MP3
import shutil
import asyncio
from voice import create_audio, isGender

# Klasörler varsa sil
if os.path.exists('audios'):
    shutil.rmtree('audios')  # Klasörü ve içindekileri sil
    
if os.path.exists('videos'):
    shutil.rmtree('videos')
    
if os.path.exists('subtitles'):
    shutil.rmtree('subtitles')
    
if os.path.exists('output'):
    shutil.rmtree('output')

# Yeniden oluştur
os.makedirs('audios')
os.makedirs('videos')
os.makedirs('subtitles')
os.makedirs('output')

# Reddit'ten hikayeleri al ve filtrele
filtered_stories = rd.fetch_and_filter()
genders = isGender()

async def main():
    counter = 1
    for story, gender in zip(filtered_stories, genders):
        # İlk adım: Ses dosyasını oluştur
        print("creating audio")
        text = story['selftext']
        await create_audio(text, counter, gender)
        
        # Ses dosyasının uzunluğunu al ve video oluştur
        print("creating video")
        audio_path = f"audios/{counter}.mp3"
        if not os.path.exists(audio_path):
            print(f"Audio file {audio_path} does not exist.")
            continue
        try:
            audio = MP3(audio_path)
            duration = audio.info.length  # Süreyi saniye cinsinden al
            vid.create_video(duration, counter)
        except Exception as e:
            print(f"An error occurred while processing audio file {audio_path}: {e}")
            continue

        # Altyazı oluştur ve videoyu birleştir
        print("creating output")
        sub.usage(counter, duration)

        # YouTube'a yükle
        print("Uploading to youtube")
        up.upload_video(f'output/{counter}.mp4', story)
        
        counter += 1

if __name__ == "__main__":
    asyncio.run(main())