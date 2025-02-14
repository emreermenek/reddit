from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import random



def create_video(duration : int, counter : int):
    change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
    selected_video = random.randint(1,5)
    # Load the video
    clip = VideoFileClip(f"clips/{selected_video}.mp4")
    # Generate a text clip  
    watermark = TextClip('@redstories_s', fontsize=50, color='red')  
    
    # setting position of text in the center and duration will be 10 seconds  
    watermark = watermark.set_pos(("right","bottom")).set_duration(duration+2).set_opacity(0.3)  

    # Clip the video to the first 10 seconds
    clip = clip.subclip(0, duration+2)

    # Get the original width and height of the video
    original_width, original_height = clip.size

    # Target aspect ratio for YouTube Shorts (9:16)
    target_aspect_ratio = 9 / 16

    # Calculate the new dimensions
    if original_width / original_height > target_aspect_ratio:
        # Crop the sides (center crop)
        new_width = int(original_height * target_aspect_ratio)
        crop_x1 = (original_width - new_width) // 2
        crop_x2 = crop_x1 + new_width
        clip = clip.crop(x1=crop_x1, x2=crop_x2)
    else:
        # Crop the top and bottom (less common for horizontal videos)
        new_height = int(original_width / target_aspect_ratio)
        crop_y1 = (original_height - new_height) // 2
        crop_y2 = crop_y1 + new_height
        clip = clip.crop(y1=crop_y1, y2=crop_y2)

    clip = CompositeVideoClip([clip, watermark])

    # Write the final video to a file
    clip.write_videofile(
        f"videos/{counter}.mp4", 
        codec="h264_nvenc",  # NVENC ile hızlandırılmış H.264 encoding
        preset="p4", 
        #codec="libx264", 
        audio_codec="aac", 
        audio=False)