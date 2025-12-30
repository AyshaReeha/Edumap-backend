from flask import Blueprint, request, jsonify
from database.mongo import videos_collection
from utils.auth import token_required
from bson import ObjectId
from services.audio_extractor import extract_audio
from services.transcription_service import transcribe_audio


video_bp = Blueprint("video", __name__)


@video_bp.route("/submit", methods=["POST"])
@token_required
def submit_video():
    data = request.json
    video_url = data.get("video_url")

    if not video_url:
        return {"message": "Video URL required"}, 400

    user = request.user

    # 1️⃣ Insert video first
    video_doc = {
        "user_id": user["user_id"],
        "email": user["email"],
        "video_url": video_url,
        "status": "processing"
    }

    result = videos_collection.insert_one(video_doc)
    video_id = str(result.inserted_id)

    try:
        # 2️⃣ Extract audio
        audio_path = extract_audio(video_url, video_id)

        # 3️⃣ Transcribe audio
        transcript_path, transcript_text = transcribe_audio(
            audio_path,
            video_id
        )

        # 4️⃣ Update DB on success
        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {
                "status": "transcribed",
                "audio_path": audio_path,
                "transcript_path": transcript_path,
                "transcript": transcript_text
            }}
        )

        return jsonify({
            "message": "Video submitted and transcribed successfully",
            "video_id": video_id
        }), 201

    except Exception as e:
        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"status": "failed"}}
        )
        return {"message": str(e)}, 500

  
# @video_bp.route("/submit", methods=["POST"])
# @token_required
# def submit_video():
#     data = request.json
#     video_url = data.get("video_url")

#     if not video_url:
#         return {"message": "Video URL required"}, 400

#     user = request.user

#     # 1️⃣ Insert video first
#     video_doc = {
#         "user_id": user["user_id"],
#         "email": user["email"],
#         "video_url": video_url,
#         "status": "processing"
#     }

#     result = videos_collection.insert_one(video_doc)
#     video_id = str(result.inserted_id)

#     try:
#         audio_path = extract_audio(video_url, video_id)

# transcript_path, transcript_text = transcribe_audio(
#     audio_path,
#     video_id
# )

# videos_collection.update_one(
#     {"_id": ObjectId(video_id)},
#     {"$set": {
#         "status": "transcribed",
#         "audio_path": audio_path,
#         "transcript_path": transcript_path,
#         "transcript": transcript_text
#     }}
#         )

#         return jsonify({
#             "message": "Video submitted and audio extracted",
#             "video_id": video_id
#         }), 201

#     except Exception as e:
#         videos_collection.update_one(
#             {"_id": ObjectId(video_id)},
#             {"$set": {"status": "failed"}}
#         )
#         return {"message": str(e)}, 500

# @video_bp.route("/submit", methods=["POST"])
# @token_required
# def submit_video():
#     data = request.json
#     video_url = data.get("video_url")

#     if not video_url:
#         return {"message": "Video URL required"}, 400

#     user = request.user

#     # 1️⃣ Create DB record FIRST
#     video_doc = {
#         "user_id": user["user_id"],
#         "email": user["email"],
#         "video_url": video_url,
#         "status": "processing"
#     }

#     video_id = videos_collection.insert_one(video_doc).inserted_id

#     # 2️⃣ Extract audio
#     audio_path = extract_audio(video_url, f"uploads/audio/{video_id}.mp3")

#     videos_collection.update_one(
#         {"_id": video_id},
#         {"$set": {
#             "audio_path": audio_path,
#             "status": "audio_extracted"
#         }}
#     )

#     # 3️⃣ Speech-to-text (AUTO STARTS)
#     transcript = transcribe_audio(audio_path)

#     videos_collection.update_one(
#         {"_id": video_id},
#         {"$set": {
#             "transcript": transcript,
#             "status": "transcribed"
#         }}
#     )


#     return {
#         "message": "Video processed successfully",
#         "video_id": str(video_id)
#     }, 201

@video_bp.route("/my-videos", methods=["GET", "OPTIONS"])
@token_required
def my_videos():
    user = request.user

    videos = list(
        videos_collection.find({"user_id": user["user_id"]})
    )

    for v in videos:
        v["id"] = str(v["_id"])
        del v["_id"]

    return jsonify(videos), 200