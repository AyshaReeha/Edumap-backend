# from transformers import pipeline
# import os

# SUMMARIES_DIR = "uploads/summaries"

# summarizer = pipeline(
#     "summarization",
#     model="sshleifer/distilbart-cnn-12-6",
#     device=-1
# )

# def summarize_text(transcript_text, video_id):
#     os.makedirs(SUMMARIES_DIR, exist_ok=True)

#     max_chars = 2500
#     chunks = [
#         transcript_text[i:i + max_chars]
#         for i in range(0, len(transcript_text), max_chars)
#     ]

#     summaries = []

#     for chunk in chunks:
#         result = summarizer(
#             chunk,                     # ✅ ONLY transcript text
#             max_length=200,
#             min_length=120,
#             do_sample=False
#         )
#         summaries.append(result[0]["summary_text"])

#     final_summary = "\n\n".join(summaries)

#     summary_path = os.path.join(
#         SUMMARIES_DIR,
#         f"{video_id}.txt"
#     )

#     with open(summary_path, "w", encoding="utf-8") as f:
#         f.write(final_summary)

#     return summary_path, final_summary

# from transformers import pipeline
# import os

# SUMMARIES_DIR = "uploads/summaries"

# summarizer = pipeline(
#     "summarization",
#     model="sshleifer/distilbart-cnn-12-6",
#     device=-1
# )

# def summarize_text(transcript_text, video_id):
#     os.makedirs(SUMMARIES_DIR, exist_ok=True)

#     max_chars = 2500
#     chunks = [
#         transcript_text[i:i + max_chars]
#         for i in range(0, len(transcript_text), max_chars)
#     ]

#     structured_sections = []

#     for chunk in chunks:
#         prompt = (
#             "Convert the following lecture transcript into structured study notes.\n\n"
#             "Use clear topic headings and bullet points.\n"
#             "Avoid repeating sentences.\n"
#             "Focus on concepts, definitions, and examples.\n\n"
#             f"{chunk}"
#         )

#         result = summarizer(
#             prompt,
#             max_length=200,
#             min_length=120,
#             do_sample=False
#         )

#         structured_sections.append(result[0]["summary_text"])

#     final_summary = "\n\n".join(structured_sections)

#     summary_path = os.path.join(
#         SUMMARIES_DIR,
#         f"{video_id}.txt"
#     )

#     with open(summary_path, "w", encoding="utf-8") as f:
#         f.write(final_summary)

#     return summary_path, final_summary


#modeelldlllll

# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
# import os

# SUMMARIES_DIR = "uploads/summaries"

# # Load FLAN-T5 once
# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")



# def summarize_text(transcript_text, video_id):
#     os.makedirs(SUMMARIES_DIR, exist_ok=True)

#     # Instruction that FLAN-T5 will *follow*
#     prompt = f"""
#     You are an expert educational summarizer.

#     Given the following lecture transcript, produce a clear
#     topic-wise summary with headings and bullet points.
#     Include main ideas, key concepts, subtopics and concise explanations.

#     Transcript:
#     \"\"\"
#     {transcript_text}
#     \"\"\"

#     Output structured summary.
#     """

#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)

#     outputs = model.generate(
#         **inputs,
#         max_length=512,
#         num_beams=4,
#         early_stopping=True
#     )

#     summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Save summary file
#     summary_path = os.path.join(SUMMARIES_DIR, f"{video_id}.txt")
#     with open(summary_path, "w", encoding="utf-8") as f:
#         f.write(summary)

#     return summary_path, summary
import subprocess
import os
import textwrap

SUMMARIES_DIR = "uploads/summaries"

def summarize_text(transcript_text, video_id):
    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    # Keep chunk size reasonable for LLaMA context
    max_chars = 3000
    chunks = [
        transcript_text[i:i + max_chars]
        for i in range(0, len(transcript_text), max_chars)
    ]

    summaries = []

    for chunk in chunks:
        prompt = f"""
You are an expert academic note creator.

Create structured study notes from the lecture below.

Instructions:
- Use clear topic headings (##)
- Bullet points under each heading
- Merge repeated ideas
- Avoid repeating sentences
- Be concise and accurate
- No introductions or conclusions

{chunk}
"""
        # OLLAMA_PATH = r"C:\Users\ASUS\.ollama"

        result = subprocess.run(
            ["ollama", "run", "llama2:7b-chat"],
            input=prompt,
            text=True,
            capture_output=True
        )

        summaries.append(result.stdout.strip())

    final_summary = "\n\n".join(summaries)

    summary_path = os.path.join(SUMMARIES_DIR, f"{video_id}.txt")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(final_summary)

    return summary_path, final_summary
