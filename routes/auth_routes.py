from flask import Blueprint, request, jsonify
import bcrypt
from database.mongo import users_collection
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY
from bson import ObjectId

auth_bp = Blueprint("auth", __name__)

# ======================
# SIGNUP
# ======================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "Signup successful"}), 201


# ======================
# LOGIN (WITH JWT)
# ======================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"message": "Invalid password"}), 401

    # 🔐 CREATE JWT TOKEN
    token = jwt.encode(
        {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "username": user["username"]
    }), 200


# ======================
# TEST ROUTE
# ======================
@auth_bp.route("/test", methods=["GET"])
def test():
    return {"message": "Auth blueprint working"}
