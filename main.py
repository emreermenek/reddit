import praw
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from gtts import gTTS
import subprocess
import reddit as rd
import video as vid
import subtitle as sub


from mutagen.mp3 import MP3


if not os.path.exists('audios'):
    os.makedirs('audios')
    
if not os.path.exists('videos'):
    os.makedirs('videos')
    
if not os.path.exists('subtitles'):
    os.makedirs('subtitles')
    
if not os.path.exists('output'):
    os.makedirs('output')


filtered_stories = rd.fetch_and_filter()

urls = []
counter = 1




for story in filtered_stories:
    if(counter ==2):
        break
#     print("creating audio")
#  # creating audio   
#     text = story['selftext']
#     language = 'en'
#     speech = gTTS(text=text, lang=language, slow=False)

# # Saving the converted audio in an mp3 file
#     speech.save(f"audios/{counter}.mp3")

# # Use ffmpeg to speed up the audio by 1.7x
#     input_file = f"audios/{counter}.mp3"
#     output_file = f"audios/{counter}_fast.mp3"
#     subprocess.run(['ffmpeg', '-i', input_file, '-filter:a', 'atempo=1.3', output_file])

#     os.remove(input_file)

#     os.rename(output_file, input_file)
    
    #creating video by looking how long audio is

    print("creating video")
    audio = MP3(f"audios/{counter}.mp3")  # Replace with your file name
    duration = audio.info.length  # Duration in seconds
    # vid.create_video(duration, counter)


    
    #creating subtitle and merging everyting
    print("creating output")
    sub.usage(counter, duration)
    
    
    counter += 1
    






