import ffmpeg
import whisper


def generate_subtitles(audio_path: str, ass_path: str):
    """Use Whisper to transcribe audio and save as ASS file with styling"""
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, word_timestamps=True)
    
    with open(ass_path, "w", encoding="utf-8") as f:
        # ASS header with style definitions
        f.write("""[Script Info]
Title: Whisper Altyazı
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,42,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")

        for segment in result["segments"]:
            for word_info in segment.get("words", []):
                start = word_info["start"]
                end = word_info["end"]
                word = word_info["word"].strip()
                
                f.write(f"Dialogue: 0,{format_ass_timestamp(start)},{format_ass_timestamp(end)},Default,,0,0,0,,{word}\\N\n")

def format_ass_timestamp(seconds: float):
    """Convert seconds to ASS timestamp format (H:MM:SS.cc)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours}:{minutes:02}:{seconds:05.2f}"

def add_audio_and_subtitles(video_path: str, audio_path: str, subtitle_path: str, output_path: str, duration : int):
    """Adds audio and burns styled subtitles into video"""
    
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    input_music_audio = ffmpeg.input("horror_background_music.mp3")
    
    
    # Altyazı stilleriyle birlikte videoya işle
    video_with_subs = input_video.filter(
        "subtitles", 
        subtitle_path,
        force_style="Alignment=2,Fontsize=24,MarginV=70"  # Ek stil ayarları
    )

    # Videodaki mevcut sesi al
    original_audio = input_audio.audio
    #new_audio = input_music_audio.audio.filter("volume", 0.3)
    new_audio = input_music_audio.audio.filter("atrim", duration=duration+2).filter("volume", 0.3)
    
    # İki sesi birleştir
    mixed_audio = ffmpeg.filter([original_audio, new_audio], "amix", inputs=2, duration="longest", dropout_transition=2)
    
    # Ses ve videoyu birleştir
    output = ffmpeg.output(
        video_with_subs,
        mixed_audio,
        output_path,
        vcodec="libx264",
        acodec="aac",
        audio_bitrate="192k",
        format="mp4",
        **{"map": "0:v:0", "map": "1:a:0"}
    )
    
    output.run(overwrite_output=True)

def usage(counter : int, duration : int):
    # Kullanım
    audio_file = f"audios/{counter}.mp3"
    video_file = f"videos/{counter}.mp4"
    subtitle_file = f"subtitles/{counter}.ass"  # Artık ASS formatında
    output_video = f"output/{counter}.mp4"

    generate_subtitles(audio_file, subtitle_file)
    add_audio_and_subtitles(video_file, audio_file, subtitle_file, output_video, duration)