from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)

db = client.get_database()


users_collection = db["users"]
videos_collection = db["videos"]

print("MongoDB connected successfully")
