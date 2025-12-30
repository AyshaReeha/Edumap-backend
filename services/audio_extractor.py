import yt_dlp
import os

AUDIO_DIR = "uploads/audio"

def extract_audio(video_url, video_id):
    os.makedirs(AUDIO_DIR, exist_ok=True)

    output_template = os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s")

    print("FFMPEG EXISTS:", os.path.exists(r"C:\ffmpeg.exe"))
    print("FFPROBE EXISTS:", os.path.exists(r"C:\ffprobe.exe"))

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "ffmpeg_location": r"C:\ffmpeg",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    final_audio = os.path.join(AUDIO_DIR, f"{video_id}.mp3")

    if not os.path.exists(final_audio):
        raise FileNotFoundError(f"Audio not created: {final_audio}")

    return final_audio

# def extract_audio(video_url, video_id):
#     os.makedirs(AUDIO_DIR, exist_ok=True)

#     output_path = os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s")

#     ydl_opts = {
#     "format": "bestaudio/best",
#     "outtmpl": output_path,
#     "ffmpeg_location": r"C:\ffmpeg",
#     "postprocessors": [
#         {
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": "mp3",
#             "preferredquality": "192",
#         }
#     ],
#     "quiet": True,
#     }


#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])

#     return f"{AUDIO_DIR}/{video_id}.mp3"
