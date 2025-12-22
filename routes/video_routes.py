from flask import Blueprint, request, jsonify
from database.mongo import videos_collection
from utils.auth import token_required
from bson import ObjectId
from services.audio_extractor import extract_audio


video_bp = Blueprint("video", __name__)

# @video_bp.route("/submit", methods=["POST"])
# @token_required
# def submit_video():
#     data = request.json
#     video_url = data.get("video_url")

#     if not video_url:
#         return {"message": "Video URL required"}, 400

#     user = request.user  # decoded token data

#     video_doc = {
#         "user_id": user["user_id"],
#         "email": user["email"],
#         "video_url": video_url,
#         "status": "pending"
#     }

#     videos_collection.insert_one(video_doc)

#     return {"message": "Video submitted successfully"}, 201
# def verify_token():
#     # ✅ Allow preflight request
#     if request.method == "OPTIONS":
#         return "preflight"

#     auth_header = request.headers.get("Authorization")
#     if not auth_header:
#         return None

#     try:
#         token = auth_header.split(" ")[1]
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return decoded
#     except:
#         return None
    
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

        # 3️⃣ Update DB after success
        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {
                "status": "audio_extracted",
                "audio_path": audio_path
            }}
        )

        return jsonify({
            "message": "Video submitted and audio extracted",
            "video_id": video_id
        }), 201

    except Exception as e:
        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"status": "failed"}}
        )
        return {"message": str(e)}, 500
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