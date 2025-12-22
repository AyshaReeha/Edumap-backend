import yt_dlp
import os

AUDIO_DIR = "uploads/audio"

def extract_audio(video_url, video_id):
    os.makedirs(AUDIO_DIR, exist_ok=True)

    output_path = os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s")

    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_path,
    "ffmpeg_location": r"C:\ffmpeg",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "quiet": True,
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return f"{AUDIO_DIR}/{video_id}.mp3"
