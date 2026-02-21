from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["autostylist"]

wardrobe_collection = db["wardrobe"]
users_collection = db["users"]
token_blocklist_collection = db["token_blocklist"]
