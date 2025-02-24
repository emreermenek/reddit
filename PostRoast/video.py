from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import random

def create_video(duration: int, counter: int):
    change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
    selected_video = random.randint(1, 5)
    
    # Videoyu yükle
    clip = VideoFileClip(f"clips/{selected_video}.mp4")
    
    # Metin klibi oluştur
    watermark = TextClip('@PostRoastt', fontsize=40, color='red')  
    
    # Metin pozisyonunu ve süresini ayarla
    watermark = watermark.set_pos(("right", "bottom")).set_duration(duration + 2).set_opacity(0.3)  

    # Videoyu gerekli süreye kırp
    clip = clip.subclip(0, duration + 2)

    # Videonun orijinal genişliğini ve yüksekliğini al
    original_width, original_height = clip.size

    # YouTube Shorts için hedef en boy oranı (9:16)
    target_aspect_ratio = 9 / 16

    # En boy oranına göre video kırpma işlemini ayarla
    if original_width / original_height > target_aspect_ratio:
        new_width = int(original_height * target_aspect_ratio)
        crop_x1 = (original_width - new_width) // 2
        crop_x2 = crop_x1 + new_width
        clip = clip.crop(x1=crop_x1, x2=crop_x2)
    else:
        new_height = int(original_width / target_aspect_ratio)
        crop_y1 = (original_height - new_height) // 2
        crop_y2 = crop_y1 + new_height
        clip = clip.crop(y1=crop_y1, y2=crop_y2)

    # Watermark ekle ve son videoyu oluştur
    clip = CompositeVideoClip([clip, watermark])

    # Son videoyu bir dosyaya yaz
    try:
        clip.write_videofile(
            f"videos/{counter}.mp4",
            codec="libx264",
            audio_codec="aac",
            audio=True,  # Sesi etkinleştir
            bitrate="5000k",  
            preset="slow",  
            ffmpeg_params=["-crf", "18"]  
        )
    except Exception as e:
        print(f"An error occurred while writing the video file: {e}")