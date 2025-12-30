import whisper
import os

TRANSCRIPTS_DIR = "uploads/transcripts"

# Load model once (important)
model = whisper.load_model("base")

def transcribe_audio(audio_path, video_id):
    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

    result = model.transcribe(audio_path)

    transcript_text = result["text"].strip()

    transcript_path = os.path.join(
        TRANSCRIPTS_DIR,
        f"{video_id}.txt"
    )

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    return transcript_path, transcript_text
