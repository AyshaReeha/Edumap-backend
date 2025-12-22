from flask import Flask
from flask_cors import CORS   # ✅ import CORS
from routes.auth_routes import auth_bp
from routes.video_routes import video_bp

app = Flask(__name__)
CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:3000"}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"],
)
app.register_blueprint(video_bp, url_prefix="/api/video")

app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return {"message": "EDU-MAP Backend Running with MongoDB"}

if __name__ == "__main__":
    app.run(debug=True)




