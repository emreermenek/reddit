import os
import reddit as rd
import video as vid
import subtitle as sub
import upload as up
from mutagen.mp3 import MP3
import shutil
import voice as vo
from TTS.api import TTS

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

#python surumu 3.11.6 ya dusurdum
filtered_stories = rd.fetch_and_filter()

urls = []
counter = 1

tts = vo.initialize_tts()

for story in filtered_stories:
    if(counter == 6):
        break
    if up.check_story(story)[0] == "False":
            continue


    
    print("creating audio")
 # creating audio   
    text = story['selftext']
    vo.create_audio(text, counter, tts)
    
    #creating video by looking how long audio is

    print("creating video")
    audio = MP3(f"audios/{counter}.mp3")  # Replace with your file name
    duration = audio.info.length  # Duration in seconds
    vid.create_video(duration, counter)


    
    #creating subtitle and merging everyting
    print("creating output")
    sub.usage(counter, duration)


    print("Uploading to youtube")
    #up.upload_video(f'output/{counter}.mp4', story)
    
    
    counter += 1
    






